import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split

def get_transforms(phase: str):
    if phase == "train":
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
                                 [0.229, 0.224, 0.225])
        ])
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

def get_dataloaders(data_dir: str, batch_size: int = 32):
    dataset = datasets.ImageFolder(
        data_dir,
        transform=get_transforms("train")
    )

    n       = len(dataset)
    train_n = int(0.7 * n)
    val_n   = int(0.15 * n)
    test_n  = n - train_n - val_n

    train_set, val_set, test_set = random_split(
        dataset, [train_n, val_n, test_n]
    )

    return {
        "train":   DataLoader(train_set, batch_size=batch_size,
                              shuffle=True,  num_workers=0),
        "val":     DataLoader(val_set,   batch_size=batch_size,
                              shuffle=False, num_workers=0),
        "test":    DataLoader(test_set,  batch_size=batch_size,
                              shuffle=False, num_workers=0),
        "classes": dataset.classes
    }