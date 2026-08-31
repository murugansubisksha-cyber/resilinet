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
        
        <div className="menu-item">🛣️ Route Comparison</div>
        <div className="menu-item">📱 Field Report</div>
      </nav>
    </aside>
  );
}

export default Sidebar;