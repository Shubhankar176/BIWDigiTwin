import { useEffect, useState } from "react";
import { api, endpoints } from "../services/api";

export const useDashboardData = () => {
  const [loading, setLoading] = useState(true);

  const [dashboardSummary, setDashboardSummary] = useState(null);
  const [lineSummary, setLineSummary] = useState([]);
  const [shiftSummary, setShiftSummary] = useState([]);
  const [downtimeSummary, setDowntimeSummary] = useState([]);
  const [productionTrend, setProductionTrend] = useState([]);
  const [oeeSummary, setOeeSummary] = useState([]);
  const [topLosses, setTopLosses] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        const [
          dashboard,
          lines,
          shifts,
          downtime,
          trend,
          oee,
          losses,
        ] = await Promise.all([
          api.get(endpoints.dashboardSummary),
          api.get(endpoints.lineSummary),
          api.get(endpoints.shiftSummary),
          api.get(endpoints.downtimeSummary),
          api.get(endpoints.productionTrend),
          api.get(endpoints.oeeSummary),
          api.get(endpoints.topLosses),
        ]);

        setDashboardSummary(dashboard.data || null);
        setLineSummary(lines.data.line_summary || []);
        setShiftSummary(shifts.data.shift_summary || []);
        setDowntimeSummary(downtime.data.downtime_summary || []);
        setProductionTrend(trend.data.production_trend || []);
        setOeeSummary(oee.data.oee_summary || []);
        setTopLosses(losses.data.top_losses || []);
      } catch (err) {
        console.error("Dashboard data load failed:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, []);

  return {
    loading,
    dashboardSummary,
    lineSummary,
    shiftSummary,
    downtimeSummary,
    productionTrend,
    oeeSummary,
    topLosses,
  };
};