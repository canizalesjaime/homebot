import React from "react";

export default function MotionControl() {
  const sendCommand = (direction) => {
    fetch(`/api/motion/${direction}`, { method: "POST" });
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Motion Control</h1>
      <div className="grid grid-cols-3 gap-4 w-48 mx-auto">
        <button onClick={() => sendCommand("forward")} className="bg-green-500 text-white p-2 rounded">↑</button>
        <button onClick={() => sendCommand("left")} className="bg-yellow-500 text-white p-2 rounded">←</button>
        <button onClick={() => sendCommand("right")} className="bg-yellow-500 text-white p-2 rounded">→</button>
        <button onClick={() => sendCommand("backward")} className="bg-red-500 text-white p-2 rounded col-span-3">↓</button>
      </div>
    </div>
  );
}