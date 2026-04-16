import torch
import joblib
import numpy as np
from PIL import Image
from src.models.cnn_model import get_model
from src.data.augmentation import get_val_augmentation

class MalariaEnsemble:
    def __init__(self):
        self.device   = "cuda" if torch.cuda.is_available() else "cpu"
        self.cnn      = get_model(self.device)
        self.cnn.load_state_dict(
            torch.load("models/saved/cnn_best.pt",
                       map_location=self.device)
        )
        self.cnn.eval()
        self.clinical = joblib.load("models/saved/clinical_pipeline.pkl")
        self.transform = get_val_augmentation()

    def predict_image(self, image_bytes: bytes) -> dict:
        from io import BytesIO
        img    = Image.open(BytesIO(image_bytes)).convert("RGB")
        tensor = self.transform(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            probs = torch.softmax(self.cnn(tensor), dim=1)[0]
        return {
            "label":      "Parasitized" if probs[0] > 0.5 else "Uninfected",
            "confidence": float(probs.max())
        }

    def predict_clinical(self, patient: dict) -> dict:
        proba = float(
            self.clinical.predict_proba(
                __import__('pandas').DataFrame([patient])
            )[0][1]
        )
        return {
            "malaria_probability": round(proba, 4),
            "risk_level": (
                "Élevé"  if proba >= 0.7 else
                "Moyen"  if proba >= 0.4 else
                "Faible"
            )
        }

    def predict_combined(self, image_bytes: bytes,
                         patient: dict) -> dict:
        img_result = self.predict_image(image_bytes)
        cli_result = self.predict_clinical(patient)

        img_proba = img_result["confidence"] if \
            img_result["label"] == "Parasitized" else \
            1 - img_result["confidence"]

        combined = round(
            0.6 * img_proba + 0.4 * cli_result["malaria_probability"], 4
        )
        return {
            "image_result":    img_result,
            "clinical_result": cli_result,
            "combined_probability": combined,
            "final_risk": (
                "Élevé"  if combined >= 0.7 else
                "Moyen"  if combined >= 0.4 else
                "Faible"
            )
        }