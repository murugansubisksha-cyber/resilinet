function Sidebar() {
  return (
    <div
      style={{
        width: "220px",
        minHeight: "100vh",
        borderRight: "1px solid #ccc",
        padding: "20px",
      }}
    >
      <h2>🚚 ResiliNet</h2>

      <hr />

      <p>🏠 Dashboard</p>
      <p>🗺️ Network Map</p>
      <p>🚛 Convoys</p>
      <p>📸 Incidents</p>
      <p>🛣️ Route Comparison</p>
      <p>📱 Field Report</p>
    </div>
  );
}

export default Sidebar;