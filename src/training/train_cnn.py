import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.cnn_model import get_model
from src.data.data_pipeline import get_dataloaders

DEVICE   = "cuda" if torch.cuda.is_available() else "cpu"
EPOCHS   = 30
LR       = 3e-4
DATA_DIR = "data/raw/cell_images/cell_images"

def train():
    print(f"Entraînement sur : {DEVICE}")
    loaders   = get_dataloaders(DATA_DIR, batch_size=32)
    model     = get_model(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=EPOCHS)

    best_val_acc = 0

    for epoch in range(EPOCHS):
        # Entraînement
        model.train()
        train_loss = 0
        for images, labels in loaders["train"]:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(images)
            loss    = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        # Validation
        model.eval()
        correct = total = 0
        with torch.no_grad():
            for images, labels in loaders["val"]:
                images, labels = images.to(DEVICE), labels.to(DEVICE)
                preds   = model(images).argmax(1)
                correct += (preds == labels).sum().item()
                total   += labels.size(0)

        val_acc = correct / total
        scheduler.step()

        print(f"Epoch {epoch+1}/{EPOCHS} | "
              f"Loss: {train_loss:.3f} | "
              f"Val acc: {val_acc:.4f}")

        # Sauvegarder le meilleur modèle
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            os.makedirs("models/saved", exist_ok=True)
            torch.save(model.state_dict(), "models/saved/cnn_best.pt")
            print(f"  -> Meilleur modèle sauvegardé ({val_acc:.4f})")

    print(f"\nEntraînement terminé. Meilleure précision : {best_val_acc:.4f}")

if __name__ == "__main__":
    train()