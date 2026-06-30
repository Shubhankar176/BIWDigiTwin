import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface LossItem {
  line: string;
  planned_downtime: number;
  unplanned_downtime: number;
  remarks: string;
}

interface Props {
  data: LossItem[];
}
const shortLineName = (line: string) => {
  return line
    .replace("SIGNA Main Line", "SIGNA ML")
    .replace("ILCV Main Line", "ILCV ML")
    .replace("SIGNA MFL", "SIGNA MFL")
    .replace("ILCV MFL", "ILCV MFL");
};
export default function TopLossesChart({ data }: Props) {
  return (
    <div
      style={{
        marginTop: "30px",
        padding: "20px",
        background: "#173f6b",
        borderRadius: "12px",
      }}
    >
      <h2>Top Losses</h2>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 45 }}>
          <XAxis dataKey="line" tickFormatter={shortLineName} interval={0}/>
          <YAxis />
          <Tooltip />

          <Bar dataKey="planned_downtime" fill="#ffcc00" />
          <Bar dataKey="unplanned_downtime" fill="#ff4d4d" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}