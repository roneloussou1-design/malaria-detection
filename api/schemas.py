from pydantic import BaseModel, Field
from typing import Optional

class ClinicalInput(BaseModel):
    age:            int   = Field(..., ge=0, le=120)
    temperature:    float = Field(..., ge=35.0, le=42.0)
    headache:       int   = Field(..., ge=0, le=1)
    chills:         int   = Field(..., ge=0, le=1)
    vomiting:       int   = Field(..., ge=0, le=1)
    sweating:       int   = Field(..., ge=0, le=1)
    fatigue:        int   = Field(..., ge=0, le=1)
    joint_pain:     int   = Field(..., ge=0, le=1)
    duration_days:  int   = Field(..., ge=0, le=30)
    region:         str

class ImagePredictionResult(BaseModel):
    prediction_id:  str
    label:          str
    confidence:     float
    recommendation: str

class ClinicalPredictionResult(BaseModel):
    prediction_id:       str
    malaria_probability: float
    risk_level:          str
    recommendation:      str