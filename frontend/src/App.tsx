import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Operations from "./pages/Operations";
import Maintenance from "./pages/Maintenance";
import LiveLogs from "./pages/LiveLogs";
import Analytics from "./pages/Analytics";
import Login from "./pages/Login";
import WorkerForms from "./pages/WorkerForms";
import "./App.css";

type Tab = "dashboard" | "operations" | "maintenance" | "logs" | "analytics";

function App() {
  const [loggedIn, setLoggedIn] = useState(
  localStorage.getItem("biw_logged_in") === "true"
  );
  const [activeTab, setActiveTab] = useState<Tab>("dashboard");
  const isWorkerPage=window.location.pathname === "/worker";
  if (isWorkerPage){
    return <WorkerForms />
  }
  if (!loggedIn) {
  return <Login onLogin={() => setLoggedIn(true)} />;
  }

  return (
    <div className="app-shell">
      <nav className="top-nav">
        <div className="brand">
          <h2>BIW Digital Twin</h2>
          <span>Shop Floor Monitoring System</span>
        </div>

        <div className="nav-tabs">
          <button className={activeTab === "dashboard" ? "active" : ""} onClick={() => setActiveTab("dashboard")}>
            Dashboard
          </button>

          <button className={activeTab === "operations" ? "active" : ""} onClick={() => setActiveTab("operations")}>
            Operations
          </button>

          <button className={activeTab === "maintenance" ? "active" : ""} onClick={() => setActiveTab("maintenance")}>
            Maintenance
          </button>

          <button className={activeTab === "logs" ? "active" : ""} onClick={() => setActiveTab("logs")}>
            Live Logs
          </button>

          <button className={activeTab === "analytics" ? "active" : ""} onClick={() => setActiveTab("analytics")}>
            Analytics
          </button>

          <button className="nav-btn" onClick={()=>{localStorage.removeItem("biw_logged_in"); localStorage.removeItem("biw_username"); setLoggedIn(false);}}>Logout</button>
               
        </div>
      </nav>

      {activeTab === "dashboard" && <Dashboard />}
      {activeTab === "operations" && <Operations />}
      {activeTab === "maintenance" && <Maintenance />}

      {activeTab === "logs" && <LiveLogs />}
        
      {activeTab === "analytics" && <Analytics />}
    </div>
  );
}

export default App;