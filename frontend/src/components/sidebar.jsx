import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <h2>🚚 ResiliNet</h2>

      <nav className="menu">
        <NavLink to="/" end>
          🏠 Dashboard
        </NavLink>

        <NavLink to="/map">
          🗺️ Network Map
        </NavLink>

        <NavLink to="/convoys">
          🚛 Convoys
        </NavLink>

        <NavLink to="/incidents">
           ⚠️ Incidents
        </NavLink>

        <NavLink to="/route-comparison">
           🛣️ Route Comparison
        </NavLink>

        <NavLink to="/field-report">
           📝 Field Report
        </NavLink>

        <NavLink to="/ai-insights">
          🤖 AI Insights
        </NavLink>
        
        <NavLink to="/smart-alerts">
          🔔 Smart Alerts
        </NavLink>

      </nav>
    </aside>
  );
}

export default Sidebar;