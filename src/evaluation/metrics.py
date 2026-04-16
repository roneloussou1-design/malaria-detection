import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    f1_score
)
import os

def evaluate_model(y_true, y_pred, y_proba, model_name: str):
    print(f"\n=== Évaluation : {model_name} ===")
    print(classification_report(
        y_true, y_pred,
        target_names=["Uninfected", "Parasitized"]
    ))
    auc = roc_auc_score(y_true, y_proba)
    print(f"AUC-ROC : {auc:.4f}")
    return auc

def plot_confusion_matrix(y_true, y_pred, save_path: str):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Uninfected", "Parasitized"])
    ax.set_yticklabels(["Uninfected", "Parasitized"])
    ax.set_xlabel("Prédit")
    ax.set_ylabel("Réel")
    ax.set_title("Matrice de confusion")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]),
                    ha="center", va="center", fontsize=14)
    plt.colorbar(im)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"Matrice sauvegardée : {save_path}")

def plot_roc_curve(y_true, y_proba, save_path: str):
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    auc         = roc_auc_score(y_true, y_proba)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}")
    plt.plot([0, 1], [0, 1], "k--")
    plt.xlabel("Taux de faux positifs")
    plt.ylabel("Taux de vrais positifs")
    plt.title("Courbe ROC")
    plt.legend()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"Courbe ROC sauvegardée : {save_path}")