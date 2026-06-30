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
  downtime_minutes: number;
  rejected_units: number;
}

interface Props {
  data: LossItem[];
}

const shortLineName = (line: string) => {
  return line
    .replace("SIGNA Main Line", "SIGNA ML")
    .replace("ILCV Main Line", "ILCV ML");
};

export default function TopLossesChart({ data = [] }: Props) {
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
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 10, bottom: 45 }}
        >
          <XAxis
            dataKey="line"
            tickFormatter={shortLineName}
            interval={0}
          />
          <YAxis />
          <Tooltip />

          <Bar dataKey="downtime_minutes" name="Downtime (min)" fill="#ff4d4d" />
          <Bar dataKey="rejected_units" name="Rejected Units" fill="#ffcc00" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}