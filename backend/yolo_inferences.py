#uvicorn yolo_inferences:app --host 0.0.0.0 --port 8001
from ultralytics import YOLO
import cv2
import time
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from picamera2 import Picamera2
import threading
import atexit

app = FastAPI()

# --- CORS (allow React frontend to connect) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Camera setup ---
picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (320, 240), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

# Clean shutdown
atexit.register(picam2.stop)

frame = None
lock = threading.Lock()

# Load model
print("[INFO] Loading YOLOv8n model...")
model = YOLO("yolov8n.pt")

# Force CPU (important on Pi)
model.to("cpu")


def run_inference(image):
    if image is None:
        print(f"[ERROR] Could not load image: {image}")
        sys.exit(1)

    print("[INFO] Running inference...")
    start = time.time()

    results = model(
        image,
        imgsz=240,
        conf=.4,
        verbose=False
    )

    elapsed = (time.time() - start) * 1000
    print(f"[INFO] Inference time: {elapsed:.2f} ms")

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

    return annotated


# --- Frame capture thread ---
def capture_frames():
    global frame
    while True:
        img = picam2.capture_array()
        img = run_inference(img)
        _, jpeg = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        with lock:
            frame = jpeg.tobytes()
        time.sleep(0.03)  # ~30 FPS

threading.Thread(target=capture_frames, daemon=True).start()

# --- MJPEG stream ---
def mjpeg_stream():
    while True:
        with lock:
            if frame is None:
                continue
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                frame +
                b"\r\n"
            )

@app.get("/camera")
def camera():
    return StreamingResponse(
        mjpeg_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
