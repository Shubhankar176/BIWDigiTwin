import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const endpoints = {
  dashboardSummary: "/dashboard-summary",
  lineSummary: "/line-summary",
  shiftSummary: "/shift-summary",
  downtimeSummary: "/downtime-summary",
  productionTrend: "/production-trend",
  oeeSummary: "/oee-summary",
  topLosses: "/top-losses",
  alerts: "/alerts",
  kpiHistory: "/kpi-history",
  lines: "/lines",
  stations: "/stations",
};

export const createProductionEntry = async (data: object) => {
  const response = await api.post("/production-events", data);
  return response.data;
};

export const createDailyTarget = async (data: object) => {
  const response = await api.post("/daily-targets", data);
  return response.data;
};

export const createMaintenanceBreakdown = async (data: object) => {
  const response = await api.post("/maintenance-breakdowns", data);
  return response.data;
};

export const createLotoRecord = async (data: object) => {
  const response = await api.post("/loto-records", data);
  return response.data;
};

export const createPMRecord = async (data: object) => {
  const response = await api.post("/pm-records", data);
  return response.data;
};

export const createSpareRecord = async (data: object) => {
  const response = await api.post("/spare-records", data);
  return response.data;
};

export const createManpowerRecord = async (data: object) => {
  const response = await api.post("/manpower-records", data);
  return response.data;
};