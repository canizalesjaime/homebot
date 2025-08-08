import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-blue-700 text-white p-4 flex gap-4">
      <Link to="/" className="hover:underline">Motion</Link>
      <Link to="/arm" className="hover:underline">Arm Motion</Link>
      <Link to="/accelerometer" className="hover:underline">Accelerometer</Link>
      <Link to="/camera" className="hover:underline">Camera</Link>
    </nav>
  );
}