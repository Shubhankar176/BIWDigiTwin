import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="BIW Digital Twin", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp { background-color: #070b12; color: #f8fafc; }
.block-container { padding-top: 1.2rem; max-width: 1400px; }
.card {
    background:#111827;
    border:1px solid #1f2937;
    border-radius:14px;
    padding:16px;
    margin-bottom:12px;
}
.small-card {
    background:#0f172a;
    border:1px solid #243244;
    border-radius:12px;
    padding:14px;
}
.na { color:#94a3b8; font-weight:700; }
.ok { color:#22c55e; font-weight:700; }
.warn { color:#facc15; font-weight:700; }
.bad { color:#ef4444; font-weight:700; }
h1, h2, h3 { letter-spacing:-0.03em; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
for key in ["production_records", "uploaded_files"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ---------------- PLANT STRUCTURE ----------------
LINES = {
    "ILCV Main Line": [
        "10 - SS Loading / Step Panel Geo Spot",
        "20 - Front Grille Welding",
        "30 - Side Wall to Floor Panel Spot Welding",
        "40 - Side Wall to Floor Panel Spot Welding",
        "50 - Mastic + Sealant + CO2 Welding",
        "60 - Rear Wall + Roof Spot Welding",
        "70 - Underbody CO2 Welding",
        "80 - Rear Wall Bottom Spot Welding",
        "90 - Unloading and Transfer",
    ],
    "ILCV MFL": [
        "10 - Body Shell Inner Side",
        "20 - Body Shell Outer",
        "60 - Door Fitment",
        "70 - Outer Corner Panel Fitment",
        "90 - Centre Panel Fitment",
        "120 - CP Flap and Jack Mount Clamp Fitment",
        "130 - QA Inspection",
        "140 - QA Inspection",
    ],
    "CAB Main Line": [
        "10 - Front Wall Assembly",
        "20 - Front Wall Welding",
        "30 - Front Wall Reinforcement",
        "40 - Ring / Support Welding",
        "50 - Robotic Spot Welding",
        "60 - Reinforcement Bonnet Welding",
    ],
    "CAB MFL": [
        "10 - Full Bonnet Reinforcement",
        "40 - Panel Side Inner / LOR for MTG Bracket",
        "60 - Grinding / Metal Finish Cleaning",
        "80 - Door Setting",
        "140 - CAB Unloading",
    ],
}

DATA_REQUIREMENTS = pd.DataFrame([
    ["KUKA Robot Logs", "Robot Health Model", "CSV Upload", "Robot_ID, Timestamp, Fault_Code, Alarm_Type, Runtime_Hours, Cycle_Count"],
    ["Rockwell PLC Data", "Production Twin", "CSV Upload", "Station_ID, PLC_Tag, Input_Status, Output_Status, Alarm, Timestamp"],
    ["Weld Gun Data", "Weld Quality Model", "CSV Upload", "Gun_ID, Weld_Count, Current, Pressure, Electrode_Age, Station_ID"],
    ["Maintenance Records", "Predictive Maintenance", "CSV Upload", "Equipment_ID, Failure_Type, Start_Time, End_Time, MTTR, Root_Cause"],
    ["Quality Records", "Quality Twin", "CSV Upload", "Station_ID, Defect_Type, Inspection_Result, Rework, Timestamp"],
    ["Production Records", "OEE and Output Tracking", "Manual Entry", "Date, Shift, Line, Target, Actual, Rejected, Planned_Downtime, Unplanned_Downtime"],
], columns=["Data Source", "Used For", "Input Method", "Required Fields"])

# ---------------- HELPERS ----------------
def readiness_status(source):
    if source == "Production Records":
        return "Connected" if st.session_state.production_records else "Not Available"
    return "Connected" if any(x["Data Source"] == source for x in st.session_state.uploaded_files) else "Not Available"

def badge(status):

    if status == "Connected":
        return '<span class="ok">Ready</span>'

    return '<span class="warn">Waiting For Data</span>'

def render_line(line_name):
    stations = LINES[line_name]
    st.subheader(line_name)
    st.caption("Station-level digital twin view. Values remain unavailable until plant data is connected.")

    cols = st.columns(3)
    for i, station in enumerate(stations):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <h4>{station}</h4>
                <p><b>Station Status:</b> <span class="na">Awaiting PLC data</span></p>
                <p><b>Robot / Equipment Health:</b> <span class="na">Awaiting logs</span></p>
                <p><b>Quality Status:</b> <span class="na">Awaiting records</span></p>
                <p><b>Maintenance Risk:</b> <span class="na">Awaiting history</span></p>
            </div>
            """, unsafe_allow_html=True)

def uploaded_table():
    if st.session_state.uploaded_files:
        st.dataframe(pd.DataFrame(st.session_state.uploaded_files), use_container_width=True)
    else:
        st.info("No CSV datasets uploaded yet.")

# ---------------- TOP TABS ----------------
st.title("BIW Digital Twin Platform")
st.caption("Digital twin framework for ILCV and CAB BIW lines with plug-in data integration.")

tabs = st.tabs([
    "Overview",
    "Plant Explorer",
    "Data Hub",
    "Analytics Center",
])

# ---------------- OVERVIEW ----------------
with tabs[0]:
    total_stations = sum(len(v) for v in LINES.values())
    connected_sources = sum(1 for src in DATA_REQUIREMENTS["Data Source"] if readiness_status(src) == "Connected")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Production Streams", "2")
    c2.metric("BIW Lines", "4")
    c3.metric("Stations Mapped", total_stations)
    c4.metric("Twin Data Readiness", f"{connected_sources}/6")

    st.divider()

    left, right = st.columns([1.1, 1])

    with left:
        st.subheader("Plant Structure")
        st.code("""
BIW Plant
│
├── ILCV Production
│   ├── ILCV Main Line
│   └── ILCV MFL
│
└── CAB Production
    ├── CAB Main Line
    └── CAB MFL
""")

    with right:
        st.subheader("Digital Twin Readiness")
        for src in DATA_REQUIREMENTS["Data Source"]:
            st.markdown(f"""
            <div class="small-card">
                <b>{src}</b><br>
                Status: {badge(readiness_status(src))}
            </div>
            """, unsafe_allow_html=True)

# ---------------- PLANT EXPLORER ----------------
# ---------------- PLANT EXPLORER ----------------
with tabs[1]:
    st.subheader("Plant Explorer")
    st.caption("Station-level twin structure for ILCV and CAB production lines.")

    line_tabs = st.tabs([
        "ILCV Main Line",
        "ILCV MFL",
        "CAB Main Line",
        "CAB MFL"
    ])

    with line_tabs[0]:
        render_line("ILCV Main Line")

    with line_tabs[1]:
        render_line("ILCV MFL")

    with line_tabs[2]:
        render_line("CAB Main Line")

    with line_tabs[3]:
        render_line("CAB MFL")
# ---------------- DATA HUB ----------------
with tabs[2]:
    st.subheader("Data Hub")
    st.caption("Data mapping comes first. Production is entered manually. Historical logs are uploaded as CSV.")

    data_tabs = st.tabs([
        "Data Mapping",
        "Production Entry",
        "CSV Upload",
        "Connected Data"
    ])

    with data_tabs[0]:
        st.markdown("### Required Data Sources")
        st.dataframe(DATA_REQUIREMENTS, use_container_width=True)

    with data_tabs[1]:
        st.markdown("### Manual Production Entry")

        with st.form("production_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                date = st.date_input("Date")
                shift = st.selectbox("Shift", ["A", "B", "C", "General"])
                line = st.selectbox("Line", list(LINES.keys()))
            with c2:
                target = st.number_input("Target Production", min_value=0, step=1)
                actual = st.number_input("Actual Production", min_value=0, step=1)
                rejected = st.number_input("Rejected / Rework Units", min_value=0, step=1)
            with c3:
                planned_dt = st.number_input("Planned Downtime (minutes)", min_value=0, step=5)
                unplanned_dt = st.number_input("Unplanned Downtime (minutes)", min_value=0, step=5)
                remarks = st.text_input("Remarks")

            submit = st.form_submit_button("Save Production Record")

        if submit:
            st.session_state.production_records.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Date": str(date),
                "Shift": shift,
                "Line": line,
                "Target Production": target,
                "Actual Production": actual,
                "Rejected / Rework Units": rejected,
                "Planned Downtime (min)": planned_dt,
                "Unplanned Downtime (min)": unplanned_dt,
                "Remarks": remarks
            })
            st.success("Production record saved.")

        if st.session_state.production_records:
            st.dataframe(pd.DataFrame(st.session_state.production_records), use_container_width=True)
        else:
            st.info("No production records entered yet.")

    with data_tabs[2]:
        st.markdown("### Upload Historical Datasets")

        dataset_type = st.selectbox(
            "Dataset Type",
            [
                "KUKA Robot Logs",
                "Rockwell PLC Data",
                "Weld Gun Data",
                "Maintenance Records",
                "Quality Records",
            ]
        )

        file = st.file_uploader("Upload CSV", type=["csv"])

        if file is not None:
            df = pd.read_csv(file)
            st.session_state.uploaded_files.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Data Source": dataset_type,
                "File Name": file.name,
                "Rows": len(df),
                "Columns": len(df.columns)
            })
            st.success(f"{dataset_type} uploaded successfully.")
            st.dataframe(df.head(20), use_container_width=True)

    with data_tabs[3]:
        st.markdown("### Connected Data Sources")

        status_df = DATA_REQUIREMENTS.copy()
        status_df["Status"] = status_df["Data Source"].apply(readiness_status)
        st.dataframe(status_df, use_container_width=True)

        st.markdown("### Uploaded Files")
        uploaded_table()

# ---------------- ANALYTICS ----------------
with tabs[3]:
    st.subheader("Analytics Center")
    st.caption("Analytics modules activate only after required data is connected.")

    modules = pd.DataFrame([
        ["Weld Quality Prediction", "Weld Gun Data + Quality Records"],
        ["Electrode Life Prediction", "Weld Gun Data"],
        ["Robot Health Prediction", "KUKA Robot Logs + Maintenance Records"],
        ["Predictive Maintenance", "Maintenance Records + PLC Data"],
        ["OEE Analysis", "Production Records + Downtime Data"],
        ["Bottleneck Detection", "Production Records + PLC Data"],
    ], columns=["Module", "Required Data"])

    modules["Status"] = "Waiting for Data"
    st.dataframe(modules, use_container_width=True)

    if st.session_state.production_records:
        st.divider()
        st.markdown("### Production Summary")

        prod = pd.DataFrame(st.session_state.production_records)
        prod["Target Production"] = pd.to_numeric(prod["Target Production"])
        prod["Actual Production"] = pd.to_numeric(prod["Actual Production"])
        prod["Rejected / Rework Units"] = pd.to_numeric(prod["Rejected / Rework Units"])

        total_target = int(prod["Target Production"].sum())
        total_actual = int(prod["Actual Production"].sum())
        total_rejected = int(prod["Rejected / Rework Units"].sum())

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Target", total_target)
        c2.metric("Total Actual", total_actual)
        c3.metric("Total Rejected / Rework", total_rejected)


