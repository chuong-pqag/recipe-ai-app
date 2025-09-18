import os
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

# Load model embedding
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_recommendations(ingredient_query, top_k=5):
    engine = create_engine(DB_URL)

    # Tạo embedding cho nguyên liệu người dùng nhập
    query_embedding = model.encode(ingredient_query).tolist()

    # Truy vấn nearest neighbor trong Postgres với pgvector
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, ten_mon, url, nguyen_lieu,
                       1 - (embedding <=> (:query_embedding)::vector) AS similarity
                FROM recipes
                ORDER BY embedding <=> (:query_embedding)::vector
                LIMIT :top_k
            """),
            {"query_embedding": query_embedding, "top_k": top_k}
        )
        return result.fetchall()

if __name__ == "__main__":
    print("👉 Nhập nguyên liệu bạn có sẵn (ví dụ: 'mì, kim chi, phô mai'):")
    user_input = input("Nguyên liệu: ")

    results = get_recommendations(user_input, top_k=5)

    print("\n🎯 Gợi ý món ăn:")
    for row in results:
        print(f"- {row.ten_mon} ({row.similarity:.2f})")
        print(f"  Nguyên liệu: {row.nguyen_lieu}")
        print(f"  Xem chi tiết: {row.url}\n")