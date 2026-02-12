#!/usr/bin/env python3

from ultralytics import YOLO
import cv2
import time
import sys
from pathlib import Path

# ----------------------------
# Config
# ----------------------------
MODEL_PATH = "models/yolov8n.pt"   # auto-downloads if not present
IMAGE_PATH = "snapshot.jpg"     # image to run inference on
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



# import cv2
# import time

# # Open the default camera (usually /dev/video0)
# cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)


# if not cap.isOpened():
#     print("❌ Failed to open camera.")
# else:
#     ret, frame = cap.read()
#     if ret:
#         filename = f"snapshot_{int(time.time())}.jpg"
#         cv2.imwrite(filename, frame)
#         print(f"📸 Saved image as {filename}")
#     else:
#         print("⚠️ Failed to capture image.")

# cap.release()

# from picamera2 import Picamera2, Preview
# from time import sleep

# picam2 = Picamera2()

# # Set up the configuration once
# camera_config = picam2.create_preview_configuration()
# picam2.configure(camera_config)

# def live_video():
#     picam2.start_preview(Preview.QTGL)  # Show video window (requires X11)
#     picam2.start()
#     sleep(5)
#     picam2.stop_preview()
#     picam2.stop()

# def capture_image():
#     picam2.start()
#     sleep(2)  # Let camera warm up
#     picam2.capture_file("test_image.jpg")
#     picam2.stop()

# capture_image()
# picam2.close()

# from picamera2 import Picamera2
# import cv2

# picam2 = Picamera2()
# picam2.start()

# frame = picam2.capture_array()  # returns a NumPy array
# cv2.imwrite("snapshot.jpg", frame)
# print("Saved snapshot.jpg")

# picam2.stop()
# picam2.close()
