import React, { useState, useEffect } from "react";

export default function Sensors() {
  const [data, setData] = useState({ x: 0, y: 0, z: 0 });
  const [lidar, setLidar] = useState({ distance: 0, strength: 0 });

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://192.168.1.156:8000/accelerometer")
        .then((res) => res.json())
        .then(setData);

      fetch("http://192.168.1.156:8000/lidar")
        .then((res) => res.json())
        .then(setLidar);

    }, 500);

    return () => clearInterval(interval);
  }, []);

  const rotateBase = async () => {
    await fetch("http://192.168.1.156:8000/rotate_base");
  };

  const stopBase = async () => {
    await fetch("http://192.168.1.156:8000/stop_base");
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Sensors Data</h1>
      <h2 className="text-2xl font-bold mb-4"> Accelerometer:</h2>
      <p>Roll: {data.x}</p>
      <p>Pitch: {data.y}</p>
      <p>Temp: {data.z}</p>

      <h2 className="text-2xl font-bold mb-4"> Lidar:</h2>
      <p className="mt-4">Distance: {lidar.distance} cm</p>
      <p>Strength: {lidar.strength}</p>

      <div className="mt-4 space-x-2">
        <button onClick={rotateBase} className="bg-blue-500 text-white px-4 py-2 rounded">
          Rotate Base
        </button>

        <button onClick={stopBase} className="bg-red-500 text-white px-4 py-2 rounded">
          Stop Base
        </button>
      </div>
    </div>
  );
}