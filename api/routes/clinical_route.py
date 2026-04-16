from fastapi import APIRouter, HTTPException
from api.schemas import ClinicalInput
from database.models import save_prediction
import joblib
import os

router    = APIRouter()
_pipeline = None

def get_pipeline():
    global _pipeline
    if _pipeline is None:
        path = "models/saved/clinical_pipeline.pkl"
        if not os.path.exists(path):
            raise HTTPException(
                503,
                "Modèle clinique pas encore entraîné."
            )
        _pipeline = joblib.load(path)
    return _pipeline

def get_recommendation(proba: float) -> str:
    if proba >= 0.7:
        return "Risque élevé. Consulter immédiatement un médecin."
    if proba >= 0.4:
        return "Risque moyen. Test de confirmation recommandé."
    return "Risque faible. Surveiller l'évolution des symptômes."

@router.post("/predict")
async def predict_clinical(data: ClinicalInput):
    from src.data.clinical_preprocessing import preprocess_single_patient
    import pandas as pd

    patient = preprocess_single_patient(data.model_dump())
    pipeline = get_pipeline()
    proba    = float(pipeline.predict_proba(patient)[0][1])

    risk_level = (
        "Élevé"  if proba >= 0.7 else
        "Moyen"  if proba >= 0.4 else
        "Faible"
    )

    pred_id = save_prediction(
        type="clinical",
        result=risk_level,
        confidence=proba,
        region=data.region
    )

    return {
        "prediction_id":       pred_id,
        "malaria_probability": round(proba, 4),
        "risk_level":          risk_level,
        "recommendation":      get_recommendation(proba)
    }