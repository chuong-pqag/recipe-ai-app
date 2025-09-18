
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import pandas as pd

# 1. Load model gốc
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Đọc dữ liệu
df = pd.read_csv("data/nguyen_lieu_sach2.csv")

# 3. Tạo dữ liệu huấn luyện (Nguyen_lieu → Ten_mon)
train_examples = [
    InputExample(texts=[row["Nguyen_lieu"], row["Ten_mon"]], label=1.0)
    for _, row in df.iterrows()
]

# 4. Tạo DataLoader & Loss
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)

# 5. Huấn luyện
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3,                # số lần lặp qua toàn bộ dữ liệu
    warmup_steps=100,        # giúp model ổn định lúc đầu
    show_progress_bar=True
)

# 6. Lưu model đã fine-tune
model.save("my_recipe_model")
print("✅ Huấn luyện xong! Model đã lưu tại: my_recipe_model/")
