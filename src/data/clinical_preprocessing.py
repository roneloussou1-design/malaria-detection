import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

FEATURES = [
    "age", "temperature", "headache", "chills",
    "vomiting", "sweating", "fatigue", "joint_pain",
    "duration_days", "region_encoded"
]

def preprocess_clinical(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Convertir Oui/Non en 0/1
    bool_cols = ["headache", "chills", "vomiting",
                 "sweating", "fatigue", "joint_pain"]
    for col in bool_cols:
        df[col] = df[col].map({"Oui": 1, "Non": 0,
                               "Yes": 1, "No": 0}).fillna(0)

    # Encoder les régions en chiffres
    le = LabelEncoder()
    df["region_encoded"] = le.fit_transform(df["region"].fillna("Inconnu"))

    # Gérer les valeurs manquantes
    df["temperature"]  = df["temperature"].fillna(df["temperature"].median())
    df["age"]          = df["age"].fillna(df["age"].median())
    df["duration_days"]= df["duration_days"].fillna(0)

    return df[FEATURES + ["malaria_positive"]]


def preprocess_single_patient(patient: dict) -> pd.DataFrame:
    """
    Prépare les données d'un seul patient pour la prédiction.
    patient = dictionnaire avec les clés de FEATURES
    """
    le = LabelEncoder()
    le.classes_ = np.array(["Atacora", "Atlantique", "Borgou",
                             "Collines", "Couffo", "Donga",
                             "Littoral", "Mono", "Oueme",
                             "Plateau", "Zou", "Inconnu"])

    region = patient.get("region", "Inconnu")
    try:
        patient["region_encoded"] = int(le.transform([region])[0])
    except ValueError:
        patient["region_encoded"] = 11  # Inconnu

    return pd.DataFrame([patient])[FEATURES]