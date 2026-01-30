import React from "react";
import CameraView from "./CameraView";

export default function MotionControl() {
  const [speed, setSpeed] = React.useState("");

  const sendCommand = (action) => {
    fetch("http://192.168.1.156:8000/command", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ action }),
    });
  };

  const changeSpeed = () => {
    const value = Number(speed);

    if (value < 0 || value > 100 || isNaN(value)) {
      alert("Speed must be between 0 and 100");
      return;
    }

    fetch("http://192.168.1.156:8000/speed", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ speed: value }),
    });
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Motion Control</h1>

      {/* Speed control */}
      <div className="flex items-center gap-2 mt-4 justify-center">
        <input
          type="number"
          min="0"
          max="100"
          value={speed}
          onChange={(e) => setSpeed(e.target.value)}
          className="border rounded px-2 py-1 w-20 text-center"
          placeholder="0-100"
        />

        <button
          onClick={changeSpeed}
          className="bg-blue-500 text-white px-3 py-1 rounded"
        >
          Change Speed
        </button>
      </div>

      {/* Motion buttons */}
      <div className="grid grid-cols-3 gap-4 w-48 mx-auto">
        <button
          onMouseDown={() => sendCommand("forward")}
          onMouseUp={() => sendCommand("stop")}
          className="bg-green-500 text-white p-2 rounded"
        >
          ↑
        </button>

        <button
          onMouseDown={() => sendCommand("left")}
          onMouseUp={() => sendCommand("stop")}
          className="bg-yellow-500 text-white p-2 rounded"
        >
          ←
        </button>

        <button
          onMouseDown={() => sendCommand("right")}
          onMouseUp={() => sendCommand("stop")}
          className="bg-yellow-500 text-white p-2 rounded"
        >
          →
        </button>

        <button
          onMouseDown={() => sendCommand("backward")}
          onMouseUp={() => sendCommand("stop")}
          className="bg-red-500 text-white p-2 rounded col-span-3"
        >
          ↓
        </button>
      </div>

      <CameraView />
    </div>
  );
}
