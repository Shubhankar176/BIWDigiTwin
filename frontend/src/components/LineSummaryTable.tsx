interface LineSummary {
  line: string;
  target_units: number;
  actual_units: number;
  achievement_percent: number;
  rejected_units: number;
  downtime_min: number;
}

interface Props {
  data: LineSummary[];
}

export default function LineSummaryTable({ data }: Props) {
  return (
    <div
      style={{
        marginTop: "30px",
        padding: "20px",
        background: "#173f6b",
        borderRadius: "12px",
      }}
    >
      <h2>Line Summary</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "15px",
        }}
      >
        <thead>
          <tr>
            <th>Line</th>
            <th>Target</th>
            <th>Actual</th>
            <th>Achievement %</th>
            <th>Rejected</th>
            <th>Downtime (min)</th>
          </tr>
        </thead>

        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row.line}</td>
              <td>{row.target_units}</td>
              <td>{row.actual_units}</td>
              <td>{row.achievement_percent.toFixed(2)}</td>
              <td>{row.rejected_units}</td>
              <td>{row.downtime_min}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}