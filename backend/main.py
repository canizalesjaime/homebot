#uvicorn main:app --host 0.0.0.0 --port 8000
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from robot_controller import RobotController

app = FastAPI()
robot = RobotController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_methods=["*"],
    allow_headers=["*"],
)

class Command(BaseModel):
    action: str

@app.post("/command")
def send_command(cmd: Command):
    robot.command(cmd.action)
    return {"ok": True}

@app.get("/status")
def get_status():
    return robot.status()

@app.on_event("shutdown")
def shutdown():
    robot.shutdown()
