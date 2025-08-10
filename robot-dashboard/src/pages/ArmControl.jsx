import React from "react";

export default function ArmControl() {
  const sendArmCommand = (action) => {
    fetch(`/api/arm/${action}`, { method: "POST" });
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Arm Control</h1>
      <div className="flex gap-4">
        <button onClick={() => sendArmCommand("up")} className="bg-blue-500 text-white p-2 rounded">Up</button>
        <button onClick={() => sendArmCommand("down")} className="bg-blue-500 text-white p-2 rounded">Down</button>
        <button onClick={() => sendArmCommand("open")} className="bg-green-500 text-white p-2 rounded">Open</button>
        <button onClick={() => sendArmCommand("close")} className="bg-red-500 text-white p-2 rounded">Close</button>
      </div>
    </div>
  );
}