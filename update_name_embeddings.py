import os
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load biến môi trường (DB_URL từ .env hoặc st.secrets)
load_dotenv()
DB_URL = os.getenv("DB_URL") or os.getenv("DATABASE_URL")

if not DB_URL:
    raise ValueError("❌ Không tìm thấy DB_URL trong .env")

# Kết nối database
engine = create_engine(DB_URL)

# Load model embedding
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Lấy danh sách id + ten_mon
with engine.connect() as conn:
    rows = conn.execute(text("SELECT id, ten_mon FROM recipes WHERE embedding_name IS NULL")).fetchall()

print(f"🔄 Tìm thấy {len(rows)} món ăn cần cập nhật embedding...")

# Cập nhật từng dòng
with engine.begin() as conn:  # begin() để auto commit
    for row in rows:
        embedding = model.encode(row.ten_mon).tolist()
        conn.execute(
            text("UPDATE recipes SET embedding_name = :embedding WHERE id = :id"),
            {"embedding": embedding, "id": row.id}
        )

print("✅ Hoàn thành cập nhật embedding cho tên món.")
