import { useState } from "react";

function SmartAlerts() {
  const [alerts, setAlerts] = useState([
    {
      id: 1,
      type: "Landslide Warning",
      location: "NH-15, Hill Section",
      severity: "High",
      status: "Active",
      recommendation:
        "Avoid this route and redirect convoys through an alternative route.",
    },
    {
      id: 2,
      type: "Heavy Rainfall",
      location: "Upper Assam Region",
      severity: "Medium",
      status: "Active",
      recommendation:
        "Monitor weather conditions before dispatching logistics vehicles.",
    },
    {
      id: 3,
      type: "Road Blockage",
      location: "Mountain Route B",
      severity: "High",
      status: "Active",
      recommendation:
        "Stop convoy movement until the road accessibility is restored.",
    },
    {
      id: 4,
      type: "Flood Risk",
      location: "River Crossing Area",
      severity: "Low",
      status: "Active",
      recommendation:
        "Use caution and continuously monitor water levels.",
    },
  ]);

  const [filter, setFilter] = useState("All");

  const resolveAlert = (id) => {
    setAlerts(
      alerts.map((alert) =>
        alert.id === id
          ? { ...alert, status: "Resolved" }
          : alert
      )
    );
  };

  const filteredAlerts =
    filter === "All"
      ? alerts
      : alerts.filter((alert) => alert.severity === filter);

  const activeAlerts = alerts.filter(
    (alert) => alert.status === "Active"
  ).length;

  const resolvedAlerts = alerts.filter(
    (alert) => alert.status === "Resolved"
  ).length;

  return (
    <div className="alerts-page">
      <h1>🚨 Smart Alerts & Emergency Response</h1>

      <p className="alerts-subtitle">
        Real-time risk alerts and recommended actions for safer logistics.
      </p>

      {/* Summary Cards */}

      <div className="alert-summary">

        <div className="summary-card">
          <h3>🚨 Active Alerts</h3>
          <p>{activeAlerts}</p>
        </div>

        <div className="summary-card">
          <h3>✅ Resolved Alerts</h3>
          <p>{resolvedAlerts}</p>
        </div>

        <div className="summary-card">
          <h3>📊 Total Alerts</h3>
          <p>{alerts.length}</p>
        </div>

      </div>

      {/* Filter */}

      <div className="alert-filter">
        <label>Filter by Severity:</label>

        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        >
          <option value="All">All Alerts</option>
          <option value="High">High Risk</option>
          <option value="Medium">Medium Risk</option>
          <option value="Low">Low Risk</option>
        </select>
      </div>

      {/* Alerts */}

      <div className="alerts-container">

        {filteredAlerts.map((alert) => (
          <div
            className={`alert-card ${
              alert.status === "Resolved"
                ? "resolved-alert"
                : ""
            }`}
            key={alert.id}
          >
            <div className="alert-header">

              <h2>⚠️ {alert.type}</h2>

              <span
                className={`severity ${alert.severity.toLowerCase()}`}
              >
                {alert.severity} Risk
              </span>

            </div>

            <p>
              <strong>📍 Location:</strong>{" "}
              {alert.location}
            </p>

            <p>
              <strong>📌 Status:</strong>{" "}
              {alert.status}
            </p>

            <div className="alert-recommendation">

              <strong>🤖 AI Recommendation:</strong>

              <p>{alert.recommendation}</p>

            </div>

            {alert.status === "Active" && (
              <button
                className="resolve-button"
                onClick={() => resolveAlert(alert.id)}
              >
                Mark as Resolved
              </button>
            )}

          </div>
        ))}

      </div>
    </div>
  );
}

export default SmartAlerts;