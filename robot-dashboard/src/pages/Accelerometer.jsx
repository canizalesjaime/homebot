import React, { useState, useEffect } from "react";

export default function Accelerometer() {
  const [data, setData] = useState({ x: 0, y: 0, z: 0 });

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://192.168.1.156:8000/accelerometer")
        .then((res) => res.json())
        .then(setData);
    }, 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Accelerometer Data</h1>
      <p>X: {data.x}</p>
      <p>Y: {data.y}</p>
      <p>Z: {data.z}</p>
    </div>
  );
}