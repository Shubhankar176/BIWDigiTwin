from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class MaintenanceBreakdownCreate(BaseModel):
    log_date: date

    shift: str

    line: Optional[str] = None
    machine_no: Optional[str] = None
    station: Optional[str] = None

    problem: str
    cause: Optional[str] = None
    action_taken: Optional[str] = None

    engineer_name: Optional[str] = None

    start_time: Optional[time] = None
    end_time: Optional[time] = None
    total_time_min: Optional[int] = None

    line_status: Optional[str] = None
    loto_no: Optional[str] = None

    remarks: Optional[str] = None

class DailyTargetCreate(BaseModel):
    line: str
    shift: str
    target_units: int
    supervisor_name: str | None = None
    remarks: str | None = None   

class MaintenanceBreakdownCreate(BaseModel):
    shift: str
    line: str
    machine_no: str
    station: str

    problem: str
    cause: str
    action_taken: str

    engineer_name: str

    start_time: str
    end_time: str
    total_time_min: int

    line_status: str
    loto_no: str

    priority: str
    breakdown_category: str
    root_cause_category: str

    status: str
    remarks: str 

class LotoCreate(BaseModel):
    loto_start_time: str | None = None

    responsible_person: str | None = None
    designation: str | None = None
    department: str | None = None

    reason_for_lockout: str | None = None

    equipment_no: str | None = None
    location: str | None = None

    energy_type: str | None = None
    energy_source: str | None = None

    action_performed: str | None = None
    loto_device_issued: str | None = None

    main_energy_isolated: bool = False
    stored_energy_released: bool = False
    secured_against_movement: bool = False

    completion_date: str | None = None
    completion_time: str | None = None

    status: str = "Open"
    remarks: str | None = None

class PMRecordCreate(BaseModel):
    shift: str
    line: str | None = None
    machine_no: str

    start_time: str | None = None
    finish_time: str | None = None
    total_time_min: int | None = None

    due_date: str | None = None

    spare_used: bool = False
    loto_no: str | None = None
    checklist_filled: bool = False

    person_name: str | None = None

    pm_type: str | None = None
    status: str = "Completed"

    remarks: str | None = None

class SpareRecordCreate(BaseModel):
    line: str | None = None
    machine_no: str | None = None

    spare_type: str

    part_number: str | None = None
    spare_description: str | None = None

    quantity: int = 0

    issued_to: str | None = None
    remarks: str | None = None

class ManpowerRecordCreate(BaseModel):
    shift: str | None = None

    employee_name: str

    designation: str | None = None
    department: str | None = None

    overtime_hours: float = 0

    remarks: str | None = None