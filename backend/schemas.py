from pydantic import BaseModel
from typing import Optional


class ProductionEventCreate(BaseModel):
    line: str
    shift: str
    produced_units: int
    rejected_units: int = 0
    downtime_minutes: int = 0
    downtime_reason: Optional[str] = None
    operator_name: Optional[str] = None
    remarks: Optional[str] = None


class DailyTargetCreate(BaseModel):
    line: str
    shift: str
    target_units: int
    supervisor_name: Optional[str] = None
    remarks: Optional[str] = None


class MaintenanceBreakdownCreate(BaseModel):
    shift: str
    line: str
    machine_no: str
    station: Optional[str] = None

    problem: str
    cause: Optional[str] = None
    action_taken: Optional[str] = None

    engineer_name: Optional[str] = None

    start_time: Optional[str] = None
    end_time: Optional[str] = None
    total_time_min: int = 0

    line_status: Optional[str] = None
    loto_no: Optional[str] = None

    breakdown_category: Optional[str] = None
    root_cause_category: Optional[str] = None

    status: str = "Closed"
    remarks: Optional[str] = None


class LotoCreate(BaseModel):
    loto_start_time: Optional[str] = None

    responsible_person: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None

    reason_for_lockout: Optional[str] = None

    equipment_no: Optional[str] = None
    location: Optional[str] = None

    energy_type: Optional[str] = None
    energy_source: Optional[str] = None

    action_performed: Optional[str] = None
    loto_device_issued: Optional[str] = None

    main_energy_isolated: bool = False
    stored_energy_released: bool = False
    secured_against_movement: bool = False

    completion_date: Optional[str] = None
    completion_time: Optional[str] = None

    status: str = "Open"
    remarks: Optional[str] = None


class PMRecordCreate(BaseModel):
    shift: str
    line: Optional[str] = None
    machine_no: str

    start_time: Optional[str] = None
    finish_time: Optional[str] = None
    total_time_min: int = 0

    due_date: Optional[str] = None

    spare_used: bool = False
    loto_no: Optional[str] = None
    checklist_filled: bool = False

    person_name: Optional[str] = None

    status: str = "Completed"
    remarks: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username:str
    password:str
    