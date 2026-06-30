export interface DashboardSummary {
  total_target: number;
  total_actual: number;
  achievement_percent: number;
  total_rejected: number;
  quality_rate_percent: number;
  planned_downtime_min: number;
  unplanned_downtime_min: number;
  total_downtime_min: number;
}

export interface LineSummary {
  line: string;
  target_units: number;
  actual_units: number;
  achievement_percent: number;
  rejected_units: number;
  downtime_min: number;
}

export interface ShiftSummary {
  shift: string;
  target: number;
  actual: number;
  achievement_percent: number;
  rejected: number;
}

export interface DowntimeSummary {
  line: string;
  planned_downtime: number;
  unplanned_downtime: number;
  total_downtime: number;
}

export interface OEEData {
  line: string;
  availability_percent: number;
  performance_percent: number;
  quality_percent: number;
  oee_percent: number;
  downtime_min: number;
}

export interface AlertData {
  severity: string;
  line: string;
  message: string;
  timestamp: string;
}

export interface KPIHistory {
  date: string;
  target_units: number;
  actual_units: number;
  achievement_percent: number;
  rejected_units: number;
  quality_percent: number;
  downtime_min: number;
}

export interface ProductionTrend {
  date: string;
  target: number;
  actual: number;
  rejected: number;
  downtime: number;
}