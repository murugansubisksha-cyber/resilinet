import {
  Routes,
  Route,
} from "react-router-dom";

import { Toaster } from "react-hot-toast";

import ProtectedRoute from "./components/ProtectedRoute";
import Sidebar from "./components/sidebar";
import Navbar from "./components/Navbar";

import Dashboard from "./pages/dashboard";
import NetworkMap from "./pages/NetworkMap";
import Convoys from "./pages/Convoys";
import Incidents from "./pages/incidents";
import RouteComparison from "./pages/RouteComparison";
import FieldReport from "./pages/FieldReport";
import AIInsights from "./pages/AIInsights";
import SmartAlerts from "./pages/SmartAlerts";
import Login from "./pages/login";


function Layout({ children }) {
  return (
    <div className="app-layout">

      <Sidebar />

      <div className="main-section">

        <Navbar />

        <main className="page-content">
          {children}
        </main>

      </div>

    </div>
  );
}


function App() {
  return (
    <>

      <Routes>

        <Route
          path="/login"
          element={<Login />}
        />


        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          }
        />


        <Route
          path="/network-map"
          element={
            <ProtectedRoute>
              <Layout>
                <NetworkMap />
              </Layout>
            </ProtectedRoute>
          }
        />


        <Route
          path="/convoys"
          element={
            <ProtectedRoute>
              <Layout>
                <Convoys />
              </Layout>
            </ProtectedRoute>
          }
        />


        <Route
          path="/incidents"
          element={
            <ProtectedRoute>
              <Layout>
                <Incidents />
              </Layout>
            </ProtectedRoute>
          }
        />


        <Route
          path="/route-comparison"
          element={
            <ProtectedRoute>
              <Layout>
                <RouteComparison />
              </Layout>
            </ProtectedRoute>
          }
        />


        <Route
          path="/field-report"
          element={
            <ProtectedRoute>
              <Layout>
                <FieldReport />
              </Layout>
            </ProtectedRoute>
          }
        />


        <Route
          path="/ai-insights"
          element={
            <ProtectedRoute>
              <Layout>
                <AIInsights />
              </Layout>
            </ProtectedRoute>
          }
        />


        <Route
          path="/smart-alerts"
          element={
            <ProtectedRoute>
              <Layout>
                <SmartAlerts />
              </Layout>
            </ProtectedRoute>
          }
        />

      </Routes>


      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: "#1E293B",
            color: "#F8FAFC",
          },
        }}
      />

    </>
  );
}

export default App;