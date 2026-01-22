#uvicorn camera_server:app --host 0.0.0.0 --port 8001
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from picamera2 import Picamera2
import cv2
import threading
import time
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
    main={"size": (640, 480), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

# Clean shutdown
atexit.register(picam2.stop)

frame = None
lock = threading.Lock()

# --- Frame capture thread ---
def capture_frames():
    global frame
    while True:
        img = picam2.capture_array()
        _, jpeg = cv2.imencode(".jpg", img)
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
