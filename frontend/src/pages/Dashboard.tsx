import KPICards from "../components/KPICards";
import OEECards from "../components/OEECards";

import AlertsPanel from "../components/AlertsPanel";
import ProductionTrendChart from "../components/ProductionTrend";

import TopLossesChart from "../components/TopLossesChart";
import KPIHistoryChart from "../components/KPIHistoryChart";

import LineSummaryTable from "../components/LineSummaryTable";
import ShiftSummaryTable from "../components/ShiftSummaryTable";

import DowntimeSummaryChart from "../components/DowntimeSummaryChart";
import { useDashboardData } from "../hooks/useDashboardData";

export default function Dashboard() {
  const {
    loading,
    dashboardSummary,
    oeeSummary,
    productionTrend,
    topLosses,
    lineSummary,
    shiftSummary,
    downtimeSummary,
  } = useDashboardData();

  if (loading) {
    return <div className="loading">Loading BIW Digital Twin...</div>;
  }

  return (
    <div className="dashboard">
  <div className="dashboard-header">
    <div>
      <h1>BIW Digital Twin Dashboard</h1>
      <p>ILCV and SIGNA production monitoring system</p>
    </div>

    <div className="status-pill">Live Backend Connected</div>
  </div>

  <section className="dashboard-section">
    <KPICards data={dashboardSummary} />
  </section>

  <section className="dashboard-section">
    <h2 className="section-title">Production Analytics</h2>

    <div className="chart-grid">
      <ProductionTrendChart data={productionTrend} />
      <TopLossesChart data={topLosses} />
      <DowntimeSummaryChart data={downtimeSummary} />
    </div>
  </section>

  <section className="dashboard-section">
    <h2 className="section-title">Line & Shift Details</h2>

    <div className="chart-grid">
      <LineSummaryTable data={lineSummary} />
      <ShiftSummaryTable data={shiftSummary} />
    </div>
  </section>

  <section className="dashboard-section">
    <h2 className="section-title"></h2>
    <OEECards data={oeeSummary} />
  </section>

  <section className="dashboard-section">
    <h2 className="section-title">Live Alerts</h2>
    <AlertsPanel data={[]} />
  </section>
</div>
  );
}