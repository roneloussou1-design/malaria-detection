import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export async function predictImage(imageFile) {
  const formData = new FormData();
  formData.append("file", imageFile);
  const response = await API.post("/api/v1/image/predict", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function predictClinical(patientData) {
  const response = await API.post(
    "/api/v1/clinical/predict",
    patientData
  );
  return response.data;
}