import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface DowntimeSummary {
  line: string;
  planned_downtime: number;
  unplanned_downtime: number;
  total_downtime: number;
}

interface Props {
  data: DowntimeSummary[];
}
const shortLineName = (line: string) => {
  return line
    .replace("SIGNA Main Line", "SIGNA ML")
    .replace("ILCV Main Line", "ILCV ML")
    .replace("SIGNA MFL", "SIGNA MFL")
    .replace("ILCV MFL", "ILCV MFL");
};

export default function DowntimeSummaryChart({ data }: Props) {
  return (
    <div
      style={{
        marginTop: "30px",
        padding: "20px",
        background: "#173f6b",
        borderRadius: "12px",
      }}
    >
      <h2>Downtime Summary</h2>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 45 }}>
          <XAxis dataKey="line" tickFormatter={shortLineName} interval={0}/>
          <YAxis />
          <Tooltip />

          <Bar dataKey="planned_downtime" fill="#ffcc00" />
          <Bar dataKey="unplanned_downtime" fill="#ff4d4d" />
          <Bar dataKey="total_downtime" fill="#00ff88" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}