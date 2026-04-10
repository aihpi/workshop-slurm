"""
CIFAR-100 training with ResNet-18 using multiple GPUs via Hugging Face Accelerate.

Compare this with 06_single_gpu.py — the training logic is almost identical,
but Accelerate handles distributing the model and data across multiple GPUs.

Key differences from the single-GPU version:
  - We create an Accelerator object
  - We call accelerator.prepare() on model, optimizer, and data loaders
  - We use accelerator.print() so only one GPU prints output
  - Everything else stays the same!

Run with: sbatch scripts/06_multi_gpu.sh
"""

import time
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from accelerate import Accelerator

# --- Initialize Accelerate ---
# This automatically detects how many GPUs are available and sets up distribution.
accelerator = Accelerator()

# --- Hyperparameters ---
BATCH_SIZE = 128
LEARNING_RATE = 0.01
EPOCHS = 5

# --- Shared project storage ---
DATA_DIR = "/sc/projects/sci-aisc/workshop-slurm/data"

accelerator.print(f"Number of GPUs: {accelerator.num_processes}")
accelerator.print(f"Current GPU: {accelerator.device}")

# --- ResNet-18 for CIFAR-100 ---
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 100)

# --- Data loading ---
train_dataset = datasets.CIFAR100(DATA_DIR, train=True, download=accelerator.is_main_process,
                                  transform=transforms.ToTensor())
test_dataset = datasets.CIFAR100(DATA_DIR, train=False, transform=transforms.ToTensor())

# Compute mean and std per channel from the training data
all_images = torch.stack([img for img, _ in train_dataset])
mean = all_images.mean(dim=(0, 2, 3))
std = all_images.std(dim=(0, 2, 3))
accelerator.print(f"CIFAR-100 mean: {mean}, std: {std}")

transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])
train_dataset.transform = transform
test_dataset.transform = transform

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

# --- Prepare for distributed training ---
# accelerator.prepare() wraps model, optimizer, and data loaders so they work across GPUs.
# Each GPU gets a slice of each batch automatically.
optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE)
model, optimizer, train_loader, test_loader = accelerator.prepare(
    model, optimizer, train_loader, test_loader
)
criterion = nn.CrossEntropyLoss()

# --- Training ---
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    epoch_start = time.time()

    for data, target in train_loader:
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        accelerator.backward(loss)
        optimizer.step()

        running_loss += loss.item()
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()

    epoch_time = time.time() - epoch_start
    accelerator.print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {running_loss/len(train_loader):.4f}, "
                      f"Acc: {100.*correct/total:.2f}%, Time: {epoch_time:.1f}s")

# --- Evaluation ---
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for data, target in test_loader:
        output = model(data)
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()

accelerator.print(f"\nTest Accuracy: {100.*correct/total:.2f}%")
