import { Gauge, Target, Factory, AlertTriangle, Clock } from "lucide-react";
import type { DashboardSummary } from "../types/dashboard.types";

interface Props {
  data: DashboardSummary | null;
}

export default function KPICards({ data }: Props) {
  if (!data) return null;

  const cards = [
    {
      title: "Target",
      value: data.total_target,
      unit: "units",
      icon: Target,
    },
    {
      title: "Actual",
      value: data.total_actual,
      unit: "units",
      icon: Factory,
    },
    {
      title: "Achievement",
      value: data.achievement_percent,
      unit: "%",
      icon: Gauge,
    },
    {
      title: "Rejected",
      value: data.total_rejected,
      unit: "units",
      icon: AlertTriangle,
    },
    {
      title: "Downtime",
      value: data.total_downtime_min,
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
                {card.value} <span>{card.unit}</span>
              </h2>
            </div>
          </div>
        );
      })}
    </div>
  );
}