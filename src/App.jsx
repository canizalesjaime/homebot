import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import MotionControl from "./pages/MotionControl";
import ArmControl from "./pages/ArmControl";
import Accelerometer from "./pages/Accelerometer";
import CameraView from "./pages/CameraView";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <div className="p-4">
        <Routes>
          <Route path="/" element={<MotionControl />} />
          <Route path="/arm" element={<ArmControl />} />
          <Route path="/accelerometer" element={<Accelerometer />} />
          <Route path="/camera" element={<CameraView />} />
        </Routes>
      </div>
    </div>
  );
}