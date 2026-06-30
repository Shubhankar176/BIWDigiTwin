from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from database import engine
from schemas import (
    ProductionEventCreate,
    DailyTargetCreate,
    MaintenanceBreakdownCreate,
    LotoCreate,
    PMRecordCreate,
    LoginRequest,
    RegisterRequest,
)

app = FastAPI(
    title="BIW Digital Twin API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "BIW Digital Twin API v2 is live"
    }

@app.post("/production-events")
def create_production_event(data: ProductionEventCreate):

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO production_events
                (
                    event_time,
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
                    NOW(),
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
                "line": data.line,
                "shift": data.shift,
                "produced_units": data.produced_units,
                "rejected_units": data.rejected_units,
                "downtime_minutes": data.downtime_minutes,
                "downtime_reason": data.downtime_reason,
                "operator_name": data.operator_name,
                "remarks": data.remarks
            }
        )

    return {
        "success": True,
        "message": "Production event saved"
    }

@app.get("/production-events")
def get_production_events():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM production_events
                ORDER BY event_time DESC
            """)
        )

        data = [dict(row._mapping) for row in result]

    return data

@app.get("/production-events")
def get_production_events():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM production_events
                ORDER BY event_time DESC
            """)
        )

        data = [dict(row._mapping) for row in result]

    return data

@app.get("/dashboard-summary")
def dashboard_summary():

    with engine.connect() as conn:

        production = conn.execute(
            text("""
                SELECT
                    COALESCE(SUM(produced_units),0) as actual_units,
                    COALESCE(SUM(rejected_units),0) as rejected_units,
                    COALESCE(SUM(downtime_minutes),0) as downtime_minutes
                FROM production_events
            """)
        ).fetchone()

        targets = conn.execute(
            text("""
                SELECT
                    COALESCE(SUM(target_units),0) as target_units
                FROM daily_targets
            """)
        ).fetchone()

    target = targets.target_units or 0
    actual = production.actual_units or 0

    achievement = 0

    if target > 0:
        achievement = round((actual / target) * 100, 2)

    return {
        "target_units": target,
        "actual_units": actual,
        "achievement_percent": achievement,
        "rejected_units": production.rejected_units,
        "downtime_minutes": production.downtime_minutes
    }

@app.post("/daily-targets")
def create_daily_target(data: DailyTargetCreate):

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO daily_targets
                (
                    target_date,
                    line,
                    shift,
                    target_units,
                    supervisor_name,
                    remarks,
                    created_at
                )
                VALUES
                (
                    CURRENT_DATE,
                    :line,
                    :shift,
                    :target_units,
                    :supervisor_name,
                    :remarks,
                    NOW()
                )
            """),
            {
                "line": data.line,
                "shift": data.shift,
                "target_units": data.target_units,
                "supervisor_name": data.supervisor_name,
                "remarks": data.remarks
            }
        )

    return {
        "success": True,
        "message": "Daily target saved"
    }


@app.get("/daily-targets")
def get_daily_targets():

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM daily_targets
                ORDER BY created_at DESC
            """)
        )

        data = [dict(row._mapping) for row in result]

    return data

@app.get("/line-summary")
def line_summary():

    with engine.connect() as conn:
        result = conn.execute(text("""
            WITH production_by_line AS (
                SELECT
                    line,
                    COALESCE(SUM(produced_units), 0) AS actual_units,
                    COALESCE(SUM(rejected_units), 0) AS rejected_units,
                    COALESCE(SUM(downtime_minutes), 0) AS downtime_minutes
                FROM production_events
                GROUP BY line
            ),
            target_by_line AS (
                SELECT
                    line,
                    COALESCE(SUM(target_units), 0) AS target_units
                FROM daily_targets
                GROUP BY line
            )
            SELECT
                COALESCE(p.line, t.line) AS line,
                COALESCE(t.target_units, 0) AS target_units,
                COALESCE(p.actual_units, 0) AS actual_units,
                COALESCE(p.rejected_units, 0) AS rejected_units,
                COALESCE(p.downtime_minutes, 0) AS downtime_minutes
            FROM production_by_line p
            FULL OUTER JOIN target_by_line t
            ON p.line = t.line
            ORDER BY line;
        """))

        data = []

        for row in result:
            target = row.target_units
            actual = row.actual_units

            achievement = 0
            if target > 0:
                achievement = round((actual / target) * 100, 2)

            data.append({
                "line": row.line,
                "target_units": target,
                "actual_units": actual,
                "achievement_percent": achievement,
                "rejected_units": row.rejected_units,
                "downtime_min": row.downtime_minutes,
            })

    return {"line_summary": data}

@app.get("/oee-summary")
def oee_summary():

    SHIFT_TIME_MIN = 480

    with engine.connect() as conn:
        result = conn.execute(text("""
            WITH production_by_line AS (
                SELECT
                    line,
                    COALESCE(SUM(produced_units), 0) AS actual_units,
                    COALESCE(SUM(rejected_units), 0) AS rejected_units,
                    COALESCE(SUM(downtime_minutes), 0) AS downtime_minutes
                FROM production_events
                GROUP BY line
            ),
            target_by_line AS (
                SELECT
                    line,
                    COALESCE(SUM(target_units), 0) AS target_units
                FROM daily_targets
                GROUP BY line
            )
            SELECT
                COALESCE(p.line, t.line) AS line,
                COALESCE(t.target_units, 0) AS target_units,
                COALESCE(p.actual_units, 0) AS actual_units,
                COALESCE(p.rejected_units, 0) AS rejected_units,
                COALESCE(p.downtime_minutes, 0) AS downtime_minutes
            FROM production_by_line p
            FULL OUTER JOIN target_by_line t
            ON p.line = t.line
            ORDER BY line;
        """))

        data = []

        for row in result:
            target = row.target_units
            actual = row.actual_units
            rejected = row.rejected_units
            downtime = row.downtime_minutes

            availability = round(((SHIFT_TIME_MIN - downtime) / SHIFT_TIME_MIN) * 100, 2)

            performance = 0
            if target > 0:
                performance = round((actual / target) * 100, 2)

            quality = 0
            if actual > 0:
                quality = round(((actual - rejected) / actual) * 100, 2)

            oee = round(
                (availability / 100) *
                (performance / 100) *
                (quality / 100) *
                100,
                2
            )

            data.append({
                "line": row.line,
                "availability_percent": availability,
                "performance_percent": performance,
                "quality_percent": quality,
                "oee_percent": oee,
                "downtime_min": downtime
            })

    return {"oee_summary": data}

@app.get("/production-trend")
def production_trend():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                DATE(event_time) AS log_date,
                COALESCE(SUM(produced_units), 0) AS actual_units,
                COALESCE(SUM(rejected_units), 0) AS rejected_units,
                COALESCE(SUM(downtime_minutes), 0) AS downtime_minutes
            FROM production_events
            GROUP BY DATE(event_time)
            ORDER BY DATE(event_time);
        """))

        data = []

        for row in result:
            data.append({
                "date": str(row.log_date),
                "actual": row.actual_units,
                "rejected": row.rejected_units,
                "downtime": row.downtime_minutes
            })

    return {"production_trend": data}

@app.get("/top-losses")
def top_losses():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                line,
                COALESCE(SUM(downtime_minutes), 0) AS downtime_minutes,
                COALESCE(SUM(rejected_units), 0) AS rejected_units
            FROM production_events
            GROUP BY line
            ORDER BY downtime_minutes DESC
            LIMIT 5;
        """))

        data = []

        for row in result:
            data.append({
                "line": row.line,
                "downtime_minutes": row.downtime_minutes,
                "rejected_units": row.rejected_units
            })

    return {"top_losses": data}

@app.get("/shift-summary")
def shift_summary():

    with engine.connect() as conn:
        result = conn.execute(text("""
            WITH production_by_shift AS (
                SELECT
                    shift,
                    COALESCE(SUM(produced_units), 0) AS actual_units,
                    COALESCE(SUM(rejected_units), 0) AS rejected_units,
                    COALESCE(SUM(downtime_minutes), 0) AS downtime_minutes
                FROM production_events
                GROUP BY shift
            ),
            target_by_shift AS (
                SELECT
                    shift,
                    COALESCE(SUM(target_units), 0) AS target_units
                FROM daily_targets
                GROUP BY shift
            )
            SELECT
                COALESCE(p.shift, t.shift) AS shift,
                COALESCE(t.target_units, 0) AS target_units,
                COALESCE(p.actual_units, 0) AS actual_units,
                COALESCE(p.rejected_units, 0) AS rejected_units,
                COALESCE(p.downtime_minutes, 0) AS downtime_minutes
            FROM production_by_shift p
            FULL OUTER JOIN target_by_shift t
            ON p.shift = t.shift
            ORDER BY shift;
        """))

        data = []

        for row in result:
            achievement = 0
            if row.target_units > 0:
                achievement = round((row.actual_units / row.target_units) * 100, 2)

            data.append({
                "shift": row.shift,
                "target": row.target_units,
                "actual": row.actual_units,
                "achievement_percent": achievement,
                "rejected": row.rejected_units,
                "downtime_min": row.downtime_minutes
            })

    return {"shift_summary": data}

@app.get("/downtime-summary")
def downtime_summary():

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                line,
                COALESCE(SUM(downtime_minutes), 0) AS downtime_minutes
            FROM production_events
            GROUP BY line
            ORDER BY downtime_minutes DESC;
        """))

        data = []

        for row in result:
            data.append({
                "line": row.line,
                "planned_downtime": 0,
                "unplanned_downtime": row.downtime_minutes,
                "total_downtime": row.downtime_minutes
            })

    return {"downtime_summary": data}

@app.post("/maintenance-breakdowns")
def create_maintenance_breakdown(data: MaintenanceBreakdownCreate):

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO maintenance_breakdown_events
                (
                    event_time,
                    log_date,
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
                    remarks,
                    breakdown_category,
                    root_cause_category,
                    status
                )
                VALUES
                (
                    NOW(),
                    CURRENT_DATE,
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
                    :remarks,
                    :breakdown_category,
                    :root_cause_category,
                    :status
                )
            """),
            {
                "shift": data.shift,
                "line": data.line,
                "machine_no": data.machine_no,
                "station": data.station,
                "problem": data.problem,
                "cause": data.cause,
                "action_taken": data.action_taken,
                "engineer_name": data.engineer_name,
                "start_time": data.start_time,
                "end_time": data.end_time,
                "total_time_min": data.total_time_min,
                "line_status": data.line_status,
                "loto_no": data.loto_no,
                "remarks": data.remarks,
                "breakdown_category": data.breakdown_category,
                "root_cause_category": data.root_cause_category,
                "status": data.status,
            }
        )

    return {
        "success": True,
        "message": "Maintenance breakdown saved"
    }


@app.get("/maintenance-breakdowns")
def get_maintenance_breakdowns():

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM maintenance_breakdown_events
                ORDER BY event_time DESC
            """)
        )

        data = [dict(row._mapping) for row in result]

    return data

@app.post("/loto-records")
def create_loto_record(data: LotoCreate):

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO loto_records
                (
                    created_at,
                    loto_start_date,
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
                VALUES
                (
                    NOW(),
                    CURRENT_DATE,
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
                "loto_start_time": data.loto_start_time,
                "responsible_person": data.responsible_person,
                "designation": data.designation,
                "department": data.department,
                "reason_for_lockout": data.reason_for_lockout,
                "equipment_no": data.equipment_no,
                "location": data.location,
                "energy_type": data.energy_type,
                "energy_source": data.energy_source,
                "action_performed": data.action_performed,
                "loto_device_issued": data.loto_device_issued,
                "main_energy_isolated": data.main_energy_isolated,
                "stored_energy_released": data.stored_energy_released,
                "secured_against_movement": data.secured_against_movement,
                "completion_date": data.completion_date,
                "completion_time": data.completion_time,
                "status": data.status,
                "remarks": data.remarks,
            }
        )

    return {
        "success": True,
        "message": "LOTO record saved"
    }


@app.get("/loto-records")
def get_loto_records():

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM loto_records
                ORDER BY created_at DESC
            """)
        )

        data = [dict(row._mapping) for row in result]

    return data

@app.post("/pm-records")
def create_pm_record(data: PMRecordCreate):

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO pm_records
                (
                    created_at,
                    pm_date,
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
                    status,
                    remarks
                )
                VALUES
                (
                    NOW(),
                    CURRENT_DATE,
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
                    :status,
                    :remarks
                )
            """),
            {
                "shift": data.shift,
                "line": data.line,
                "machine_no": data.machine_no,
                "start_time": data.start_time,
                "finish_time": data.finish_time,
                "total_time_min": data.total_time_min,
                "due_date": data.due_date,
                "spare_used": data.spare_used,
                "loto_no": data.loto_no,
                "checklist_filled": data.checklist_filled,
                "person_name": data.person_name,
                "status": data.status,
                "remarks": data.remarks,
            }
        )

    return {
        "success": True,
        "message": "PM record saved"
    }


@app.get("/pm-records")
def get_pm_records():

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM pm_records
                ORDER BY created_at DESC
            """)
        )

        data = [dict(row._mapping) for row in result]

    return data

@app.get("/live-logs")
def live_logs():

    with engine.connect() as conn:

        production = conn.execute(text("""
            SELECT
                event_time AS time,
                'Production' AS module,
                line,
                shift,
                CONCAT(
                    'Produced: ', produced_units,
                    ', Rejected: ', rejected_units,
                    ', Downtime: ', downtime_minutes, ' min'
                ) AS description,
                COALESCE(operator_name, '') AS person
            FROM production_events
        """))

        maintenance = conn.execute(text("""
            SELECT
                event_time AS time,
                'Breakdown' AS module,
                line,
                shift,
                CONCAT(
                    machine_no, ' - ', problem,
                    ' | Downtime: ', total_time_min, ' min'
                ) AS description,
                COALESCE(engineer_name, '') AS person
            FROM maintenance_breakdown_events
        """))

        pm = conn.execute(text("""
            SELECT
                created_at AS time,
                'Preventive Maintenance' AS module,
                line,
                shift,
                CONCAT(
                    machine_no, ' PM completed | Time: ', total_time_min, ' min'
                ) AS description,
                COALESCE(person_name, '') AS person
            FROM pm_records
        """))

        loto = conn.execute(text("""
            SELECT
                created_at AS time,
                'LOTO' AS module,
                location AS line,
                '' AS shift,
                CONCAT(
                    equipment_no, ' - ', reason_for_lockout,
                    ' | Status: ', status
                ) AS description,
                COALESCE(responsible_person, '') AS person
            FROM loto_records
        """))

        logs = []

        for result in [production, maintenance, pm, loto]:
            for row in result:
                logs.append(dict(row._mapping))

        logs.sort(key=lambda x: x["time"], reverse=True)

    return {"live_logs": logs[:50]}

@app.get("/maintenance-kpis")
def maintenance_kpis():

    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT
                COUNT(*) AS total_breakdowns,
                COALESCE(SUM(total_time_min), 0) AS total_repair_time,
                COALESCE(AVG(total_time_min), 0) AS mttr,
                COALESCE(480.0 / NULLIF(COUNT(*), 0), 0) AS mtbf
            FROM maintenance_breakdown_events
            WHERE total_time_min IS NOT NULL;
        """)).fetchone()

    return {
        "total_breakdowns": row.total_breakdowns,
        "total_repair_time_min": row.total_repair_time,
        "mttr_min": round(row.mttr, 2),
        "mtbf_min": round(row.mtbf, 2)
    }

@app.post("/login")
def login(data: LoginRequest):
    username = data.username.strip()
    password = data.password.strip()

    with engine.connect() as conn:
        user = conn.execute(
            text("""
                SELECT username
                FROM users
                WHERE LOWER(TRIM(username)) = LOWER(:username)
                AND TRIM(password) = :password
            """),
            {
                "username": username,
                "password": password,
            },
        ).fetchone()

    if user:
        return {
            "success": True,
            "username": user.username
        }

    return {
        "success": False,
        "message": "Invalid username or password"
    }

@app.post("/register")
def register(data: RegisterRequest):
    username = data.username.strip()
    password = data.password.strip()

    if not username or not password:
        return {
            "success": False,
            "message": "Name and password are required"
        }

    with engine.begin() as conn:
        existing_user = conn.execute(
            text("""
                SELECT id
                FROM users
                WHERE LOWER(TRIM(username)) = LOWER(:username)
            """),
            {"username": username}
        ).fetchone()

        if existing_user:
            return {
                "success": False,
                "message": "User already exists"
            }

        conn.execute(
            text("""
                INSERT INTO users (username, password)
                VALUES (:username, :password)
            """),
            {
                "username": username,
                "password": password
            }
        )

    return {
        "success": True,
        "message": "User created successfully",
        "username": username
    }

@app.get("/kpi-history")
def kpi_history():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                log_date,
                COALESCE(SUM(produced_units), 0) AS actual_units,
                COALESCE(SUM(rejected_units), 0) AS rejected_units,
                COALESCE(SUM(downtime_minutes), 0) AS downtime_minutes
            FROM production_events
            GROUP BY log_date
            ORDER BY log_date;
        """))

        data = []

        for row in result:
            actual = row.actual_units or 0
            rejected = row.rejected_units or 0
            total = actual + rejected

            quality = round((actual / total) * 100, 2) if total > 0 else 0

            data.append({
                "date": row.log_date.strftime("%m/%d"),
                "actual_units": actual,
                "rejected_units": rejected,
                "downtime_minutes": row.downtime_minutes,
                "achievement_percent": quality
            })

    return {"kpi_history": data}