import React from "react";

const convoys = [
  {
    id: "CV-101",
    route: "Guwahati → Shillong",
    vehicle_count: 8,
    average_speed: 42,
    progress: 75,
    current_risk: "Low",
  },
  {
    id: "CV-102",
    route: "Imphal → Kohima",
    vehicle_count: 5,
    average_speed: 35,
    progress: 45,
    current_risk: "Medium",
  },
  {
    id: "CV-103",
    route: "Silchar → Aizawl",
    vehicle_count: 10,
    average_speed: 28,
    progress: 25,
    current_risk: "High",
  },
];

function Convoys() {
  return (
    <div className="convoys-page">
      <h1>🚚 Convoy Monitoring</h1>

      <p className="page-description">
        Monitor active vehicles and convoy movement in real time.
      </p>

      <div className="convoy-grid">
        {convoys.map((convoy) => (
          <div className="convoy-card" key={convoy.id}>
            
            <h3>🚚 Convoy {convoy.id}</h3>

            <p>
              <strong>🛣 Route:</strong> {convoy.route}
            </p>

            <p>
              <strong>🚛 Vehicles:</strong> {convoy.vehicle_count}
            </p>

            <p>
              <strong>⚡ Speed:</strong> {convoy.average_speed} km/h
            </p>

            <p>
              <strong>⚠️ Current Risk:</strong>{" "}
              <span className={`risk ${convoy.current_risk.toLowerCase()}`}>
                {convoy.current_risk}
              </span>
            </p>

            <p>
              <strong>📍 Journey Progress:</strong>{" "}
              {convoy.progress}%
            </p>

            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${convoy.progress}%`,
                }}
              ></div>
            </div>

            {convoy.current_risk === "High" && (
              <div className="reroute-alert">
                ⚠️ High route risk detected!
                <br />

                <button>Accept Reroute</button>
              </div>
            )}

          </div>
        ))}
      </div>
    </div>
  );
}

export default Convoys;