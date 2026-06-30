import { Gauge, Target, Factory, AlertTriangle, Clock } from "lucide-react";

type DashboardCardData={
  [key: string]: string|number|null|undefined;
};

interface Props {
  data: DashboardCardData | null;
}

export default function KPICards({ data }: Props) {
  if (!data) return null;

  const getValue = (...keys: string[]) => {
    for (const key of keys) {
      if (data[key] !== undefined && data[key] !== null) {
        return data[key];
      }
    }
    return 0;
  };

  const cards = [
    {
      title: "Target",
      value: getValue("total_target", "target", "target_units"),
      unit: "units",
      icon: Target,
    },
    {
      title: "Actual",
      value: getValue("total_actual", "actual", "actual_units", "produced_units"),
      unit: "units",
      icon: Factory,
    },
    {
      title: "Achievement",
      value: getValue("achievement_percent", "achievement", "achievement_percentage"),
      unit: "%",
      icon: Gauge,
    },
    {
      title: "Rejected",
      value: getValue("total_rejected", "rejected", "rejected_units"),
      unit: "units",
      icon: AlertTriangle,
    },
    {
      title: "Downtime",
      value: getValue("total_downtime_min", "downtime_min", "downtime_minutes", "total_downtime"),
      unit: "min",
      icon: Clock,
    },
  ];

  return (
    <div className="kpi-grid">
      {cards.map((card) => {
        const Icon = card.icon;

        return (
          <div className="kpi-card" key={card.title}>
            <div className="kpi-icon">
              <Icon size={22} />
            </div>

            <div>
              <p className="kpi-title">{card.title}</p>
              <h2>
                {Number(card.value).toFixed(card.unit === "%" ? 2 : 0)}{" "}
                <span>{card.unit}</span>
              </h2>
            </div>
          </div>
        );
      })}
    </div>
  );
}