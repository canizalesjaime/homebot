import React from "react";

export default function CameraView() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Live Camera</h1>

      <div className="border rounded overflow-hidden">
        <img
          src="http://192.168.1.156:8000/camera"
          alt="Robot Camera"
          className="w-full"
        />
      </div>
    </div>
  );
}
