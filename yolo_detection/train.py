from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data=r"C:\Users\samli\Desktop\SAM\GIHUB\ARDUINO_ESP32\yolo_detection\dataset.yaml",
    epochs=10,
    imgsz=640
)