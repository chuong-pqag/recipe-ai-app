import os
import random
import streamlit as st
import bcrypt
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from supabase import create_client, Client

# Cấu hình trang
st.set_page_config(page_title="AI Gợi ý món ăn", page_icon="🍲", layout="wide")
GUEST_AVATAR_URL = "https://cyfekkruuahcrbalwhiq.supabase.co/storage/v1/object/public/avatars/avatar_kh1.jpg"

# Load biến môi trường (DB_URL)
DB_URL = st.secrets.get("DB_URL", None)
if not DB_URL:
    load_dotenv()
    DB_URL = os.getenv("DB_URL") or os.getenv("DATABASE_URL")

if not DB_URL:
    st.error("❌ Không tìm thấy DB_URL trong .env hoặc secrets.toml")
    st.stop()

# Kết nối DB
@st.cache_resource
def get_engine():
    return create_engine(DB_URL, pool_size=5, max_overflow=0)

engine = get_engine()

# Kết nối Supabase Storage
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load model embedding
@st.cache_resource
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

model = load_model()

# ====== Xử lý tài khoản ======
def create_user(username, password, email, avatar_url=None):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO users (username, password, email, avatar) VALUES (:u, :p, :e, :a)"),
            {"u": username, "p": hashed_pw, "e": email, "a": avatar_url}
        )

def authenticate_user(username, password):
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT id, username, password, avatar FROM users WHERE username=:u"),
            {"u": username}
        ).fetchone()
        if row and bcrypt.checkpw(password.encode(), row.password.encode()):
            # Trả về dict thay vì Row
            return dict(row._mapping)
    return None

# ====== Sidebar: Đăng nhập / Đăng ký ======
if "user" not in st.session_state:
    st.session_state.user = None

st.sidebar.markdown("## 👤 Tài khoản")

if st.session_state.user is None:
    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <img src="{GUEST_AVATAR_URL}" width="80" style="border-radius:10%;">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<p style='text-align:center; font-weight:bold;'>Khách vãng lai</p>",
        unsafe_allow_html=True
    )

    with st.sidebar.expander("🔑 Đăng nhập"):
        login_user = st.text_input("Tên đăng nhập", key="login_user")
        login_pass = st.text_input("Mật khẩu", type="password", key="login_pass")
        if st.button("Đăng nhập"):
            user = authenticate_user(login_user, login_pass)
            if user:
                st.session_state.user = user
                st.success(f"Xin chào {user['username']} 👋")
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu!")

    with st.sidebar.expander("📝 Đăng ký"):
        reg_user = st.text_input("Tên đăng nhập", key="reg_user")
        reg_email = st.text_input("Email", key="reg_email")
        reg_pass = st.text_input("Mật khẩu", type="password", key="reg_pass")
        reg_avatar_file = st.file_uploader("Ảnh đại diện", type=["png", "jpg", "jpeg"], key="reg_avatar")

        if st.button("Đăng ký"):
            avatar_url = None
            if reg_avatar_file:
                file_name = f"{reg_user}_{reg_avatar_file.name}"
                supabase.storage.from_("avatars").upload(
                    file_name,
                    reg_avatar_file.getvalue(),
                    {"content-type": reg_avatar_file.type}
                )
                avatar_url = supabase.storage.from_("avatars").get_public_url(file_name)

            try:
                create_user(reg_user, reg_pass, reg_email, avatar_url)
                st.success("🎉 Đăng ký thành công! Hãy đăng nhập.")
            except Exception as e:
                st.error(f"Lỗi đăng ký: {e}")

else:
    # Đã đăng nhập
    avatar_url = st.session_state.user.get("avatar") or "data/avatar_kh.jpg"
    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <img src="{avatar_url}" width="80" style="border-radius:10%;">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        f"<p style='text-align:center; font-weight:bold;'>{st.session_state.user['username']}</p>",
        unsafe_allow_html=True
    )
    # === Nút đổi avatar ===
    with st.sidebar.expander("🖼️ Đổi avatar"):
        new_avatar_file = st.file_uploader("Chọn ảnh mới", type=["png", "jpg", "jpeg"], key="new_avatar")
        if new_avatar_file and st.button("Cập nhật avatar"):
            # Tên file trên Supabase
            file_name = f"{st.session_state.user.username}_{new_avatar_file.name}"
            supabase.storage.from_("avatars").upload(
                file_name,
                new_avatar_file.getvalue(),
                {"content-type": new_avatar_file.type}
            )
            new_avatar_url = supabase.storage.from_("avatars").get_public_url(file_name)

            # Sau khi upload ảnh và update DB
            with engine.begin() as conn:
                conn.execute(
                    text("UPDATE users SET avatar=:a WHERE id=:id"),
                    {"a": new_avatar_url, "id": st.session_state.user["id"]}
                )
            st.session_state.user["avatar"] = new_avatar_url
            st.success("✅ Avatar đã được cập nhật!")
            st.rerun()
    if st.sidebar.button("🚪 Đăng xuất"):
        st.session_state.user = None
        st.rerun()

# ====== Các hàm gợi ý món ăn ======
def get_recommendations(ingredient_query, top_k=5):
    query_embedding = model.encode(ingredient_query).tolist()
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, ten_mon, anh, video, url, nguyen_lieu, cach_lam,
                       1 - (embedding <=> (:query_embedding)::vector) AS similarity
                FROM recipes
                ORDER BY embedding <=> (:query_embedding)::vector
                LIMIT :top_k
            """),
            {"query_embedding": query_embedding, "top_k": top_k}
        )
        return result.fetchall()

def get_recommendations_by_name(name_query, top_k=5):
    query_embedding = model.encode(name_query).tolist()
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, ten_mon, anh, video, url, nguyen_lieu, cach_lam,
                       1 - (embedding_name <=> (:query_embedding)::vector) AS similarity
                FROM recipes
                ORDER BY embedding_name <=> (:query_embedding)::vector
                LIMIT :top_k
            """),
            {"query_embedding": query_embedding, "top_k": top_k}
        )
        return result.fetchall()

def get_random_recipes(top_k=5):
    with engine.connect() as conn:
        max_id = conn.execute(text("SELECT MAX(id) FROM recipes")).scalar()
        random_ids = [random.randint(1, max_id) for _ in range(top_k)]
        result = conn.execute(
            text("""
                SELECT id, ten_mon, anh, video, url, nguyen_lieu, cach_lam, 1 AS similarity
                FROM recipes
                WHERE id = ANY(:ids)
            """),
            {"ids": random_ids}
        )
        return result.fetchall()

# ====== Giao diện chính ======
st.image("data/Food_Banner_1.jpg", width="stretch")

st.sidebar.title("🍴 Sở thích của bạn")
search_mode = st.sidebar.radio("Bạn muốn tìm món ăn theo?", ["Nguyên liệu", "Tên món"])

st.title("🍲 Gợi ý nấu ăn bằng AI")
st.write("Khám phá món ăn phù hợp bằng cách sử dụng AI và tìm tương đồng vector!")

st.markdown(
    "<h2 style='color:#27AE60; font-size:28px; font-weight:bold; margin-bottom:15px;'>🔍 Tìm kiếm món ăn</h2>",
    unsafe_allow_html=True
)

col_input1, col_input2 = st.columns([1, 3])
with col_input1:
    if search_mode == "Nguyên liệu":
        st.markdown("<p style='text-align:right; font-size:20px; font-weight:bold;'>Nhập nguyên liệu bạn đang có:</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:right; font-size:20px; font-weight:bold;'>Nhập tên món ăn bạn cần tìm:</p>", unsafe_allow_html=True)

with col_input2:
    if search_mode == "Nguyên liệu":
        query = st.text_input("", placeholder="Ví dụ: gà, hành, ớt, tỏi", label_visibility="collapsed")
    else:
        query = st.text_input("", placeholder="Ví dụ: phở bò, gỏi cuốn, bún chả", label_visibility="collapsed")

col_slider1, col_slider2 = st.columns([1, 3])
with col_slider1:
    st.markdown("<p style='text-align:right; font-weight:bold;'>Số lượng món ăn bạn muốn gợi ý:</p>", unsafe_allow_html=True)

with col_slider2:
    top_k = st.slider("", 3, 10, 5, label_visibility="collapsed")
    if st.button("🔍 Gợi ý món ăn"):
        if query.strip() == "":
            st.warning("⚠️ Vui lòng nhập ít nhất 1 nguyên liệu hoặc tên món.")
        else:
            if search_mode == "Nguyên liệu":
                st.session_state.results = get_recommendations(query, top_k=top_k)
            else:
                st.session_state.results = get_recommendations_by_name(query, top_k=top_k)

col1, col2 = st.columns([3, 1])

with col1:
    daily_recipes = get_random_recipes(top_k=5)

    if "results" in st.session_state and st.session_state.results:
        st.markdown("<h2 style='color:#27AE60; font-size:28px; font-weight:bold;'>🍽️ Món ăn gợi ý cho bạn</h2>", unsafe_allow_html=True)
        for row in st.session_state.results:
            with st.container():
                st.subheader(f"{row.ten_mon}  (⭐ {row.similarity:.2f})")
                cols = st.columns([1, 2])

                with cols[0]:
                    if row.anh:
                        st.image(row.anh, width="stretch")
                    if row.video and "youtube" in row.video:
                        st.video(row.video)

                with cols[1]:
                    st.markdown(f"**Nguyên liệu:** {row.nguyen_lieu}")
                    st.markdown(f"**Cách làm:** {row.cach_lam}")
                    if row.url:
                        st.markdown(f"[🔗 Xem chi tiết]({row.url})")

                st.markdown("---")

    if daily_recipes:
        st.markdown("<h2 style='color:#27AE60; font-size:28px; font-weight:bold;'>🍴 Món ăn ngày mới dành cho bạn</h2>", unsafe_allow_html=True)
        for row in daily_recipes:
            with st.container():
                st.subheader(row.ten_mon)
                cols = st.columns([1, 2])

                with cols[0]:
                    if row.anh:
                        st.image(row.anh, width="stretch")
                    if row.video and "youtube" in row.video:
                        st.video(row.video)

                with cols[1]:
                    st.markdown(f"**Nguyên liệu:** {row.nguyen_lieu}")
                    st.markdown(f"**Cách làm:** {row.cach_lam}")
                    if row.url:
                        st.markdown(f"[🔗 Xem chi tiết]({row.url})")

                st.markdown("---")

with col2:
    st.markdown("### 💡 Mẹo")
    st.info("""
        - Cụ thể với nguyên liệu bạn có  
        - Kết hợp nhiều cách chế biến  
        - Thử phong cách mới  
        - Tìm món ngẫu nhiên để lấy cảm hứng  
        - Có thể tìm theo tên món trực tiếp
        """)

    st.markdown("### 📊 Thống kê cơ sở dữ liệu")
    st.metric("Món ăn có sẵn", "2400+")
    st.metric("Kết hợp nguyên liệu", "∞")
    st.metric("Độ chính xác AI", "90%+")