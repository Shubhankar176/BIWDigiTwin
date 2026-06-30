type AlertItem = {
  id?: number;
  message?: string;
  alert_message?: string;
  severity?: string;
  created_at?: string;
};

interface Props {
  data?: AlertItem[];
}

export default function AlertsPanel({ data = [] }: Props) {
  if (!data || data.length === 0) {
    return (
      <div className="form-panel">
        <p>No active alerts.</p>
      </div>
    );
  }

  return (
    <div className="form-panel">
      {data.map((alert, index) => (
        <div className="alert-item" key={alert.id || index}>
          <strong>{alert.severity || "Info"}</strong>
          <p>{alert.message || alert.alert_message || "Alert"}</p>
          {alert.created_at && <small>{alert.created_at}</small>}
        </div>
      ))}
    </div>
  );
}