import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={{
      background: "#1D9E75",
      padding: "12px 24px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between"
    }}>
      <span style={{
        color: "white",
        fontWeight: "bold",
        fontSize: "18px"
      }}>
        Malaria Detection — Bénin
      </span>
      <div style={{ display: "flex", gap: "24px" }}>
        <Link to="/"
          style={{ color: "white", textDecoration: "none" }}>
          Accueil
        </Link>
        <Link to="/image"
          style={{ color: "white", textDecoration: "none" }}>
          Diagnostic image
        </Link>
        <Link to="/clinical"
          style={{ color: "white", textDecoration: "none" }}>
          Diagnostic clinique
        </Link>
      </div>
    </nav>
  );
}