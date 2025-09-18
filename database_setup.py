import os
import pandas as pd
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

# Hàm tạo kết nối và setup DB
def setup_db():
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        # Bật extension pgvector
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

        # Xoá bảng nếu tồn tại (để tránh conflict)
        conn.execute(text("DROP TABLE IF EXISTS recipes"))

        # Tạo bảng mới
        conn.execute(text("""
            CREATE TABLE recipes (
                id SERIAL PRIMARY KEY,
                ten_mon TEXT,
                anh TEXT,
                video TEXT,
                url TEXT,
                nguyen_lieu TEXT,
                cach_lam TEXT,
                embedding VECTOR(384)
            )
        """))
        conn.commit()
    print("✅ Database schema created")
    return engine

# Hàm nạp dữ liệu từ CSV
def insert_data(engine):
    # Load CSV
    df = pd.read_csv("data/nguyen_lieu_sach2.csv")

    # Load model sentence-transformers
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    with engine.connect() as conn:
        for _, row in df.iterrows():
            text_to_embed = f"{row['Ten_mon']} {row['Nguyen_lieu']} {row['Cach_lam']}"
            embedding = model.encode(text_to_embed).tolist()

            conn.execute(
                text("""
                    INSERT INTO recipes (ten_mon, anh, video, url, nguyen_lieu, cach_lam, embedding)
                    VALUES (:ten_mon, :anh, :video, :url, :nguyen_lieu, :cach_lam, :embedding)
                """),
                {
                    "ten_mon": row["Ten_mon"],
                    "anh": row["Anh"],
                    "video": row["Video"],
                    "url": row["URL"],
                    "nguyen_lieu": row["Nguyen_lieu"],
                    "cach_lam": row["Cach_lam"],
                    "embedding": embedding
                }
            )
        conn.commit()
    print("✅ Data inserted into recipes")

if __name__ == "__main__":
    engine = setup_db()
    insert_data(engine)
    print("🎉 Database setup completed")