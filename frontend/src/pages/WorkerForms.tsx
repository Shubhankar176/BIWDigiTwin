import { useState } from "react";
import Maintenance from "./Maintenance";

type WorkerTab = "select" | "breakdown" | "pm" | "loto";

export default function WorkerForms() {
  const [selectedForm, setSelectedForm] = useState<WorkerTab>("select");

  if (selectedForm === "breakdown") {
    return <Maintenance workerMode defaultTab="breakdown" />;
  }

  if (selectedForm === "pm") {
    return <Maintenance workerMode defaultTab="pm" />;
  }

  if (selectedForm === "loto") {
    return <Maintenance workerMode defaultTab="loto" />;
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-brand">
          <h1>BIW Worker Form</h1>
          <p>Select the form you want to fill</p>
        </div>

        <div className="login-form">
          <button onClick={() => setSelectedForm("breakdown")}>
            Breakdown Entry
          </button>

          <button onClick={() => setSelectedForm("pm")}>
            Preventive Maintenance
          </button>

          <button onClick={() => setSelectedForm("loto")}>
            LOTO Register
          </button>
        </div>
      </div>
    </div>
  );
}