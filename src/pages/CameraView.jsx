import React from "react";

export default function CameraView() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Live Camera</h1>
      <img src="/api/camera/stream" alt="Robot Camera" className="border" />
    </div>
  );
}