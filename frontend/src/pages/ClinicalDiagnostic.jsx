import { useState } from "react";
import { predictClinical } from "../api/malaria";

const REGIONS = [
  "Atacora","Atlantique","Borgou","Collines",
  "Couffo","Donga","Littoral","Mono","Oueme",
  "Plateau","Zou"
];

export default function ClinicalDiagnostic() {
  const [form, setForm] = useState({
    age: "", temperature: "", headache: 0,
    chills: 0, vomiting: 0, sweating: 0,
    fatigue: 0, joint_pain: 0,
    duration_days: "", region: "Littoral"
  });
  const [result,  setResult]  = useState(null);
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState(null);

  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setForm(f => ({
      ...f,
      [name]: type === "checkbox" ? (checked ? 1 : 0) : value
    }));
  }

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    try {
      const payload = {
        ...form,
        age:           parseInt(form.age),
        temperature:   parseFloat(form.temperature),
        duration_days: parseInt(form.duration_days)
      };
      const data = await predictClinical(payload);
      setResult(data);
    } catch {
      setError("Erreur lors de l'analyse. Vérifiez les données.");
    }
    setLoading(false);
  }

  const riskColor = {
    "Élevé": "#e74c3c",
    "Moyen": "#f39c12",
    "Faible": "#1D9E75"
  };

  const symptomes = [
    { name: "headache",   label: "Maux de tête" },
    { name: "chills",     label: "Frissons" },
    { name: "vomiting",   label: "Vomissements" },
    { name: "sweating",   label: "Sueurs" },
    { name: "fatigue",    label: "Fatigue" },
    { name: "joint_pain", label: "Douleurs articulaires" }
  ];

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", padding: "0 24px" }}>
      <h1 style={{ fontSize: "22px", marginBottom: "24px" }}>
        Diagnostic clinique
      </h1>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
        <div>
          <label style={{ fontSize: "14px", color: "#666" }}>Âge</label>
          <input name="age" type="number" value={form.age}
            onChange={handleChange} placeholder="ex: 25"
            style={{ width: "100%", padding: "10px", marginTop: "4px",
              border: "1px solid #ddd", borderRadius: "8px" }}
          />
        </div>
        <div>
          <label style={{ fontSize: "14px", color: "#666" }}>
            Température (°C)
          </label>
          <input name="temperature" type="number" step="0.1"
            value={form.temperature} onChange={handleChange}
            placeholder="ex: 38.5"
            style={{ width: "100%", padding: "10px", marginTop: "4px",
              border: "1px solid #ddd", borderRadius: "8px" }}
          />
        </div>
        <div>
          <label style={{ fontSize: "14px", color: "#666" }}>
            Durée des symptômes (jours)
          </label>
          <input name="duration_days" type="number"
            value={form.duration_days} onChange={handleChange}
            placeholder="ex: 3"
            style={{ width: "100%", padding: "10px", marginTop: "4px",
              border: "1px solid #ddd", borderRadius: "8px" }}
          />
        </div>
        <div>
          <label style={{ fontSize: "14px", color: "#666" }}>Région</label>
          <select name="region" value={form.region}
            onChange={handleChange}
            style={{ width: "100%", padding: "10px", marginTop: "4px",
              border: "1px solid #ddd", borderRadius: "8px" }}
          >
            {REGIONS.map(r => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>
      </div>

      <div style={{ marginTop: "20px" }}>
        <p style={{ fontSize: "14px", color: "#666", marginBottom: "12px" }}>
          Symptômes présents
        </p>
        <div style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "10px"
        }}>
          {symptomes.map(s => (
            <label key={s.name} style={{
              display: "flex", alignItems: "center",
              gap: "8px", fontSize: "14px"
            }}>
              <input type="checkbox" name={s.name}
                checked={form[s.name] === 1}
                onChange={handleChange}
              />
              {s.label}
            </label>
          ))}
        </div>
      </div>

      <button onClick={handleSubmit} disabled={loading}
        style={{
          width: "100%", padding: "14px", marginTop: "24px",
          background: "#1D9E75", color: "white",
          border: "none", borderRadius: "8px",
          fontSize: "16px", cursor: "pointer"
        }}
      >
        {loading ? "Analyse en cours..." : "Analyser les symptômes"}
      </button>

      {error && (
        <p style={{ color: "#e74c3c", marginTop: "12px" }}>{error}</p>
      )}

      {result && (
        <div style={{
          marginTop: "24px", padding: "24px",
          border: `2px solid ${riskColor[result.risk_level]}`,
          borderRadius: "12px"
        }}>
          <h2 style={{
            color: riskColor[result.risk_level],
            fontSize: "20px"
          }}>
            Risque {result.risk_level}
          </h2>
          <p style={{ marginTop: "8px" }}>
            Probabilité de paludisme :{" "}
            <strong>
              {(result.malaria_probability * 100).toFixed(1)}%
            </strong>
          </p>
          <p style={{
            marginTop: "12px", padding: "12px",
            background: "#f5f5f5", borderRadius: "8px",
            fontSize: "14px"
          }}>
            {result.recommendation}
          </p>
        </div>
      )}
    </div>
  );
}