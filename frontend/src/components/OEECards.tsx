import { Activity, CheckCircle, Gauge, Zap } from "lucide-react";
import type { OEEData } from "../types/dashboard.types";

interface Props {
  data: OEEData[];
}

export default function OEECards({ data }: Props) {
  if (!data || data.length === 0) return null;

  const avgAvailability =
    data.reduce((sum, item) => sum + item.availability_percent, 0) / data.length;

  const avgPerformance =
    data.reduce((sum, item) => sum + item.performance_percent, 0) / data.length;

  const avgQuality =
    data.reduce((sum, item) => sum + item.quality_percent, 0) / data.length;

  const avgOEE =
    data.reduce((sum, item) => sum + item.oee_percent, 0) / data.length;

  const cards = [
    {
      title: "Availability",
      value: avgAvailability.toFixed(2),
      unit: "%",
      icon: Activity,
    },
    {
      title: "Performance",
      value: avgPerformance.toFixed(2),
      unit: "%",
      icon: Zap,
    },
    {
      title: "Quality",
      value: avgQuality.toFixed(2),
      unit: "%",
      icon: CheckCircle,
    },
    {
      title: "Overall OEE",
      value: avgOEE.toFixed(2),
      unit: "%",
      icon: Gauge,
    },
  ];

  return (
    <div className="section">
      <h2>OEE Overview</h2>

      <div className="kpi-grid oee-grid">
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
    </div>
  );
}