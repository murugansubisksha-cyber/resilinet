import {
  LayoutDashboard,
  Map,
  Truck,
  AlertTriangle,
  Route,
  FileText,
  Brain,
  Bell,
  LogOut,
  Wifi,
} from "lucide-react";

import {
  NavLink,
  useNavigate,
} from "react-router-dom";

import { useAuth } from "../context/AuthContext";

function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const menuItems = [
    {
      name: "Dashboard",
      path: "/",
      icon: LayoutDashboard,
    },
    {
      name: "Network Map",
      path: "/network-map",
      icon: Map,
    },
    {
      name: "Convoys",
      path: "/convoys",
      icon: Truck,
    },
    {
      name: "Incidents",
      path: "/incidents",
      icon: AlertTriangle,
    },
    {
      name: "Route Comparison",
      path: "/route-comparison",
      icon: Route,
    },
    {
      name: "Field Report",
      path: "/field-report",
      icon: FileText,
    },
    {
      name: "AI Insights",
      path: "/ai-insights",
      icon: Brain,
    },
    {
      name: "Smart Alerts",
      path: "/smart-alerts",
      icon: Bell,
    },
  ];

  return (
    <aside className="sidebar">

      <div className="sidebar-logo">
        🚚 ResiliNet
      </div>


      <nav>

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `nav-item ${
                  isActive
                    ? "active"
                    : ""
                }`
              }
            >

              <Icon size={20} />

              <span>
                {item.name}
              </span>

            </NavLink>
          );
        })}

      </nav>


      <div className="sidebar-bottom">

        <div className="server-health">

          <Wifi size={16} />

          <span className="health-dot"></span>

          <span>
            Backend Connected
          </span>

        </div>


        <div className="user-card">

          <div className="avatar">
            {user?.email?.charAt(0)
              ?.toUpperCase() || "U"}
          </div>

          <div>

            <strong>
              {user?.email || "User"}
            </strong>

            <small>
              {user?.role}
            </small>

          </div>

        </div>


        <button
          className="logout-button"
          onClick={handleLogout}
        >

          <LogOut size={18} />

          Logout

        </button>

      </div>

    </aside>
  );
}

export default Sidebar;