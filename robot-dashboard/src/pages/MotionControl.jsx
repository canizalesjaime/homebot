import React from "react";

export default function MotionControl() {
  const sendCommand = (action) => {
    fetch("http://localhost:8000/command", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ action }),
    });
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Motion Control</h1>

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
    </div>
  );
}
