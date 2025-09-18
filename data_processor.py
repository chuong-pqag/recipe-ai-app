import pandas as pd
from sentence_transformers import SentenceTransformer

def load_and_process(csv_path="data/nguyen_lieu_sach2.csv"):
    """
    Đọc file CSV, chuẩn hóa dữ liệu và sinh embedding cho cột Nguyen_lieu.
    Trả về DataFrame có thêm cột 'embedding'.
    """
    # Đọc dữ liệu từ CSV
    df = pd.read_csv(csv_path)

    # Điền giá trị rỗng nếu có ô bị NaN
    df = df.fillna("")

    # Khởi tạo model embedding (sử dụng model đã fine-tune)
    model = SentenceTransformer("my_recipe_model")  # <--- Thay đổi ở đây

    # Sinh embedding từ cột Nguyen_lieu
    print("🔄 Đang sinh embedding cho nguyên liệu (dùng model fine-tune)...")
    embeddings = model.encode(df["Nguyen_lieu"].tolist())

    # Gắn embedding vào DataFrame
    df["embedding"] = embeddings.tolist()

    print(f"✅ Đã xử lý {len(df)} món ăn với model fine-tune.")
    return df

if __name__ == "__main__":
    df = load_and_process()
    print(df.head())