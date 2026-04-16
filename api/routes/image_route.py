from fastapi import APIRouter, UploadFile, File, HTTPException
import torch
from PIL import Image
from io import BytesIO
from src.models.cnn_model import get_model
from src.data.augmentation import get_val_augmentation
from database.models import save_prediction
import os

router  = APIRouter()
DEVICE  = "cuda" if torch.cuda.is_available() else "cpu"
_model  = None

def get_cnn():
    global _model
    if _model is None:
        _model = get_model(DEVICE)
        model_path = "models/saved/cnn_best.pt"
        if os.path.exists(model_path):
            _model.load_state_dict(
                torch.load(model_path, map_location=DEVICE)
            )
        _model.eval()
    return _model

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

    contents  = await file.read()
    img       = Image.open(BytesIO(contents)).convert("RGB")
    transform = get_val_augmentation()
    tensor    = transform(img).unsqueeze(0).to(DEVICE)

    model = get_cnn()
    with torch.no_grad():
        probs = torch.softmax(model(tensor), dim=1)[0]

    label      = "Parasitized" if probs[0] > probs[1] else "Uninfected"
    confidence = float(probs.max())

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