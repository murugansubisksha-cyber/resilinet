import { Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import NetworkMap from "./pages/NetworkMap";
import Convoys from "./pages/Convoys";
import Incidents from "./pages/Incidents";

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
        </Routes>
      </main>
    </div>
  );
}

export default App;