import StatCard from "../components/StatCard";

function Dashboard() {
  return (
    <div>
      <h1>ResiliNet Command Center</h1>

      <div
        style={{
          display: "flex",
          gap: "15px",
          flexWrap: "wrap",
        }}
      >
        <StatCard title="Accessibility Score" value="85%" />

        <StatCard title="High Risk Roads" value="12" />

        <StatCard title="Active Incidents" value="5" />

        <StatCard title="Active Convoys" value="3" />
      </div>
    </div>
  );
}

export default Dashboard;