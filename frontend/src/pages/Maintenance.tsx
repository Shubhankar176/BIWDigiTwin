import { useState } from "react";
import {
  createMaintenanceBreakdown,
  createLotoRecord,
  createPMRecord,
  createSpareRecord,
  createManpowerRecord
} from "../services/api";

type MaintenanceTab = "breakdown" | "pm" | "loto" ;

type Props = {
  workerMode?: boolean;
  defaultTab?: MaintenanceTab;
};
export default function Maintenance({
  workerMode=false,
  defaultTab="breakdown",
}:Props){
  const[activeTab, setActiveTab]=useState<MaintenanceTab>(defaultTab);


  const [breakdownForm, setBreakdownForm] = useState({
    shift: "A",
    line: "SIGNA Main Line",
    machine_no: "",
    station: "",
    problem: "",
    cause: "",
    action_taken: "",
    engineer_name: "",
    start_time: "",
    end_time: "",
    total_time_min: "",
    line_status: "Stopped",
    loto_no: "",
    breakdown_category: "Robot",
    root_cause_category: "Sensor",
    status: "Closed",
    remarks: "",
  });

  const [lotoForm, setLotoForm] = useState({
    loto_start_time: "",
    responsible_person: "",
    designation: "",
    department: "",
    reason_for_lockout: "",
    equipment_no: "",
    location: "",
    energy_type: "Electrical",
    energy_source: "",
    action_performed: "",
    loto_device_issued: "",
    main_energy_isolated: false,
    stored_energy_released: false,
    secured_against_movement: false,
    completion_date: "",
    completion_time: "",
    status: "Open",
    remarks: "",
  });

  const [pmForm, setPmForm] = useState({
  shift: "A",
  line: "SIGNA Main Line",
  machine_no: "",

  start_time: "",
  finish_time: "",
  total_time_min: "",

  due_date: "",

  spare_used: false,
  loto_no: "",
  checklist_filled: false,

  person_name: "",

  pm_type: "Weekly",
  status: "Completed",

  remarks: "",
});

const [spareForm, setSpareForm] = useState({
  line: "SIGNA Main Line",
  machine_no: "",

  spare_type: "Consumed",

  part_number: "",
  spare_description: "",

  quantity: "",

  issued_to: "",
  remarks: "",
});

const [manpowerForm, setManpowerForm] = useState({
  shift: "A",
  employee_name: "",
  designation: "",
  department: "Maintenance",
  overtime_hours: "",
  remarks: "",
});

const calculateMinutes = (start: string, end: string) => {
  if (!start || !end) return "";

  const [startHour, startMinute] = start.split(":").map(Number);
  const [endHour, endMinute] = end.split(":").map(Number);

  const startTotal = startHour * 60 + startMinute;
  const endTotal = endHour * 60 + endMinute;

  return String(endTotal - startTotal);
};

  const saveBreakdown = async () => {
    if (!breakdownForm.machine_no || !breakdownForm.problem) {
      alert("Machine No and Problem are required");
      return;
    }

    try {
      await createMaintenanceBreakdown({
        ...breakdownForm,
        total_time_min: Number(breakdownForm.total_time_min || 0),
      });

      alert("Breakdown Entry Saved");

      setBreakdownForm({
        shift: "A",
        line: "SIGNA Main Line",
        machine_no: "",
        station: "",
        problem: "",
        cause: "",
        action_taken: "",
        engineer_name: "",
        start_time: "",
        end_time: "",
        total_time_min: "",
        line_status: "Stopped",
        loto_no: "",
        breakdown_category: "Robot",
        root_cause_category: "Sensor",
        status: "Closed",
        remarks: "",
      });
    } catch (error) {
      console.error(error);
      alert("Save Failed");
    }
  };

  const saveLoto = async () => {
    if (!lotoForm.responsible_person || !lotoForm.equipment_no) {
      alert("Responsible Person and Equipment No are required");
      return;
    }

    try {
      await createLotoRecord(lotoForm);

      alert("LOTO Record Saved");

      setLotoForm({
        loto_start_time: "",
        responsible_person: "",
        designation: "",
        department: "",
        reason_for_lockout: "",
        equipment_no: "",
        location: "",
        energy_type: "Electrical",
        energy_source: "",
        action_performed: "",
        loto_device_issued: "",
        main_energy_isolated: false,
        stored_energy_released: false,
        secured_against_movement: false,
        completion_date: "",
        completion_time: "",
        status: "Open",
        remarks: "",
      });
    } catch (error) {
      console.error(error);
      alert("Save Failed");
    }
  };
  const savePM = async () => {
  if (!pmForm.machine_no) {
    alert("Machine No is required");
    return;
  }

  try {
    await createPMRecord({
      ...pmForm,
      total_time_min: Number(pmForm.total_time_min || 0),
    });

    alert("PM Record Saved");

    setPmForm({
      shift: "A",
      line: "SIGNA Main Line",
      machine_no: "",

      start_time: "",
      finish_time: "",
      total_time_min: "",

      due_date: "",

      spare_used: false,
      loto_no: "",
      checklist_filled: false,

      person_name: "",

      pm_type: "Weekly",
      status: "Completed",

      remarks: "",
    });
  } catch (error) {
    console.error(error);
    alert("Save Failed");
  }
};
  const saveSpare = async () => {
  if (!spareForm.part_number) {
    alert("Part Number is required");
    return;
  }

  try {
    await createSpareRecord({
      ...spareForm,
      quantity: Number(spareForm.quantity || 0),
    });  

    alert("Spare Record Saved");

    setSpareForm({
      line: "SIGNA Main Line",
      machine_no: "",
      spare_type: "Consumed",
      part_number: "",
      spare_description: "",
      quantity: "",
      issued_to: "",
      remarks: "",
    });
  } catch (error) {
    console.error(error);
    alert("Save Failed");
  }
};
  const saveManpower = async () => {
  if (!manpowerForm.employee_name) {
    alert("Employee Name is required");
    return;
  }

  try {
    await createManpowerRecord({
      ...manpowerForm,
      overtime_hours: Number(manpowerForm.overtime_hours || 0),
    });

    alert("Manpower Record Saved");

    setManpowerForm({
      shift: "A",
      employee_name: "",
      designation: "",
      department: "",
      overtime_hours: "",
      remarks: "",
    });
  } catch (error) {
    console.error(error);
    alert("Save Failed");
  }
};
  return (
    <div className="operations-page">
      <div className="page-header">
        <h1>Maintenance Data Entry</h1>
        <p>Digital replacement for BIW maintenance, breakdown and LOTO registers.</p>
      </div>

      <div className="form-tabs">
        <button className={activeTab === "breakdown" ? "active" : ""} onClick={() => setActiveTab("breakdown")}>
          Breakdown Entry
        </button>
        <button className={activeTab === "pm" ? "active" : ""} onClick={() => setActiveTab("pm")}>
          Preventive Maintenance
        </button>
        <button className={activeTab === "loto" ? "active" : ""} onClick={() => setActiveTab("loto")}>
          LOTO Register
        </button>
      </div>

      <div className="form-panel">
        {activeTab === "breakdown" && (
          <>
            <h2>Breakdown Entry</h2>

            <div className="form-grid">
              <div>
                <label>Line</label>
                <select value={breakdownForm.line} onChange={(e) => setBreakdownForm({ ...breakdownForm, line: e.target.value })}>
                  <option>SIGNA Main Line</option>
                  <option>SIGNA MFL</option>
                  <option>ILCV Main Line</option>
                  <option>ILCV MFL</option>
                </select>
              </div>

              <div>
                <label>Shift</label>
                <select value={breakdownForm.shift} onChange={(e) => setBreakdownForm({ ...breakdownForm, shift: e.target.value })}>
                  <option>A</option>
                  <option>B</option>
                  <option>C</option>
                  <option>G</option>
                </select>
              </div>

              <div><label>Machine No</label><input value={breakdownForm.machine_no} onChange={(e) => setBreakdownForm({ ...breakdownForm, machine_no: e.target.value })} /></div>
              <div><label>Station</label><input value={breakdownForm.station} onChange={(e) => setBreakdownForm({ ...breakdownForm, station: e.target.value })} /></div>
              <div><label>Problem</label><input value={breakdownForm.problem} onChange={(e) => setBreakdownForm({ ...breakdownForm, problem: e.target.value })} /></div>
              <div><label>Cause</label><input value={breakdownForm.cause} onChange={(e) => setBreakdownForm({ ...breakdownForm, cause: e.target.value })} /></div>
              <div><label>Action Taken</label><input value={breakdownForm.action_taken} onChange={(e) => setBreakdownForm({ ...breakdownForm, action_taken: e.target.value })} /></div>
              <div><label>Engineer Name</label><input value={breakdownForm.engineer_name} onChange={(e) => setBreakdownForm({ ...breakdownForm, engineer_name: e.target.value })} /></div>
              <div><label>Start Time</label><input type="time" value={breakdownForm.start_time} 
              onChange={(e) => {
                const startTime = e.target.value;

                setBreakdownForm({
                  ...breakdownForm,
                  start_time: startTime,
                  total_time_min: calculateMinutes(
                    startTime,
                    breakdownForm.end_time
                  ),
                });
              }} /></div>
              <div><label>End Time</label><input type="time" value={breakdownForm.end_time} 
              onChange={(e) => {
                const endTime = e.target.value;

                setBreakdownForm({
                ...breakdownForm,
                end_time: endTime,
                total_time_min: calculateMinutes(
                  breakdownForm.start_time,
                  endTime
                ),
                });
              }}
              /></div>
              <div><label>Total Time (min)</label><input type="number" value={breakdownForm.total_time_min} readOnly /></div>

              <div>
                <label>Line Status</label>
                <select value={breakdownForm.line_status} onChange={(e) => setBreakdownForm({ ...breakdownForm, line_status: e.target.value })}>
                  <option>Running</option>
                  <option>Stopped</option>
                  <option>Under Maintenance</option>
                </select>
              </div>

              <div><label>LOTO No</label><input value={breakdownForm.loto_no} onChange={(e) => setBreakdownForm({ ...breakdownForm, loto_no: e.target.value })} /></div>

              <div>
                <label>Breakdown Category</label>
                <select value={breakdownForm.breakdown_category} onChange={(e) => setBreakdownForm({ ...breakdownForm, breakdown_category: e.target.value })}>
                  <option>Robot</option>
                  <option>Welding</option>
                  <option>Conveyor</option>
                  <option>Fixture</option>
                  <option>Electrical</option>
                  <option>Pneumatic</option>
                  <option>Hydraulic</option>
                  <option>PLC</option>
                  <option>Safety</option>
                  <option>Utility</option>
                  <option>Others</option>
                </select>
              </div>

              <div>
                <label>Root Cause Category</label>
                <select value={breakdownForm.root_cause_category} onChange={(e) => setBreakdownForm({ ...breakdownForm, root_cause_category: e.target.value })}>
                  <option>Sensor</option>
                  <option>Mechanical Wear</option>
                  <option>Electrical Fault</option>
                  <option>PLC Logic</option>
                  <option>Air Pressure</option>
                  <option>Material Issue</option>
                  <option>Operator Error</option>
                  <option>Others</option>
                </select>
              </div>

              <div>
                <label>Status</label>
                <select value={breakdownForm.status} onChange={(e) => setBreakdownForm({ ...breakdownForm, status: e.target.value })}>
                  <option>Open</option>
                  <option>In Progress</option>
                  <option>Closed</option>
                </select>
              </div>

              <div><label>Remarks</label><input value={breakdownForm.remarks} onChange={(e) => setBreakdownForm({ ...breakdownForm, remarks: e.target.value })} /></div>
            </div>

            <button className="save-btn" onClick={saveBreakdown}>Save Breakdown Entry</button>
          </>
        )}

        {activeTab === "loto" && (
          <>
            <h2>LOTO Register</h2>

            <div className="form-grid">
              <div><label>LOTO Start Time</label><input type="time" value={lotoForm.loto_start_time} onChange={(e) => setLotoForm({ ...lotoForm, loto_start_time: e.target.value })} /></div>
              <div><label>Responsible Person</label><input value={lotoForm.responsible_person} onChange={(e) => setLotoForm({ ...lotoForm, responsible_person: e.target.value })} /></div>
              <div><label>Designation</label><input value={lotoForm.designation} onChange={(e) => setLotoForm({ ...lotoForm, designation: e.target.value })} /></div>
              <div><label>Department</label><input value={lotoForm.department} onChange={(e) => setLotoForm({ ...lotoForm, department: e.target.value })} /></div>
              <div><label>Reason for Lockout</label><input value={lotoForm.reason_for_lockout} onChange={(e) => setLotoForm({ ...lotoForm, reason_for_lockout: e.target.value })} /></div>
              <div><label>Equipment No</label><input value={lotoForm.equipment_no} onChange={(e) => setLotoForm({ ...lotoForm, equipment_no: e.target.value })} /></div>
              <div><label>Location</label><input value={lotoForm.location} onChange={(e) => setLotoForm({ ...lotoForm, location: e.target.value })} /></div>

              <div>
                <label>Energy Type</label>
                <select value={lotoForm.energy_type} onChange={(e) => setLotoForm({ ...lotoForm, energy_type: e.target.value })}>
                  <option>Electrical</option>
                  <option>Pneumatic</option>
                  <option>Chemical</option>
                  <option>Mechanical</option>
                  <option>Hydraulic</option>
                  <option>Others</option>
                </select>
              </div>

              <div><label>Energy Source</label><input value={lotoForm.energy_source} onChange={(e) => setLotoForm({ ...lotoForm, energy_source: e.target.value })} /></div>
              <div><label>Action Performed</label><input value={lotoForm.action_performed} onChange={(e) => setLotoForm({ ...lotoForm, action_performed: e.target.value })} /></div>
              <div><label>LOTO Device Issued</label><input value={lotoForm.loto_device_issued} onChange={(e) => setLotoForm({ ...lotoForm, loto_device_issued: e.target.value })} /></div>

              <div>
                <label>Main Energy Isolated</label>
                <input type="checkbox" checked={lotoForm.main_energy_isolated} onChange={(e) => setLotoForm({ ...lotoForm, main_energy_isolated: e.target.checked })} />
              </div>

              <div>
                <label>Stored Energy Released</label>
                <input type="checkbox" checked={lotoForm.stored_energy_released} onChange={(e) => setLotoForm({ ...lotoForm, stored_energy_released: e.target.checked })} />
              </div>

              <div>
                <label>Secured Against Movement</label>
                <input type="checkbox" checked={lotoForm.secured_against_movement} onChange={(e) => setLotoForm({ ...lotoForm, secured_against_movement: e.target.checked })} />
              </div>

              <div><label>Completion Date</label><input type="date" value={lotoForm.completion_date} onChange={(e) => setLotoForm({ ...lotoForm, completion_date: e.target.value })} /></div>
              <div><label>Completion Time</label><input type="time" value={lotoForm.completion_time} onChange={(e) => setLotoForm({ ...lotoForm, completion_time: e.target.value })} /></div>

              <div>
                <label>Status</label>
                <select value={lotoForm.status} onChange={(e) => setLotoForm({ ...lotoForm, status: e.target.value })}>
                  <option>Open</option>
                  <option>Incomplete</option>
                  <option>Complete</option>
                  <option>Closed</option>
                </select>
              </div>

              <div><label>Remarks</label><input value={lotoForm.remarks} onChange={(e) => setLotoForm({ ...lotoForm, remarks: e.target.value })} /></div>
            </div>

            <button className="save-btn" onClick={saveLoto}>Save LOTO Record</button>
          </>
        )}

        {activeTab === "pm" && (
  <>
    <h2>Preventive Maintenance</h2>

    <div className="form-grid">
      <div>
        <label>Line</label>
        <select
          value={pmForm.line}
          onChange={(e) =>
            setPmForm({ ...pmForm, line: e.target.value })
          }
        >
          <option>SIGNA Main Line</option>
          <option>SIGNA MFL</option>
          <option>ILCV Main Line</option>
          <option>ILCV MFL</option>
        </select>
      </div>

      <div>
        <label>Shift</label>
        <select
          value={pmForm.shift}
          onChange={(e) =>
            setPmForm({ ...pmForm, shift: e.target.value })
          }
        >
          <option>A</option>
          <option>B</option>
          <option>C</option>
          <option>G</option>
        </select>
      </div>

      <div>
        <label>Machine No</label>
        <input
          value={pmForm.machine_no}
          onChange={(e) =>
            setPmForm({ ...pmForm, machine_no: e.target.value })
          }
        />
      </div>

      <div>
        <label>Start Time</label>
        <input
          type="time"
          value={pmForm.start_time}
          onChange={(e) => {
            const startTime = e.target.value;

            setPmForm({
              ...pmForm,
              start_time: startTime,
              total_time_min: calculateMinutes(
                startTime,
                pmForm.finish_time
              ),
            });
         }}
        />
      </div>

      <div>
        <label>Finish Time</label>
        <input
          type="time"
          value={pmForm.finish_time}
          onChange={(e) => {
            const endTime = e.target.value;

            setPmForm({
              ...pmForm,
              finish_time: endTime,
              total_time_min: calculateMinutes(
                pmForm.start_time,
                endTime
              ),
            });
          }}
        />
      </div>

      <div>
        <label>Total Time (min)</label>
        <input
          type="number"
          value={pmForm.total_time_min}
          onChange={(e) =>
            setPmForm({
              ...pmForm,
              total_time_min: e.target.value,
            })
          }
        />
      </div>

      <div>
        <label>Due Date</label>
        <input
          type="date"
          value={pmForm.due_date}
          onChange={(e) =>
            setPmForm({ ...pmForm, due_date: e.target.value })
          }
        />
      </div>

      <div>
        <label>LOTO No</label>
        <input
          value={pmForm.loto_no}
          onChange={(e) =>
            setPmForm({ ...pmForm, loto_no: e.target.value })
          }
        />
      </div>

      <div>
        <label>Technician Name</label>
        <input
          value={pmForm.person_name}
          onChange={(e) =>
            setPmForm({
              ...pmForm,
              person_name: e.target.value,
            })
          }
        />
      </div>
      <div>
        <label>Status</label>
        <select
          value={pmForm.status}
          onChange={(e) =>
            setPmForm({ ...pmForm, status: e.target.value })
          }
        >
          <option>Scheduled</option>
          <option>In Progress</option>
          <option>Completed</option>
          <option>Overdue</option>
        </select>
      </div>

      <div>
        <label>Spare Used</label>
        <input
          type="checkbox"
          checked={pmForm.spare_used}
          onChange={(e) =>
            setPmForm({
              ...pmForm,
              spare_used: e.target.checked,
            })
          }
        />
      </div>

      <div>
        <label>Checklist Filled</label>
        <input
          type="checkbox"
          checked={pmForm.checklist_filled}
          onChange={(e) =>
            setPmForm({
              ...pmForm,
              checklist_filled: e.target.checked,
            })
          }
        />
      </div>

      <div>
        <label>Remarks</label>
        <input
          value={pmForm.remarks}
          onChange={(e) =>
            setPmForm({ ...pmForm, remarks: e.target.value })
          }
        />
      </div>
    </div>

    <button className="save-btn" onClick={savePM}>
      Save PM Record
    </button>
  </>
)}
        {activeTab === "spares" && (
  <>
    <h2>Spare Management</h2>

    <div className="form-grid">
      <div>
        <label>Line</label>
        <select
          value={spareForm.line}
          onChange={(e) =>
            setSpareForm({ ...spareForm, line: e.target.value })
          }
        >
          <option>SIGNA Main Line</option>
          <option>SIGNA MFL</option>
          <option>ILCV Main Line</option>
          <option>ILCV MFL</option>
        </select>
      </div>

      <div>
        <label>Machine No</label>
        <input
          value={spareForm.machine_no}
          onChange={(e) =>
            setSpareForm({
              ...spareForm,
              machine_no: e.target.value,
            })
          }
        />
      </div>

      <div>
        <label>Spare Type</label>
        <select
          value={spareForm.spare_type}
          onChange={(e) =>
            setSpareForm({
              ...spareForm,
              spare_type: e.target.value,
            })
          }
        >
          <option>Consumed</option>
          <option>Required</option>
          <option>Reserved</option>
        </select>
      </div>

      <div>
        <label>Part Number</label>
        <input
          value={spareForm.part_number}
          onChange={(e) =>
            setSpareForm({
              ...spareForm,
              part_number: e.target.value,
            })
          }
        />
      </div>

      <div>
        <label>Description</label>
        <input
          value={spareForm.spare_description}
          onChange={(e) =>
            setSpareForm({
              ...spareForm,
              spare_description: e.target.value,
            })
          }
        />
      </div>

      <div>
        <label>Quantity</label>
        <input
          type="number"
          value={spareForm.quantity}
          onChange={(e) =>
            setSpareForm({
              ...spareForm,
              quantity: e.target.value,
            })
          }
        />
      </div>

      <div>
        <label>Issued To</label>
        <input
          value={spareForm.issued_to}
          onChange={(e) =>
            setSpareForm({
              ...spareForm,
              issued_to: e.target.value,
            })
          }
        />
      </div>

      <div>
        <label>Remarks</label>
        <input
          value={spareForm.remarks}
          onChange={(e) =>
            setSpareForm({
              ...spareForm,
              remarks: e.target.value,
            })
          }
        />
      </div>
    </div>

    <button className="save-btn" onClick={saveSpare}>
      Save Spare Record
    </button>
  </>
)}
        {activeTab === "manpower" && (
  <>
    <h2>Manpower Entry</h2>

    <div className="form-grid">
      <div>
        <label>Shift</label>
        <select
          value={manpowerForm.shift}
          onChange={(e) =>
            setManpowerForm({ ...manpowerForm, shift: e.target.value })
          }
        >
          <option>A</option>
          <option>B</option>
          <option>C</option>
          <option>G</option>
        </select>
      </div>

      <div>
        <label>Employee Name</label>
        <input
          value={manpowerForm.employee_name}
          onChange={(e) =>
            setManpowerForm({
              ...manpowerForm,
              employee_name: e.target.value,
            })
          }
        />
      </div>

      <div>
        <label>Designation</label>
        <input
          value={manpowerForm.designation}
          onChange={(e) =>
            setManpowerForm({
              ...manpowerForm,
              designation: e.target.value,
            })
          }
        />
      </div>

      <div>
        <label>Department</label>
        <input
          value={manpowerForm.department}
          onChange={(e) =>
            setManpowerForm({
              ...manpowerForm,
              department: e.target.value,
            })
          }
        />
      </div>

      <div>
        <label>Overtime Hours</label>
        <input
          type="number"
          value={manpowerForm.overtime_hours}
          onChange={(e) =>
            setManpowerForm({
              ...manpowerForm,
              overtime_hours: e.target.value,
            })
          }
        />
      </div>

      <div>
        <label>Remarks</label>
        <input
          value={manpowerForm.remarks}
          onChange={(e) =>
            setManpowerForm({
              ...manpowerForm,
              remarks: e.target.value,
            })
          }
        />
      </div>
    </div>

    <button className="save-btn" onClick={saveManpower}>
      Save Manpower Record
    </button>
  </>
)}
      </div>
    </div>
  );
}