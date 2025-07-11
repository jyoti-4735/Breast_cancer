import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from torchvision import transforms, datasets
from torch.utils.data import DataLoader

def get_data_loaders(data_dir, batch_size=32):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    train_dataset = datasets.ImageFolder(os.path.join(data_dir, 'train'), transform=transform)
    test_dataset  = datasets.ImageFolder(os.path.join(data_dir, 'test'), transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader  = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader


def train_multiclass_classifier(data_root, num_epochs=10, batch_size=32, lr=1e-4, save_path="multiclass_classifier.pth"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_loader, test_loader = get_data_loaders(data_root, batch_size)

    model = models.resnet18(pretrained=True)
    num_feats = model.fc.in_features
    model.fc = nn.Linear(num_feats, 6)  # 6 classes: 0-5
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(1, num_epochs + 1):
        model.train()
        running_loss, correct, total = 0.0, 0, 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        epoch_loss = running_loss / total
        epoch_acc  = correct / total
        print(f"[Train] Epoch {epoch}/{num_epochs}  Loss: {epoch_loss:.4f}  Acc: {epoch_acc:.4f}")

        model.eval()
        val_loss, val_correct, val_total = 0.0, 0, 0
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * images.size(0)
                preds = outputs.argmax(dim=1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)

        val_epoch_loss = val_loss / val_total
        val_epoch_acc  = val_correct / val_total
        print(f"[ Val ] Epoch {epoch}/{num_epochs}  Loss: {val_epoch_loss:.4f}  Acc: {val_epoch_acc:.4f}")
        print("-" * 50)

    torch.save(model.state_dict(), save_path)
    print(f"\n✅ Saved multiclass classifier to '{save_path}'")


if __name__ == "__main__":
    DATA_ROOT = "data/combined"   # expects combined/train and combined/test folders with 6 folders inside train/test

    train_multiclass_classifier(
        data_root=DATA_ROOT,
        num_epochs=10,
        batch_size=32,
        lr=1e-4,
        save_path="multiclass_classifier.pth"
    )
