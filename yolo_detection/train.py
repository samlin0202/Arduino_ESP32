from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data=r"C:\Users\samli\Desktop\YOLO\dataset\data.yaml",
    epochs=10,
    imgsz=640
)