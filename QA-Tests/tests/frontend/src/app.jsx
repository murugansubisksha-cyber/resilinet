import { Routes, Route } from "react-router-dom";

import Sidebar from "./components/sidebar";
import Dashboard from "./pages/Dashboard";
import NetworkMap from "./pages/NetworkMap";
import Convoys from "./pages/Convoys";
import Incidents from "./pages/Incidents";
import RouteComparison from "./pages/RouteComparison";
import FieldReport from "./pages/FieldReport";
import AIInsights from "./pages/AIInsights";
import SmartAlerts from "./pages/SmartAlerts";

function App() {
  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/map" element={<NetworkMap />} />
          <Route path="/convoys" element={<Convoys />} />
          <Route path="/incidents" element={<Incidents />} />
          <Route path="/route-comparison" element={<RouteComparison />} />
          <Route path="/field-report" element={<FieldReport />} />
          <Route path="/ai-insights" element={<AIInsights />} />
          <Route path="/smart-alerts" element={<SmartAlerts />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

