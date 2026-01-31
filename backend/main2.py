# uvicorn combined_server:app --host 0.0.0.0 --port 8000
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from robot_controller import RobotController
from picamera2 import Picamera2
import cv2
import threading
import time
import atexit

app = FastAPI()
robot = RobotController()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Robot models ---
class Command(BaseModel):
    action: str

class Speed(BaseModel):
    speed: int

@app.post("/command")
def send_command(cmd: Command):
    robot.command(cmd.action)
    return {"ok": True}

@app.post("/speed")
def set_speed(spd: Speed):
    robot.set_speed(spd.speed)
    return {"ok": True, "speed": spd.speed}

@app.get("/status")
def get_status():
    return robot.status()

# --- Camera setup ---
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (320, 240), "format": "RGB888"})
picam2.configure(config)
picam2.start()

atexit.register(picam2.stop)

frame = None
lock = threading.Lock()

def capture_frames():
    global frame
    while True:
        img = picam2.capture_array()
        _, jpeg = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        with lock:
            frame = jpeg.tobytes()
        time.sleep(0.03)  # ~30 FPS

threading.Thread(target=capture_frames, daemon=True).start()

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

@app.on_event("shutdown")
def shutdown():
    robot.shutdown()
    picam2.stop()
