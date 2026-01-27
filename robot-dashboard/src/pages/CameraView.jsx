import React from "react";

// export default function CameraView() {
//   return (
//     <div>
//       <h1 className="text-2xl font-bold mb-4">Live Camera</h1>
//       <img src="/api/camera/stream" alt="Robot Camera" className="border" />
//     </div>
//   );
// }

export default function CameraView() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Live Camera</h1>

      <div className="border rounded overflow-hidden">
        <img
          src="http://localhost:8001/camera"
          alt="Robot Camera"
          className="w-full"
        />
      </div>
    </div>
  );
}
