import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from xgboost import XGBClassifier
import os

FEATURES = [
    "age", "temperature", "headache", "chills",
    "vomiting", "sweating", "fatigue", "joint_pain",
    "duration_days", "region_encoded"
]

def build_pipeline():
    xgb = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        eval_metric="logloss",
        random_state=42
    )
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        n_jobs=-1
    )
    ensemble = VotingClassifier(
        estimators=[("xgb", xgb), ("rf", rf)],
        voting="soft"
    )
    return Pipeline([
        ("scaler", StandardScaler()),
        ("model",  ensemble)
    ])

def train_clinical(csv_path: str):
    df = pd.read_csv(csv_path)
    X  = df[FEATURES]
    y  = df["malaria_positive"]

    pipeline = build_pipeline()

    cv     = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring="roc_auc")
    print(f"AUC-ROC moyen : {scores.mean():.4f} "
          f"(+/- {scores.std():.4f})")

    pipeline.fit(X, y)
    os.makedirs("models/saved", exist_ok=True)
    joblib.dump(pipeline, "models/saved/clinical_pipeline.pkl")
    print("Modèle clinique sauvegardé.")
    return pipeline

def predict_proba(pipeline, patient_data: dict) -> float:
    df = pd.DataFrame([patient_data])[FEATURES]
    return float(pipeline.predict_proba(df)[0][1])