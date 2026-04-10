"""
MNIST training with SLURM array jobs for hyperparameter sweeps.

This script is the same training as 04_python_training.py, but designed to run
multiple times in parallel with different hyperparameters. Each SLURM array task
gets a different combination of learning rate and batch size via --task-id.

The --task-id comes from $SLURM_ARRAY_TASK_ID in the sbatch script.
With --array=0-3, SLURM launches 4 jobs with task IDs 0, 1, 2, 3.
"""

import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# --- Parse task ID from SLURM ---
# Each array job gets a unique task ID, which we use to select hyperparameters.
parser = argparse.ArgumentParser()
parser.add_argument("--task-id", type=int, required=True,
                    help="SLURM array task ID, used to select a hyperparameter config")
args = parser.parse_args()

# --- Define hyperparameter grid ---
# Each entry is one experiment. SLURM array task ID selects which one to run.
# This way, 4 jobs run in parallel, each testing a different combination.
CONFIGS = [
    {"lr": 0.001, "batch_size": 32},
    {"lr": 0.01,  "batch_size": 32},
    {"lr": 0.001, "batch_size": 128},
    {"lr": 0.01,  "batch_size": 128},
]

config = CONFIGS[args.task_id]
EPOCHS = 3

print(f"Task {args.task_id}: lr={config['lr']}, batch_size={config['batch_size']}")

# --- Device setup ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


# --- Model (same as 04_python_training.py) ---
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 32 * 7 * 7)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# --- Data loading ---
train_dataset = datasets.MNIST("./data", train=True, download=True, transform=transforms.ToTensor())
test_dataset = datasets.MNIST("./data", train=False, transform=transforms.ToTensor())

# Compute mean and std from the training data for normalization
all_images = torch.stack([img for img, _ in train_dataset])
mean = all_images.mean()
std = all_images.std()
print(f"MNIST mean: {mean:.4f}, std: {std:.4f}")

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((mean,), (std,))
])
train_dataset.transform = transform
test_dataset.transform = transform

# num_workers=2 loads data in parallel using 2 CPU cores (see --cpus-per-task in sbatch)
# batch_size comes from the hyperparameter config selected by the task ID
train_loader = DataLoader(train_dataset, batch_size=config["batch_size"], shuffle=True, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=config["batch_size"], shuffle=False, num_workers=2)

# --- Training ---
model = SimpleCNN().to(device)
optimizer = optim.SGD(model.parameters(), lr=config["lr"])
criterion = nn.CrossEntropyLoss()

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

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

    print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {running_loss/len(train_loader):.4f}, Acc: {100.*correct/total:.2f}%")

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

print(f"\nTask {args.task_id} | lr={config['lr']}, bs={config['batch_size']} | Test Acc: {100.*correct/total:.2f}%")
