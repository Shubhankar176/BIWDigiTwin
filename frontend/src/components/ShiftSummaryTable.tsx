interface ShiftSummary {
  shift: string;
  target: number;
  actual: number;
  achievement_percent: number;
  rejected: number;
}

interface Props {
  data: ShiftSummary[];
}

export default function ShiftSummaryTable({ data }: Props) {
  return (
    <div
      style={{
        marginTop: "30px",
        padding: "20px",
        background: "#173f6b",
        borderRadius: "12px",
      }}
    >
      <h2>Shift Summary</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "15px",
        }}
      >
        <thead>
          <tr>
            <th>Shift</th>
            <th>Target</th>
            <th>Actual</th>
            <th>Achievement %</th>
            <th>Rejected</th>
          </tr>
        </thead>

        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row.shift}</td>
              <td>{row.target}</td>
              <td>{row.actual}</td>
              <td>{row.achievement_percent.toFixed(2)}</td>
              <td>{row.rejected}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}