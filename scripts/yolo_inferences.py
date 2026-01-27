#!/usr/bin/env python3

from ultralytics import YOLO
import cv2
import time
import sys
from pathlib import Path

# ----------------------------
# Config
# ----------------------------
MODEL_PATH = "yolov8n.pt"   # auto-downloads if not present
IMAGE_PATH = "test_image.jpg"     # image to run inference on
IMG_SIZE = 480              # good balance for Pi 5
CONF_THRESH = 0.4

# ----------------------------
# Load model
# ----------------------------
print("[INFO] Loading YOLOv8n model...")
model = YOLO(MODEL_PATH)

# Force CPU (important on Pi)
model.to("cpu")

# ----------------------------
# Load image
# ----------------------------
image = cv2.imread(IMAGE_PATH)
if image is None:
    print(f"[ERROR] Could not load image: {IMAGE_PATH}")
    sys.exit(1)

# ----------------------------
# Run inference
# ----------------------------
print("[INFO] Running inference...")
start = time.time()

results = model(
    image,
    imgsz=IMG_SIZE,
    conf=CONF_THRESH,
    verbose=False
)

elapsed = (time.time() - start) * 1000
print(f"[INFO] Inference time: {elapsed:.2f} ms")

# ----------------------------
# Process detections
# ----------------------------
annotated = image.copy()

for r in results:
    boxes = r.boxes
    if boxes is None:
        continue

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        label = f"{model.names[cls]} {conf:.2f}"

        # Draw box
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw label
        cv2.putText(
            annotated,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

# ----------------------------
# Show result
# ----------------------------
# cv2.imshow("YOLOv8n Detection", annotated)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
cv2.imwrite("yolov8n_detection.jpg", annotated)
