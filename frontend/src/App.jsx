import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import ImageDiagnostic from "./pages/ImageDiagnostic";
import ClinicalDiagnostic from "./pages/ClinicalDiagnostic";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/"         element={<Home />} />
        <Route path="/image"    element={<ImageDiagnostic />} />
        <Route path="/clinical" element={<ClinicalDiagnostic />} />
      </Routes>
    </BrowserRouter>
  );
}