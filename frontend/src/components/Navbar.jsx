import { useLocation, useNavigate } from "react-router-dom";
import {
  Bell,
  Search,
  Plus,
} from "lucide-react";

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const pathName = location.pathname;

  const getPageName = () => {
    const routes = {
      "/": "Dashboard",
      "/network-map": "Network Map",
      "/convoys": "Convoys",
      "/incidents": "Incidents",
      "/route-comparison": "Route Comparison",
      "/field-report": "Field Report",
      "/ai-insights": "AI Insights",
      "/smart-alerts": "Smart Alerts",
    };

    return routes[pathName] || "Dashboard";
  };

  return (
    <header className="navbar">

      <div className="breadcrumb">
        <span>ResiliNet</span>
        <span>/</span>
        <strong>{getPageName()}</strong>
      </div>


      <div className="navbar-actions">

        <div className="global-search">

          <Search size={18} />

          <input
            placeholder="Search road, segment or incident..."
          />

        </div>


        <button
          className="report-button"
          onClick={() =>
            navigate("/field-report")
          }
        >
          <Plus size={18} />
          Report Hazard
        </button>


        <button className="alert-button">

          <Bell size={20} />

          <span className="alert-count">
            3
          </span>

        </button>

      </div>

    </header>
  );
}

export default Navbar;