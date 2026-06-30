import { useState } from "react";
import { createProductionEntry, createDailyTarget } from "../services/api";

type FormTab = "production" | "downtime" | "target";

export default function Operations() {
  const [activeForm, setActiveForm] = useState<FormTab>("production");

  const [productionForm, setProductionForm] = useState({
    line: "SIGNA Main Line",
    shift: "A",
    produced_units: "",
    rejected_units: "",
    operator_name: "",
    remarks: "",
  });

  const [downtimeForm, setDowntimeForm] = useState({
    line: "SIGNA Main Line",
    shift: "A",
    downtime_minutes: "",
    downtime_reason: "Robot Fault",
    operator_name: "",
    remarks: "",
  });

  const [targetForm, setTargetForm] = useState({
    line: "SIGNA Main Line",
    shift: "A",
    target_units: "",
    supervisor_name: "",
    remarks: "",
  });

  const saveProduction = async () => {
    if (!productionForm.produced_units) {
      alert("Please enter Produced Units");
      return;
    }

    try {
      await createProductionEntry({
        line: productionForm.line,
        shift: productionForm.shift,
        produced_units: Number(productionForm.produced_units),
        rejected_units: Number(productionForm.rejected_units || 0),
        downtime_minutes: 0,
        downtime_reason: "",
        operator_name: productionForm.operator_name,
        remarks: productionForm.remarks,
      });

      alert("Production Entry Saved");

      setProductionForm({
        line: "SIGNA Main Line",
        shift: "A",
        produced_units: "",
        rejected_units: "",
        operator_name: "",
        remarks: "",
      });
    } catch (error) {
      console.error(error);
      alert("Save Failed");
    }
  };

  const saveDowntime = async () => {
    if (!downtimeForm.downtime_minutes) {
      alert("Please enter Downtime Minutes");
      return;
    }

    try {
      await createProductionEntry({
        line: downtimeForm.line,
        shift: downtimeForm.shift,
        produced_units: 0,
        rejected_units: 0,
        downtime_minutes: Number(downtimeForm.downtime_minutes),
        downtime_reason: downtimeForm.downtime_reason,
        operator_name: downtimeForm.operator_name,
        remarks: downtimeForm.remarks,
      });

      alert("Downtime Entry Saved");

      setDowntimeForm({
        line: "SIGNA Main Line",
        shift: "A",
        downtime_minutes: "",
        downtime_reason: "Robot Fault",
        operator_name: "",
        remarks: "",
      });
    } catch (error) {
      console.error(error);
      alert("Save Failed");
    }
  };

  const saveTarget = async () => {
  if (!targetForm.target_units) {
    alert("Please enter Target Units");
    return;
  }

  try {
    await createDailyTarget({
      line: targetForm.line,
      shift: targetForm.shift,
      target_units: Number(targetForm.target_units),
      supervisor_name: targetForm.supervisor_name,
      remarks: targetForm.remarks,
    });

    alert("Daily Target Saved");

    setTargetForm({
      line: "SIGNA Main Line",
      shift: "A",
      target_units: "",
      supervisor_name: "",
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
        <h1>Operations Data Entry</h1>
        <p>Digital replacement for production and downtime logbook entries.</p>
      </div>

      <div className="form-tabs">
        <button
          className={activeForm === "production" ? "active" : ""}
          onClick={() => setActiveForm("production")}
        >
          Production Entry
        </button>

        <button
          className={activeForm === "downtime" ? "active" : ""}
          onClick={() => setActiveForm("downtime")}
        >
          Downtime Entry
        </button>

        <button
          className={activeForm === "target" ? "active" : ""}
          onClick={() => setActiveForm("target")}
        >
          Daily Target
        </button>
      </div>

      <div className="form-panel">
        {activeForm === "production" && (
          <>
            <h2>Production Entry</h2>

            <div className="form-grid">
              <div>
                <label>Line</label>
                <select
                  value={productionForm.line}
                  onChange={(e) =>
                    setProductionForm({ ...productionForm, line: e.target.value })
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
                  value={productionForm.shift}
                  onChange={(e) =>
                    setProductionForm({ ...productionForm, shift: e.target.value })
                  }
                >
                  <option>A</option>
                  <option>B</option>
                  <option>C</option>
                  <option>G</option>
                </select>
              </div>

              <div>
                <label>Produced Units</label>
                <input
                  type="number"
                  value={productionForm.produced_units}
                  onChange={(e) =>
                    setProductionForm({
                      ...productionForm,
                      produced_units: e.target.value,
                    })
                  }
                />
              </div>

              <div>
                <label>Rejected Units</label>
                <input
                  type="number"
                  value={productionForm.rejected_units}
                  onChange={(e) =>
                    setProductionForm({
                      ...productionForm,
                      rejected_units: e.target.value,
                    })
                  }
                />
              </div>

              <div>
                <label>Operator Name</label>
                <input
                  type="text"
                  value={productionForm.operator_name}
                  onChange={(e) =>
                    setProductionForm({
                      ...productionForm,
                      operator_name: e.target.value,
                    })
                  }
                />
              </div>

              <div>
                <label>Remarks</label>
                <input
                  type="text"
                  value={productionForm.remarks}
                  onChange={(e) =>
                    setProductionForm({
                      ...productionForm,
                      remarks: e.target.value,
                    })
                  }
                />
              </div>
            </div>

            <button className="save-btn" onClick={saveProduction}>
              Save Production Entry
            </button>
          </>
        )}

        {activeForm === "downtime" && (
          <>
            <h2>Downtime Entry</h2>

            <div className="form-grid">
              <div>
                <label>Line</label>
                <select
                  value={downtimeForm.line}
                  onChange={(e) =>
                    setDowntimeForm({ ...downtimeForm, line: e.target.value })
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
                  value={downtimeForm.shift}
                  onChange={(e) =>
                    setDowntimeForm({ ...downtimeForm, shift: e.target.value })
                  }
                >
                  <option>A</option>
                  <option>B</option>
                  <option>C</option>
                  <option>G</option>
                </select>
              </div>

              <div>
                <label>Downtime Minutes</label>
                <input
                  type="number"
                  value={downtimeForm.downtime_minutes}
                  onChange={(e) =>
                    setDowntimeForm({
                      ...downtimeForm,
                      downtime_minutes: e.target.value,
                    })
                  }
                />
              </div>

              <div>
                <label>Downtime Reason</label>
                <select
                  value={downtimeForm.downtime_reason}
                  onChange={(e) =>
                    setDowntimeForm({
                      ...downtimeForm,
                      downtime_reason: e.target.value,
                    })
                  }
                >
                  <option>Robot Fault</option>
                  <option>Material Delay</option>
                  <option>Power Failure</option>
                  <option>Tool Change</option>
                  <option>Maintenance</option>
                  <option>Quality Hold</option>
                  <option>Manpower Issue</option>
                  <option>Others</option>
                </select>
              </div>

              <div>
                <label>Operator Name</label>
                <input
                  type="text"
                  value={downtimeForm.operator_name}
                  onChange={(e) =>
                    setDowntimeForm({
                      ...downtimeForm,
                      operator_name: e.target.value,
                    })
                  }
                />
              </div>

              <div>
                <label>Remarks</label>
                <input
                  type="text"
                  value={downtimeForm.remarks}
                  onChange={(e) =>
                    setDowntimeForm({
                      ...downtimeForm,
                      remarks: e.target.value,
                    })
                  }
                />
              </div>
            </div>

            <button className="save-btn" onClick={saveDowntime}>
              Save Downtime Entry
            </button>
          </>
        )}

        {activeForm === "target" && (
          <>
            <h2>Daily Target Entry</h2>

            <div className="form-grid">
              <div>
                <label>Line</label>
                <select
                  value={targetForm.line}
                  onChange={(e) =>
                    setTargetForm({ ...targetForm, line: e.target.value })
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
                  value={targetForm.shift}
                  onChange={(e) =>
                    setTargetForm({ ...targetForm, shift: e.target.value })
                  }
                >
                  <option>A</option>
                  <option>B</option>
                  <option>C</option>
                  <option>G</option>
                </select>
              </div>

              <div>
                <label>Target Units</label>
                <input
                  type="number"
                  value={targetForm.target_units}
                  onChange={(e) =>
                    setTargetForm({
                      ...targetForm,
                      target_units: e.target.value,
                    })
                  }
                />
              </div>

              <div>
                <label>Supervisor Name</label>
                <input
                  type="text"
                  value={targetForm.supervisor_name}
                  onChange={(e) =>
                    setTargetForm({
                      ...targetForm,
                      supervisor_name: e.target.value,
                    })
                  }
                />
              </div>

              <div>
                <label>Remarks</label>
                <input
                  type="text"
                  value={targetForm.remarks}
                  onChange={(e) =>
                    setTargetForm({
                      ...targetForm,
                      remarks: e.target.value,
                    })
                  }
                />
              </div>
            </div>

            <button className="save-btn" onClick={saveTarget}>
              Save Daily Target
            </button>
          </>
        )}
      </div>
    </div>
  );
}