from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
from io import BytesIO
import numpy as np
import onnxruntime as ort
from database.models import save_prediction
import os

router = APIRouter()
_session = None

def get_session():
    global _session
    if _session is None:
        path = "models/saved/cnn_best.onnx"
        if not os.path.exists(path):
            raise HTTPException(503, "Modèle non disponible.")
        _session = ort.InferenceSession(path)
    return _session

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    arr = np.array(img).astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406])
    std  = np.array([0.229, 0.224, 0.225])
    arr  = (arr - mean) / std
    arr  = arr.transpose(2, 0, 1)
    return arr[np.newaxis, :].astype(np.float32)

def get_recommendation(label: str, confidence: float) -> str:
    if label == "Parasitized" and confidence > 0.85:
        return "Résultat positif. Consulter immédiatement un médecin."
    if label == "Parasitized" and confidence > 0.6:
        return "Résultat incertain. Répéter le test ou consulter."
    return "Résultat négatif. Surveiller les symptômes."

@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Format non supporté. JPEG ou PNG.")

    contents = await file.read()
    tensor   = preprocess_image(contents)
    session  = get_session()

    outputs    = session.run(None, {"input": tensor})
    probs      = outputs[0][0]
    label      = "Parasitized" if probs[0] > probs[1] else "Uninfected"
    confidence = float(max(probs))

    pred_id = save_prediction(
        type="image",
        result=label,
        confidence=confidence
    )

    return {
        "prediction_id":  pred_id,
        "label":          label,
        "confidence":     round(confidence, 4),
        "recommendation": get_recommendation(label, confidence)
    }