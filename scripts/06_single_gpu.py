"""
CIFAR-100 training with ResNet-18 on a single GPU to test training time.

This script uses a ResNet-18 model (~11M parameters) on CIFAR-100 (100 classes).
ResNet-18 is much larger than our SimpleCNN, so training takes longer per epoch —
this will help us see whether multi-GPU training provides a real speedup.

The dataset is stored in the shared project storage at /sc/projects/sci-aisc/workshop-slurm/data/
instead of the home folder. On the cluster, home folders have limited space —
large datasets and model checkpoints should always go to /sc/projects/sci-aisc/.
"""

import time
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# --- Hyperparameters ---
BATCH_SIZE = 128
LEARNING_RATE = 0.01
EPOCHS = 5

# --- Shared project storage ---
# Store data here instead of your home folder!
DATA_DIR = "/sc/projects/sci-aisc/workshop-slurm/data"

# --- Device setup ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


# --- ResNet-18 for CIFAR-100 ---
# torchvision provides pre-defined ResNet architectures.
# We modify the final layer to output 100 classes instead of the default 1000 (ImageNet).
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 100)


# --- Data loading ---
train_dataset = datasets.CIFAR100(DATA_DIR, train=True, download=True, transform=transforms.ToTensor())
test_dataset = datasets.CIFAR100(DATA_DIR, train=False, transform=transforms.ToTensor())

# Compute mean and std per channel from the training data
all_images = torch.stack([img for img, _ in train_dataset])
mean = all_images.mean(dim=(0, 2, 3))  # mean per RGB channel
std = all_images.std(dim=(0, 2, 3))    # std per RGB channel
print(f"CIFAR-100 mean: {mean}, std: {std}")

# Resize to 224x224 — the resolution ResNet was designed for.
# This makes training significantly slower (more computation per image),
# which helps demonstrate the benefit of multi-GPU training later.
transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])
train_dataset.transform = transform
test_dataset.transform = transform

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

# --- Training ---
model = model.to(device)
optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE)
criterion = nn.CrossEntropyLoss()

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    epoch_start = time.time()

    for data, target in train_loader:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()

    epoch_time = time.time() - epoch_start
    print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {running_loss/len(train_loader):.4f}, "
          f"Acc: {100.*correct/total:.2f}%, Time: {epoch_time:.1f}s")

# --- Evaluation ---
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()

print(f"\nTest Accuracy: {100.*correct/total:.2f}%")
