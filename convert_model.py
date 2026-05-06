"""
Run this script once to convert YOLOv8n to TFLite.
Requirements: pip install ultralytics
Output: yolov8n_float32.tflite  (copy it to assets/models/)
"""
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.export(format='tflite', imgsz=320)
print("Done. Copy yolov8n_float32.tflite to assets/models/")
