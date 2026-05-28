from ultralytics import YOLO
import os
from collections import Counter

model = YOLO(r"runs\detect\train4\weights\best.pt")

input_folder = "data/captured_images"
output_folder = "data/detected_images"

os.makedirs(output_folder, exist_ok=True)

files = os.listdir(input_folder)

counter = Counter()

if not files:
    print("沒有圖片")
    exit()

for f in files:
    path = os.path.join(input_folder, f)

    print("正在辨識:", f)

    results = model(path)

    # 存框圖
    save_path = os.path.join(output_folder, f)
    results[0].save(filename=save_path)

    # 統計
    names = model.names
    boxes = results[0].boxes

    for box in boxes:
        cls_id = int(box.cls[0])
        label = names[cls_id]
        counter[label] += 1

# 存統計
with open("result.txt", "w", encoding="utf-8") as f:
    for k, v in counter.items():
        f.write(f"{k}:{v}\n")

print("完成")