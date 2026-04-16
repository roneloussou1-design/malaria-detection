import torch
import torch.nn as nn
from torchvision import models

class MalariaCNN(nn.Module):
    def __init__(self, num_classes: int = 2, dropout: float = 0.4):
        super().__init__()
        base = models.efficientnet_b0(weights="IMAGENET1K_V1")

        for param in list(base.parameters())[:-20]:
            param.requires_grad = False

        in_features = base.classifier[1].in_features
        base.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Dropout(dropout / 2),
            nn.Linear(256, num_classes)
        )
        self.model = base

    def forward(self, x):
        return self.model(x)

def get_model(device: str = "cpu"):
    model = MalariaCNN()
    return model.to(device)