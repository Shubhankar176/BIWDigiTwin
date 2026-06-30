import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import type { ProductionTrend } from "../types/dashboard.types";

interface Props {
  data: ProductionTrend[];
}
const formatDate = (date: string) => {
  const parts = date.split("-");
  return `${parts[1]}/${parts[2]}`;
};


export default function ProductionTrendChart({ data }: Props) {
  return (
    <div
      style={{
        marginTop: "30px",
        padding: "20px",
        background: "#173f6b",
        borderRadius: "12px",
      }}
    >
      <h2>Production Trend</h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 35 }}>
          <XAxis dataKey="date" tickFormatter={formatDate} />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="actual"
            stroke="#00ff88"
            strokeWidth={3}
          />

          <Line
            type="monotone"
            dataKey="target"
            stroke="#ffcc00"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}