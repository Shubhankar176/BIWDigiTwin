import type { AlertData } from "../types/dashboard.types";

interface Props {
  data: AlertData[];
}

export default function AlertsPanel({ data }: Props) {
  return (
    <div className="alerts-compact">
      {data.map((alert, index) => (
        <div
          key={index}
          className={`alert-row ${
            alert.severity === "HIGH" ? "alert-high" : "alert-medium"
          }`}
        >
          <div>
            <strong>{alert.severity}</strong> — {alert.line}
          </div>
          <div>{alert.message}</div>
          <small>{alert.timestamp}</small>
        </div>
      ))}
    </div>
  );
}