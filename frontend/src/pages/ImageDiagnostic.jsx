import { useState } from "react";
import { predictImage } from "../api/malaria";

export default function ImageDiagnostic() {
  const [file,    setFile]    = useState(null);
  const [preview, setPreview] = useState(null);
  const [result,  setResult]  = useState(null);
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState(null);

  function handleFile(e) {
    const f = e.target.files[0];
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
  }

  async function handleSubmit() {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const data = await predictImage(file);
      setResult(data);
    } catch {
      setError("Erreur lors de l'analyse. Réessayez.");
    }
    setLoading(false);
  }

  const riskColor = result?.label === "Parasitized" ? "#e74c3c" : "#1D9E75";

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", padding: "0 24px" }}>
      <h1 style={{ fontSize: "22px", marginBottom: "24px" }}>
        Diagnostic par image microscopique
      </h1>

      <div style={{
        border: "2px dashed #ccc",
        borderRadius: "12px",
        padding: "32px",
        textAlign: "center",
        marginBottom: "20px"
      }}>
        <input
          type="file"
          accept="image/jpeg,image/png"
          onChange={handleFile}
          style={{ marginBottom: "12px" }}
        />
        {preview && (
          <img src={preview} alt="preview"
            style={{
              width: "100%", maxHeight: "300px",
              objectFit: "contain", marginTop: "12px",
              borderRadius: "8px"
            }}
          />
        )}
      </div>

      <button
        onClick={handleSubmit}
        disabled={!file || loading}
        style={{
          width: "100%", padding: "14px",
          background: file ? "#1D9E75" : "#ccc",
          color: "white", border: "none",
          borderRadius: "8px", fontSize: "16px",
          cursor: file ? "pointer" : "not-allowed"
        }}
      >
        {loading ? "Analyse en cours..." : "Analyser l'image"}
      </button>

      {error && (
        <p style={{ color: "#e74c3c", marginTop: "12px" }}>{error}</p>
      )}

      {result && (
        <div style={{
          marginTop: "24px", padding: "24px",
          border: `2px solid ${riskColor}`,
          borderRadius: "12px"
        }}>
          <h2 style={{ color: riskColor, fontSize: "20px" }}>
            {result.label === "Parasitized"
              ? "Positif — Parasite détecté"
              : "Négatif — Aucun parasite"}
          </h2>
          <p style={{ marginTop: "8px" }}>
            Confiance : <strong>
              {(result.confidence * 100).toFixed(1)}%
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