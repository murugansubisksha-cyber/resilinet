function Incidents() {
  const incidents = [
    {
      id: "INC-001",
      type: "Landslide",
      location: "NH-6, Assam",
      risk: "High",
      status: "Active",
      reported: "Today, 10:30 AM",
    },
    {
      id: "INC-002",
      type: "Flood",
      location: "Barak Valley",
      risk: "Medium",
      status: "Monitoring",
      reported: "Today, 9:15 AM",
    },
    {
      id: "INC-003",
      type: "Road Block",
      location: "Imphal Road",
      risk: "High",
      status: "Active",
      reported: "Yesterday, 6:40 PM",
    },
  ];

  return (
    <div>
      <h1 className="page-title">⚠️ Incident Management</h1>

      <p className="page-subtitle">
        Monitor reported road disruptions and emergency incidents
      </p>

      <div className="incident-grid">
        {incidents.map((incident) => (
          <div className="incident-card" key={incident.id}>
            <h2>{incident.type}</h2>

            <p>
              <strong>Incident ID:</strong> {incident.id}
            </p>

            <p>
              <strong>📍 Location:</strong> {incident.location}
            </p>

            <p>
              <strong>⚠️ Risk Level:</strong> {incident.risk}
            </p>

            <p>
              <strong>Status:</strong> {incident.status}
            </p>

            <p>
              <strong>🕒 Reported:</strong> {incident.reported}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Incidents;