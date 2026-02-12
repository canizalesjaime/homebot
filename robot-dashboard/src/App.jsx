import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import MotionControl from "./pages/MotionControl";
import ArmControl from "./pages/ArmControl";
import Accelerometer from "./pages/Accelerometer";

export default function App() {
  return (
    <div>
      <Navbar />
      <main className="pt-20 max-w-7xl mx-auto px-6">
        <Routes>
          <Route path="/" element={<MotionControl />} />
          <Route path="/arm" element={<ArmControl />} />
          <Route path="/accelerometer" element={<Accelerometer />} />
        </Routes>
      </main>
    </div>
  );
}
