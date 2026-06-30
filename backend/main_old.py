from fastapi import FastAPI
from sqlalchemy import text

from database import engine
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.schemas_old import MaintenanceBreakdownCreate , DailyTargetCreate , LotoCreate , PMRecordCreate , SpareRecordCreate , ManpowerRecordCreate

app = FastAPI(
    title="BIW Digital Twin API",
    version="1.0.0"
)
class ProductionEventCreate(BaseModel):
    line: str
    shift: str
    produced_units: int
    rejected_units: int = 0
    downtime_minutes: int = 0
    downtime_reason: str | None = None
    operator_name: str | None = None
    remarks: str | None = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "BIW Digital Twin Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-test")
def db_test():

    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW();"))
        current_time = result.fetchone()[0]

    return {
        "database": "connected",
        "server_time": str(current_time)
    }
@app.get("/tables")
def get_tables():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
        """))

        return {
            "tables": [row[0] for row in result]
        }
    
@app.get("/lines")
def get_lines():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                l.id,
                pt.production_name,
                l.line_name
            FROM lines l
            JOIN production_types pt
            ON l.production_type_id = pt.id
            ORDER BY l.id;
        """))

        lines = []

        for row in result:
            lines.append({
                "id": row[0],
                "production": row[1],
                "line_name": row[2]
            })

    return {
        "lines": lines
    }

@app.get("/stations")
def get_stations():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                s.id,
                l.line_name,
                s.station_code,
                s.station_name
            FROM stations s
            JOIN lines l
            ON s.line_id = l.id
            ORDER BY l.id, s.id;
        """))

        stations = []

        for row in result:
            stations.append({
                "id": row[0],
                "line_name": row[1],
                "station_code": row[2],
                "station_name": row[3]
            })

    return {
        "stations": stations
    }

@app.get("/production-types")
def get_production_types():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT *
            FROM production_types
            ORDER BY id;
        """))

        data = []

        for row in result:
            data.append({
                "id": row[0],
                "vehicle_type": row[1]
            })

    return {"production_types": data}

@app.get("/production-logs")
def get_production_logs():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                pl.id,
                pl.log_date,
                pl.shift,
                l.line_name,
                pl.target_units,
                pl.actual_units,
                pl.rejected_units,
                pl.planned_downtime_min,
                pl.unplanned_downtime_min,
                pl.remarks
            FROM production_logs pl
            JOIN lines l
            ON pl.line_id = l.id
            ORDER BY pl.id;
        """))

        data = []

        for row in result:
            data.append({
                "id": row[0],
                "log_date": str(row[1]),
                "shift": row[2],
                "line": row[3],
                "target_units": row[4],
                "actual_units": row[5],
                "rejected_units": row[6],
                "planned_downtime_min": row[7],
                "unplanned_downtime_min": row[8],
                "remarks": row[9]
            })

    return {"production_logs": data}

@app.get("/dashboard-summary")
def dashboard_summary():

    with engine.connect() as conn:

        target_row = conn.execute(text("""
            SELECT COALESCE(SUM(target_units), 0)
            FROM daily_targets
        """)).fetchone()

        production_row = conn.execute(text("""
            SELECT
                COALESCE(SUM(produced_units), 0),
                COALESCE(SUM(rejected_units), 0),
                COALESCE(SUM(downtime_minutes), 0)
            FROM production_events
        """)).fetchone()

        total_target = target_row[0]

        total_actual = production_row[0]
        total_rejected = production_row[1]
        total_downtime = production_row[2]

        achievement = 0
        if total_target > 0:
            achievement = round(
                (total_actual / total_target) * 100,
                2
            )

        quality_rate = 0
        if total_actual > 0:
            quality_rate = round(
                ((total_actual - total_rejected) / total_actual) * 100,
                2
            )

    return {
        "total_target": total_target,
        "total_actual": total_actual,
        "achievement_percent": achievement,
        "total_rejected": total_rejected,
        "quality_rate_percent": quality_rate,
        "total_downtime_min": total_downtime
    }

@app.get("/line-summary")
def line_summary():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                l.line_name,
                COALESCE(SUM(pl.target_units), 0) AS total_target,
                COALESCE(SUM(pl.actual_units), 0) AS total_actual,
                COALESCE(SUM(pl.rejected_units), 0) AS total_rejected,
                COALESCE(SUM(pl.planned_downtime_min + pl.unplanned_downtime_min), 0) AS total_downtime
            FROM lines l
            LEFT JOIN production_logs pl
            ON l.id = pl.line_id
            GROUP BY l.line_name
            ORDER BY l.line_name;
        """))

        data = []

        for row in result:
            target = row[1]
            actual = row[2]

            achievement = 0
            if target > 0:
                achievement = round((actual / target) * 100, 2)

            data.append({
                "line": row[0],
                "target_units": target,
                "actual_units": actual,
                "achievement_percent": achievement,
                "rejected_units": row[3],
                "downtime_min": row[4]
            })

    return {
        "line_summary": data
    }

@app.get("/top-losses")
def top_losses():

    with engine.connect() as conn:

        result = conn.execute(text("""
            SELECT
                line_name,
                planned_downtime_min,
                unplanned_downtime_min,
                remarks
            FROM production_logs pl
            JOIN lines l
            ON pl.line_id = l.id
            ORDER BY unplanned_downtime_min DESC
            LIMIT 5
        """))

        losses = []

        for row in result:
            losses.append({
                "line": row[0],
                "planned_downtime": row[1],
                "unplanned_downtime": row[2],
                "remarks": row[3]
            })

    return {
        "top_losses": losses
    }

@app.get("/shift-summary")
def shift_summary():

    with engine.connect() as conn:

        result = conn.execute(text("""
            SELECT
                shift,
                SUM(target_units) as target,
                SUM(actual_units) as actual,
                SUM(rejected_units) as rejected
            FROM production_logs
            GROUP BY shift
            ORDER BY shift;
        """))

        data = []

        for row in result:

            achievement = round(
                (row.actual / row.target) * 100,
                2
            )

            data.append({
                "shift": row.shift,
                "target": row.target,
                "actual": row.actual,
                "achievement_percent": achievement,
                "rejected": row.rejected
            })

    return {"shift_summary": data}

@app.get("/downtime-summary")
def downtime_summary():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                l.line_name,
                SUM(pl.planned_downtime_min) AS planned_downtime,
                SUM(pl.unplanned_downtime_min) AS unplanned_downtime,
                SUM(pl.planned_downtime_min + pl.unplanned_downtime_min) AS total_downtime
            FROM production_logs pl
            JOIN lines l
            ON pl.line_id = l.id
            GROUP BY l.line_name
            ORDER BY total_downtime DESC;
        """))

        data = []

        for row in result:
            data.append({
                "line": row[0],
                "planned_downtime": row[1],
                "unplanned_downtime": row[2],
                "total_downtime": row[3]
            })

    return {"downtime_summary": data}

@app.get("/production-trend")
def production_trend():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                DATE(event_time) AS log_date,
                COALESCE(SUM(produced_units), 0) AS actual,
                COALESCE(SUM(rejected_units), 0) AS rejected,
                COALESCE(SUM(downtime_minutes), 0) AS downtime
            FROM production_events
            GROUP BY DATE(event_time)
            ORDER BY DATE(event_time);
        """))

        data = []

        for row in result:
            data.append({
                "date": str(row[0]),
                "target": 0,
                "actual": row[1],
                "rejected": row[2],
                "downtime": row[3]
            })

    return {"production_trend": data}


@app.get("/oee-summary")
def oee_summary():

    SHIFT_TIME_MIN = 480

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                l.line_name,
                COALESCE(SUM(pl.target_units), 0) AS target,
                COALESCE(SUM(pl.actual_units), 0) AS actual,
                COALESCE(SUM(pl.rejected_units), 0) AS rejected,
                COALESCE(SUM(pl.planned_downtime_min + pl.unplanned_downtime_min), 0) AS downtime
            FROM lines l
            LEFT JOIN production_logs pl
            ON l.id = pl.line_id
            GROUP BY l.line_name
            ORDER BY l.line_name;
        """))

        data = []

        for row in result:
            line = row[0]
            target = row[1]
            actual = row[2]
            rejected = row[3]
            downtime = row[4]

            availability = 0
            performance = 0
            quality = 0
            oee = 0

            if SHIFT_TIME_MIN > 0:
                availability = ((SHIFT_TIME_MIN - downtime) / SHIFT_TIME_MIN) * 100

            if target > 0:
                performance = (actual / target) * 100

            if actual > 0:
                quality = ((actual - rejected) / actual) * 100

            oee = (availability / 100) * (performance / 100) * (quality / 100) * 100

            data.append({
                "line": line,
                "availability_percent": round(availability, 2),
                "performance_percent": round(performance, 2),
                "quality_percent": round(quality, 2),
                "oee_percent": round(oee, 2),
                "downtime_min": downtime
            })

    return {"oee_summary": data}

@app.get("/line-details/{line_id}")
def line_details(line_id: int):

    SHIFT_TIME_MIN = 480

    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT
                l.line_name,
                COALESCE(SUM(pl.target_units), 0),
                COALESCE(SUM(pl.actual_units), 0),
                COALESCE(SUM(pl.rejected_units), 0),
                COALESCE(SUM(pl.planned_downtime_min), 0),
                COALESCE(SUM(pl.unplanned_downtime_min), 0)
            FROM lines l
            LEFT JOIN production_logs pl
            ON l.id = pl.line_id
            WHERE l.id = :line_id
            GROUP BY l.line_name;
        """), {"line_id": line_id}).fetchone()

        if row is None:
            return {"error": "Line not found"}

        line = row[0]
        target = row[1]
        actual = row[2]
        rejected = row[3]
        planned_dt = row[4]
        unplanned_dt = row[5]
        total_dt = planned_dt + unplanned_dt

        achievement = round((actual / target) * 100, 2) if target > 0 else 0
        availability = round(((SHIFT_TIME_MIN - total_dt) / SHIFT_TIME_MIN) * 100, 2)
        performance = achievement
        quality = round(((actual - rejected) / actual) * 100, 2) if actual > 0 else 0
        oee = round((availability / 100) * (performance / 100) * (quality / 100) * 100, 2)

    return {
        "line_id": line_id,
        "line": line,
        "target_units": target,
        "actual_units": actual,
        "achievement_percent": achievement,
        "rejected_units": rejected,
        "planned_downtime_min": planned_dt,
        "unplanned_downtime_min": unplanned_dt,
        "total_downtime_min": total_dt,
        "availability_percent": availability,
        "performance_percent": performance,
        "quality_percent": quality,
        "oee_percent": oee
    }


@app.get("/line-summary")
def line_summary():

    with engine.connect() as conn:
        result = conn.execute(text("""
            WITH production_by_line AS (
                SELECT
                    line,
                    COALESCE(SUM(produced_units), 0) AS total_actual,
                    COALESCE(SUM(rejected_units), 0) AS total_rejected,
                    COALESCE(SUM(downtime_minutes), 0) AS total_downtime
                FROM production_events
                GROUP BY line
            ),
            target_by_line AS (
                SELECT
                    line,
                    COALESCE(SUM(target_units), 0) AS total_target
                FROM daily_targets
                GROUP BY line
            )
            SELECT
                COALESCE(p.line, t.line) AS line,
                COALESCE(t.total_target, 0) AS total_target,
                COALESCE(p.total_actual, 0) AS total_actual,
                COALESCE(p.total_rejected, 0) AS total_rejected,
                COALESCE(p.total_downtime, 0) AS total_downtime
            FROM production_by_line p
            FULL OUTER JOIN target_by_line t
            ON p.line = t.line
            ORDER BY line;
        """))

        data = []

        for row in result:
            target = row[1]
            actual = row[2]

            achievement = 0
            if target > 0:
                achievement = round((actual / target) * 100, 2)

            data.append({
                "line": row[0],
                "target_units": target,
                "actual_units": actual,
                "achievement_percent": achievement,
                "rejected_units": row[3],
                "downtime_min": row[4]
            })

    return {"line_summary": data}

@app.get("/top-losses")
def top_losses():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                line,
                COALESCE(SUM(downtime_minutes), 0) AS total_downtime,
                COALESCE(SUM(rejected_units), 0) AS total_rejected
            FROM production_events
            GROUP BY line
            ORDER BY total_downtime DESC
            LIMIT 5;
        """))

        losses = []

        for row in result:
            losses.append({
                "line": row[0],
                "planned_downtime": 0,
                "unplanned_downtime": row[1],
                "remarks": f"Rejected units: {row[2]}"
            })

    return {"top_losses": losses}



@app.get("/shift-summary")
def shift_summary():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                pe.shift,
                COALESCE(SUM(dt.target_units), 0) AS target,
                COALESCE(SUM(pe.produced_units), 0) AS actual,
                COALESCE(SUM(pe.rejected_units), 0) AS rejected
            FROM production_events pe
            LEFT JOIN daily_targets dt
            ON pe.line = dt.line
            AND pe.shift = dt.shift
            GROUP BY pe.shift
            ORDER BY pe.shift;
        """))

        data = []

        for row in result:
            target = row[1]
            actual = row[2]

            achievement = 0
            if target > 0:
                achievement = round((actual / target) * 100, 2)

            data.append({
                "shift": row[0],
                "target": target,
                "actual": actual,
                "achievement_percent": achievement,
                "rejected": row[3]
            })

    return {"shift_summary": data}

@app.get("/downtime-summary")
def downtime_summary():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                line,
                COALESCE(SUM(downtime_minutes), 0) AS total_downtime
            FROM production_events
            GROUP BY line
            ORDER BY total_downtime DESC;
        """))

        data = []

        for row in result:
            data.append({
                "line": row[0],
                "planned_downtime": 0,
                "unplanned_downtime": row[1],
                "total_downtime": row[1]
            })

    return {"downtime_summary": data}

@app.get("/production-trend")
def production_trend():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                log_date,
                SUM(target_units) AS target,
                SUM(actual_units) AS actual,
                SUM(rejected_units) AS rejected,
                SUM(planned_downtime_min + unplanned_downtime_min) AS downtime
            FROM production_logs
            GROUP BY log_date
            ORDER BY log_date;
        """))

        data = []

        for row in result:
            data.append({
                "date": str(row[0]),
                "target": row[1],
                "actual": row[2],
                "rejected": row[3],
                "downtime": row[4]
            })

    return {"production_trend": data}


@app.get("/oee-summary")
def oee_summary():

    SHIFT_TIME_MIN = 480

    with engine.connect() as conn:
        result = conn.execute(text("""
            WITH production_by_line AS (
                SELECT
                    line,
                    COALESCE(SUM(produced_units), 0) AS actual,
                    COALESCE(SUM(rejected_units), 0) AS rejected,
                    COALESCE(SUM(downtime_minutes), 0) AS downtime
                FROM production_events
                GROUP BY line
            ),
            target_by_line AS (
                SELECT
                    line,
                    COALESCE(SUM(target_units), 0) AS target
                FROM daily_targets
                GROUP BY line
            )
            SELECT
                COALESCE(p.line, t.line) AS line,
                COALESCE(t.target, 0) AS target,
                COALESCE(p.actual, 0) AS actual,
                COALESCE(p.rejected, 0) AS rejected,
                COALESCE(p.downtime, 0) AS downtime
            FROM production_by_line p
            FULL OUTER JOIN target_by_line t
            ON p.line = t.line
            ORDER BY line;
        """))

        data = []

        for row in result:
            line = row[0]
            target = row[1]
            actual = row[2]
            rejected = row[3]
            downtime = row[4]

            availability = 0
            performance = 0
            quality = 0
            oee = 0

            if SHIFT_TIME_MIN > 0:
                availability = ((SHIFT_TIME_MIN - downtime) / SHIFT_TIME_MIN) * 100

            if target > 0:
                performance = (actual / target) * 100

            if actual > 0:
                quality = ((actual - rejected) / actual) * 100

            oee = (
                (availability / 100)
                * (performance / 100)
                * (quality / 100)
                * 100
            )

            data.append({
                "line": line,
                "availability_percent": round(availability, 2),
                "performance_percent": round(performance, 2),
                "quality_percent": round(quality, 2),
                "oee_percent": round(oee, 2),
                "downtime_min": downtime
            })

    return {"oee_summary": data}

@app.get("/line-details/{line_id}")
def line_details(line_id: int):

    SHIFT_TIME_MIN = 480

    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT
                l.line_name,
                COALESCE(SUM(pl.target_units), 0),
                COALESCE(SUM(pl.actual_units), 0),
                COALESCE(SUM(pl.rejected_units), 0),
                COALESCE(SUM(pl.planned_downtime_min), 0),
                COALESCE(SUM(pl.unplanned_downtime_min), 0)
            FROM lines l
            LEFT JOIN production_logs pl
            ON l.id = pl.line_id
            WHERE l.id = :line_id
            GROUP BY l.line_name;
        """), {"line_id": line_id}).fetchone()

        if row is None:
            return {"error": "Line not found"}

        line = row[0]
        target = row[1]
        actual = row[2]
        rejected = row[3]
        planned_dt = row[4]
        unplanned_dt = row[5]
        total_dt = planned_dt + unplanned_dt

        achievement = round((actual / target) * 100, 2) if target > 0 else 0
        availability = round(((SHIFT_TIME_MIN - total_dt) / SHIFT_TIME_MIN) * 100, 2)
        performance = achievement
        quality = round(((actual - rejected) / actual) * 100, 2) if actual > 0 else 0
        oee = round((availability / 100) * (performance / 100) * (quality / 100) * 100, 2)

    return {
        "line_id": line_id,
        "line": line,
        "target_units": target,
        "actual_units": actual,
        "achievement_percent": achievement,
        "rejected_units": rejected,
        "planned_downtime_min": planned_dt,
        "unplanned_downtime_min": unplanned_dt,
        "total_downtime_min": total_dt,
        "availability_percent": availability,
        "performance_percent": performance,
        "quality_percent": quality,
        "oee_percent": oee
    }

from datetime import datetime

@app.get("/alerts")
def alerts():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                l.line_name,
                COALESCE(SUM(pl.target_units), 0) AS target,
                COALESCE(SUM(pl.actual_units), 0) AS actual,
                COALESCE(SUM(pl.rejected_units), 0) AS rejected,
                COALESCE(SUM(pl.planned_downtime_min + pl.unplanned_downtime_min), 0) AS downtime
            FROM lines l
            LEFT JOIN production_logs pl
            ON l.id = pl.line_id
            GROUP BY l.line_name
            ORDER BY l.line_name;
        """))

        alert_list = []

        for row in result:
            line = row[0]
            target = row[1]
            actual = row[2]
            rejected = row[3]
            downtime = row[4]

            achievement = round((actual / target) * 100, 2) if target > 0 else 0
            quality = round(((actual - rejected) / actual) * 100, 2) if actual > 0 else 0

            current_time = datetime.now().strftime("%H:%M:%S")

            # Production Alert
            if achievement < 95:
                alert_list.append({
                    "severity": "HIGH",
                    "line": line,
                    "message": f"Production achievement below 95% ({achievement}%)",
                    "timestamp": current_time
                })

            # Quality Alert
            if quality < 97:
                alert_list.append({
                    "severity": "MEDIUM",
                    "line": line,
                    "message": f"Quality rate below 97% ({quality}%)",
                    "timestamp": current_time
                })

            # Downtime Alert
            if downtime > 25:
                alert_list.append({
                    "severity": "HIGH",
                    "line": line,
                    "message": f"Total downtime above 25 minutes ({downtime} min)",
                    "timestamp": current_time
                })

    return {
        "alerts": alert_list
    }

@app.get("/kpi-history")
def kpi_history():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                log_date,
                COALESCE(SUM(target_units), 0) AS target,
                COALESCE(SUM(actual_units), 0) AS actual,
                COALESCE(SUM(rejected_units), 0) AS rejected,
                COALESCE(SUM(planned_downtime_min + unplanned_downtime_min), 0) AS downtime
            FROM production_logs
            GROUP BY log_date
            ORDER BY log_date;
        """))

        history = []

        for row in result:
            date = row[0]
            target = row[1]
            actual = row[2]
            rejected = row[3]
            downtime = row[4]

            achievement = round((actual / target) * 100, 2) if target > 0 else 0
            quality = round(((actual - rejected) / actual) * 100, 2) if actual > 0 else 0

            history.append({
                "date": str(date),
                "target_units": target,
                "actual_units": actual,
                "achievement_percent": achievement,
                "rejected_units": rejected,
                "quality_percent": quality,
                "downtime_min": downtime
            })

    return {"kpi_history": history}

@app.post("/production-events")
def create_production_event(event: ProductionEventCreate):

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO production_events
                (
                    line,
                    shift,
                    produced_units,
                    rejected_units,
                    downtime_minutes,
                    downtime_reason,
                    operator_name,
                    remarks
                )
                VALUES
                (
                    :line,
                    :shift,
                    :produced_units,
                    :rejected_units,
                    :downtime_minutes,
                    :downtime_reason,
                    :operator_name,
                    :remarks
                )
            """),
            {
                "line": event.line,
                "shift": event.shift,
                "produced_units": event.produced_units,
                "rejected_units": event.rejected_units,
                "downtime_minutes": event.downtime_minutes,
                "downtime_reason": event.downtime_reason,
                "operator_name": event.operator_name,
                "remarks": event.remarks
            }
        )

    return {
        "message": "Production event created successfully"
    }

@app.post("/daily-targets")
def create_daily_target(target: DailyTargetCreate):

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO daily_targets
                (
                    line,
                    shift,
                    target_units,
                    supervisor_name,
                    remarks
                )
                VALUES
                (
                    :line,
                    :shift,
                    :target_units,
                    :supervisor_name,
                    :remarks
                )
            """),
            {
                "line": target.line,
                "shift": target.shift,
                "target_units": target.target_units,
                "supervisor_name": target.supervisor_name,
                "remarks": target.remarks
            }
        )

    return {
        "message": "Daily target created successfully"
    }

@app.post("/maintenance-breakdown-events")
def create_maintenance_breakdown(event: MaintenanceBreakdownCreate):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO maintenance_breakdown_events
                (
                    shift,
                    line,
                    machine_no,
                    station,
                    problem,
                    cause,
                    action_taken,
                    engineer_name,
                    start_time,
                    end_time,
                    total_time_min,
                    line_status,
                    loto_no,
                    priority,
                    breakdown_category,
                    root_cause_category,
                    status,
                    remarks
                )
                VALUES
                (
                    :shift,
                    :line,
                    :machine_no,
                    :station,
                    :problem,
                    :cause,
                    :action_taken,
                    :engineer_name,
                    :start_time,
                    :end_time,
                    :total_time_min,
                    :line_status,
                    :loto_no,
                    :priority,
                    :breakdown_category,
                    :root_cause_category,
                    :status,
                    :remarks
                )
            """),
            {
                "shift": event.shift,
                "line": event.line,
                "machine_no": event.machine_no,
                "station": event.station,
                "problem": event.problem,
                "cause": event.cause,
                "action_taken": event.action_taken,
                "engineer_name": event.engineer_name,
                "start_time": event.start_time,
                "end_time": event.end_time,
                "total_time_min": event.total_time_min,
                "line_status": event.line_status,
                "loto_no": event.loto_no,
                "priority": event.priority,
                "breakdown_category": event.breakdown_category,
                "root_cause_category": event.root_cause_category,
                "status": event.status,
                "remarks": event.remarks,
            },
        )

    return {"message": "Maintenance breakdown event created successfully"}

@app.post("/loto-records")
def create_loto_record(record: LotoCreate):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO loto_records (
                    loto_start_time,
                    responsible_person,
                    designation,
                    department,
                    reason_for_lockout,
                    equipment_no,
                    location,
                    energy_type,
                    energy_source,
                    action_performed,
                    loto_device_issued,
                    main_energy_isolated,
                    stored_energy_released,
                    secured_against_movement,
                    completion_date,
                    completion_time,
                    status,
                    remarks
                )
                VALUES (
                    :loto_start_time,
                    :responsible_person,
                    :designation,
                    :department,
                    :reason_for_lockout,
                    :equipment_no,
                    :location,
                    :energy_type,
                    :energy_source,
                    :action_performed,
                    :loto_device_issued,
                    :main_energy_isolated,
                    :stored_energy_released,
                    :secured_against_movement,
                    :completion_date,
                    :completion_time,
                    :status,
                    :remarks
                )
            """),
            {
                "loto_start_time": record.loto_start_time,
                "responsible_person": record.responsible_person,
                "designation": record.designation,
                "department": record.department,
                "reason_for_lockout": record.reason_for_lockout,
                "equipment_no": record.equipment_no,
                "location": record.location,
                "energy_type": record.energy_type,
                "energy_source": record.energy_source,
                "action_performed": record.action_performed,
                "loto_device_issued": record.loto_device_issued,
                "main_energy_isolated": record.main_energy_isolated,
                "stored_energy_released": record.stored_energy_released,
                "secured_against_movement": record.secured_against_movement,
                "completion_date": record.completion_date,
                "completion_time": record.completion_time,
                "status": record.status,
                "remarks": record.remarks,
            },
        )

    return {"message": "LOTO record created successfully"}

@app.post("/pm-records")
def create_pm_record(record: PMRecordCreate):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO pm_records (
                    shift,
                    line,
                    machine_no,
                    start_time,
                    finish_time,
                    total_time_min,
                    due_date,
                    spare_used,
                    loto_no,
                    checklist_filled,
                    person_name,
                    pm_type,
                    status,
                    remarks
                )
                VALUES (
                    :shift,
                    :line,
                    :machine_no,
                    :start_time,
                    :finish_time,
                    :total_time_min,
                    :due_date,
                    :spare_used,
                    :loto_no,
                    :checklist_filled,
                    :person_name,
                    :pm_type,
                    :status,
                    :remarks
                )
            """),
            {
                "shift": record.shift,
                "line": record.line,
                "machine_no": record.machine_no,
                "start_time": record.start_time,
                "finish_time": record.finish_time,
                "total_time_min": record.total_time_min,
                "due_date": record.due_date,
                "spare_used": record.spare_used,
                "loto_no": record.loto_no,
                "checklist_filled": record.checklist_filled,
                "person_name": record.person_name,
                "pm_type": record.pm_type,
                "status": record.status,
                "remarks": record.remarks,
            }
        )

    return {
        "message": "PM record created successfully"
    }

@app.post("/spare-records")
def create_spare_record(record: SpareRecordCreate):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO spare_records (
                    line,
                    machine_no,
                    spare_type,
                    part_number,
                    spare_description,
                    quantity,
                    issued_to,
                    remarks
                )
                VALUES (
                    :line,
                    :machine_no,
                    :spare_type,
                    :part_number,
                    :spare_description,
                    :quantity,
                    :issued_to,
                    :remarks
                )
            """),
            {
                "line": record.line,
                "machine_no": record.machine_no,
                "spare_type": record.spare_type,
                "part_number": record.part_number,
                "spare_description": record.spare_description,
                "quantity": record.quantity,
                "issued_to": record.issued_to,
                "remarks": record.remarks,
            }
        )

    return {
        "message": "Spare record created successfully"
    }

@app.post("/manpower-records")
def create_manpower_record(record: ManpowerRecordCreate):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO manpower_records (
                    shift,
                    employee_name,
                    designation,
                    department,
                    overtime_hours,
                    remarks
                )
                VALUES (
                    :shift,
                    :employee_name,
                    :designation,
                    :department,
                    :overtime_hours,
                    :remarks
                )
            """),
            {
                "shift": record.shift,
                "employee_name": record.employee_name,
                "designation": record.designation,
                "department": record.department,
                "overtime_hours": record.overtime_hours,
                "remarks": record.remarks,
            }
        )

    return {"message": "Manpower record created successfully"}