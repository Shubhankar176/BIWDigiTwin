import { useEffect, useState } from "react";
import { api } from "../services/api";

type LiveLog = {
  time: string;
  module: string;
  line: string;
  shift: string;
  description: string;
  person: string;
};

export default function LiveLogs() {
  const [logs, setLogs] = useState<LiveLog[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    try {
      const response = await api.get("/live-logs");
      setLogs(response.data.live_logs || []);
    } catch (error) {
      console.error(error);
      alert("Failed to load live logs");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setTimeout(()=>{
        fetchLogs();
    },0);

    const interval = setInterval(fetchLogs, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="operations-page">
      <div className="page-header">
        <h1>Live Logs</h1>
        <p>Real-time activity feed from production, maintenance, PM and LOTO records.</p>
      </div>

      <div className="form-panel">
        <h2>Recent Shop Floor Activity</h2>

        {loading && <p>Loading live logs...</p>}

        {!loading && logs.length === 0 && <p>No logs found.</p>}

        {!loading && logs.length > 0 && (
          <table className="data-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Module</th>
                <th>Line / Location</th>
                <th>Shift</th>
                <th>Description</th>
                <th>Person</th>
              </tr>
            </thead>

            <tbody>
              {logs.map((log, index) => (
                <tr key={index}>
                  <td>{new Date(log.time).toLocaleString()}</td>
                  <td>{log.module}</td>
                  <td>{log.line}</td>
                  <td>{log.shift || "-"}</td>
                  <td>{log.description}</td>
                  <td>{log.person || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}