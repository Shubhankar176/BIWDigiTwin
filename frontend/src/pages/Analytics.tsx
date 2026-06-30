import { useEffect, useState } from "react";
import { api } from "../services/api";

type OEE = {
  line: string;
  availability_percent: number;
  performance_percent: number;
  quality_percent: number;
  oee_percent: number;
  downtime_min: number;
};

type Loss = {
  line: string;
  downtime_minutes: number;
  rejected_units: number;
};

type MaintenanceKpis = {
  total_breakdowns: number;
  total_repair_time_min: number;
  mttr_min: number;
  mtbf_min: number;
};

export default function Analytics() {
  const [oee, setOee] = useState<OEE[]>([]);
  const [losses, setLosses] = useState<Loss[]>([]);
  const [maintenanceKpis, setMaintenanceKpis] = useState<MaintenanceKpis | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchAnalytics = async () => {
    try {
      const [oeeRes, lossRes, maintenanceRes] = await Promise.all([
        api.get("/oee-summary"),
        api.get("/top-losses"),
        api.get("/maintenance-kpis"),
      ]);

      setOee(oeeRes.data.oee_summary || []);
      setLosses(lossRes.data.top_losses || []);
      setMaintenanceKpis(maintenanceRes.data);
    } catch (error) {
      console.error(error);
      alert("Failed to load analytics");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setTimeout(() => {
      fetchAnalytics();
    }, 0);
  }, []);

  return (
    <div className="operations-page">
      <div className="page-header">
        <h1>Analytics</h1>
        <p>Line-wise OEE, downtime, rejection and maintenance KPIs for BIW operations.</p>
      </div>

      {loading && <p>Loading analytics...</p>}

      {!loading && (
        <>
          {maintenanceKpis && (
            <div className="form-panel">
              <h2>Maintenance KPIs</h2>

              <div className="kpi-grid">
                <div className="kpi-card">
                  <p>Total Breakdowns</p>
                  <h2>{maintenanceKpis.total_breakdowns}</h2>
                </div>

                <div className="kpi-card">
                  <p>Total Repair Time</p>
                  <h2>{maintenanceKpis.total_repair_time_min} min</h2>
                </div>

                <div className="kpi-card">
                  <p>MTTR</p>
                  <h2>{maintenanceKpis.mttr_min} min</h2>
                </div>

                <div className="kpi-card">
                  <p>MTBF</p>
                  <h2>{maintenanceKpis.mtbf_min} min</h2>
                </div>
              </div>
            </div>
          )}

          <div className="form-panel">
            <h2>OEE Summary</h2>

            <table className="data-table">
              <thead>
                <tr>
                  <th>Line</th>
                  <th>Availability</th>
                  <th>Performance</th>
                  <th>Quality</th>
                  <th>OEE</th>
                  <th>Downtime</th>
                </tr>
              </thead>

              <tbody>
                {oee.map((row) => (
                  <tr key={row.line}>
                    <td>{row.line}</td>
                    <td>{row.availability_percent}%</td>
                    <td>{row.performance_percent}%</td>
                    <td>{row.quality_percent}%</td>
                    <td>
                      <strong>{row.oee_percent}%</strong>
                    </td>
                    <td>{row.downtime_min} min</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="form-panel">
            <h2>Top Losses</h2>

            <table className="data-table">
              <thead>
                <tr>
                  <th>Line</th>
                  <th>Downtime</th>
                  <th>Rejected Units</th>
                </tr>
              </thead>

              <tbody>
                {losses.map((row) => (
                  <tr key={row.line}>
                    <td>{row.line}</td>
                    <td>{row.downtime_minutes} min</td>
                    <td>{row.rejected_units}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}