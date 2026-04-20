"""
Simple MNIST training script to demonstrate GPU usage on the cluster.

This script trains a small CNN (Convolutional Neural Network) on the MNIST
handwritten digit dataset (0-9). It automatically uses the GPU if available,
otherwise falls back to CPU.

The MNIST dataset is stored in shared project storage (see 04_data_setup.sh).
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# --- Hyperparameters ---
# Feel free to experiment with these values!
BATCH_SIZE = 64          # Number of images per training step
LEARNING_RATE = 0.01     # How fast the model learns (too high = unstable, too low = slow)
EPOCHS = 3               # Number of full passes through the training data

# --- Device setup ---
# This checks if a GPU is available and uses it, otherwise falls back to CPU.
# On the cluster, this requires --gpus=1 in your sbatch script.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


# --- Simple CNN model ---
# A small convolutional neural network for classifying 28x28 grayscale images.
# Input: 1x28x28 image -> Output: 10 class probabilities (digits 0-9)
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)   # 1 input channel (grayscale), 16 output filters
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)   # 16 input channels, 32 output filters
        self.pool = nn.MaxPool2d(2, 2)                  # Halves spatial dimensions (28->14->7)
        self.fc1 = nn.Linear(32 * 7 * 7, 128)          # Flatten and project to 128 features
        self.fc2 = nn.Linear(128, 10)                   # Final layer: 10 classes (digits 0-9)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))   # -> 16 x 14 x 14
        x = self.pool(self.relu(self.conv2(x)))   # -> 32 x 7 x 7
        x = x.view(-1, 32 * 7 * 7)               # Flatten to 1D
        x = self.relu(self.fc1(x))                # -> 128
        x = self.fc2(x)                           # -> 10
        return x


# --- Shared project storage ---
# Data was downloaded by 04_data_setup.sh to shared storage (see that script for details).
DATA_DIR = "/sc/projects/sci-aisc/workshop-slurm/data"

# --- Data loading ---
train_dataset = datasets.MNIST(DATA_DIR, train=True, download=False, transform=transforms.ToTensor())
test_dataset = datasets.MNIST(DATA_DIR, train=False, transform=transforms.ToTensor())

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
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

# --- Training ---
model = SimpleCNN().to(device)                     # Move model to GPU
optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE)  # Stochastic Gradient Descent
criterion = nn.CrossEntropyLoss()                  # Loss function for classification

for epoch in range(EPOCHS):
    model.train()                                  # Set model to training mode
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)  # Move data to GPU

        optimizer.zero_grad()          # Reset gradients from previous step
        output = model(data)           # Forward pass: compute predictions
        loss = criterion(output, target)  # Compute loss
        loss.backward()                # Backward pass: compute gradients
        optimizer.step()               # Update model weights

        running_loss += loss.item()
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()

    train_acc = 100.0 * correct / total
    avg_loss = running_loss / len(train_loader)
    print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {avg_loss:.4f}, Accuracy: {train_acc:.2f}%")

# --- Evaluation ---
# Test the trained model on data it has never seen before
model.eval()                                       # Set model to evaluation mode
correct = 0
total = 0
with torch.no_grad():                              # Disable gradient computation (saves memory)
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()

test_acc = 100.0 * correct / total
print(f"\nTest Accuracy: {test_acc:.2f}%")
