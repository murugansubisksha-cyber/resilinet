function Convoys() {
  const convoys = [
    {
      id: "CV-001",
      vehicle: "Truck 01",
      destination: "Silchar",
      status: "Moving",
      risk: "Low",
    },
    {
      id: "CV-002",
      vehicle: "Truck 02",
      destination: "Imphal",
      status: "Delayed",
      risk: "Medium",
    },
    {
      id: "CV-003",
      vehicle: "Medical Van",
      destination: "Guwahati",
      status: "Stopped",
      risk: "High",
    },
  ];

  return (
    <div>
      <h1 className="page-title">🚛 Convoy Management</h1>

      <p className="page-subtitle">
        Monitor vehicles and logistics movements
      </p>

      <div className="convoy-grid">
        {convoys.map((convoy) => (
          <div className="convoy-card" key={convoy.id}>
            <h2>{convoy.id}</h2>

            <p>
              <strong>Vehicle:</strong> {convoy.vehicle}
            </p>

            <p>
              <strong>Destination:</strong> {convoy.destination}
            </p>

            <p>
              <strong>Status:</strong> {convoy.status}
            </p>

            <p>
              <strong>Risk Level:</strong> {convoy.risk}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Convoys;