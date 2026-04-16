import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  return (
    <div style={{
      maxWidth: "800px",
      margin: "60px auto",
      padding: "0 24px",
      textAlign: "center"
    }}>
      <h1 style={{ fontSize: "28px", marginBottom: "12px" }}>
        Système de détection du paludisme
      </h1>
      <p style={{ color: "#666", marginBottom: "40px" }}>
        Outil d'aide au diagnostic pour les agents de santé du Bénin
      </p>

      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "20px"
      }}>
        <div style={{
          border: "1px solid #e0e0e0",
          borderRadius: "12px",
          padding: "32px",
          cursor: "pointer",
          transition: "all .2s"
        }}
          onClick={() => navigate("/image")}
        >
          <div style={{ fontSize: "48px", marginBottom: "16px" }}>🔬</div>
          <h2 style={{ fontSize: "18px", marginBottom: "8px" }}>
            Diagnostic par image
          </h2>
          <p style={{ color: "#666", fontSize: "14px" }}>
            Uploader une image microscopique de frottis sanguin
            pour détecter la présence du parasite.
          </p>
        </div>

        <div style={{
          border: "1px solid #e0e0e0",
          borderRadius: "12px",
          padding: "32px",
          cursor: "pointer",
          transition: "all .2s"
        }}
          onClick={() => navigate("/clinical")}
        >
          <div style={{ fontSize: "48px", marginBottom: "16px" }}>📋</div>
          <h2 style={{ fontSize: "18px", marginBottom: "8px" }}>
            Diagnostic clinique
          </h2>
          <p style={{ color: "#666", fontSize: "14px" }}>
            Remplir les symptômes du patient pour obtenir
            une probabilité de paludisme.
          </p>
        </div>
      </div>
    </div>
  );
}