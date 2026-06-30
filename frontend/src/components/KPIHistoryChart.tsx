import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface KPIHistory {
  date: string;
  achievement_percent: number;
}

interface Props {
  data: KPIHistory[];
}
const formatDate = (date: string) => {
  const parts = date.split("-");
  return `${parts[1]}/${parts[2]}`;
}

export default function KPIHistoryChart({ data }: Props) {
  return (
    <div
      style={{
        marginTop: "30px",
        padding: "20px",
        background: "#173f6b",
        borderRadius: "12px",
      }}
    >
      <h2>KPI Achievement History</h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 35 }}>
          <XAxis dataKey="date" tickFormatter={formatDate} />
          <YAxis />
          <Tooltip />

          <Line
            type="monotone"
            dataKey="achievement_percent"
            stroke="#00ff88"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}