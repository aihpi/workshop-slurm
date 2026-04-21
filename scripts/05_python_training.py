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
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)   # 1 input channel (grayscale), 16 output filters, kernel size of 3 with padding=1 ensures spatial size stays the same
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)   # 16 input channels, 32 output filters
        self.pool = nn.MaxPool2d(2, 2)                  # Halves spatial dimensions (28->14). Slides a 2×2 window with stride 2 and keeps only the maximum value in each window.
        self.fc1 = nn.Linear(32 * 7 * 7, 128)          # Flatten and project to 128 features
        self.fc2 = nn.Linear(128, 10)                   # Final layer: 10 classes (digits 0-9)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))   # -> 16 x 14 x 14
        x = self.pool(self.relu(self.conv2(x)))   # -> 32 x 7 x 7
        x = x.view(-1, 32 * 7 * 7)               # Flatten to 1D, The -1 means "figure out this dimension automatically" — it becomes the batch size here.
        x = self.relu(self.fc1(x))                # -> 128
        x = self.fc2(x)                           # -> 10
        return x


# --- Shared project storage ---
# Data was downloaded by 04_data_setup.sh to shared storage (see that script for details).
DATA_DIR = "/sc/projects/sci-aisc/workshop-slurm/data"

# --- Data loading ---
# MNIST is the "hello world" of image classification: 70,000 grayscale images
# of handwritten digits 0-9, each 28x28 pixels. It ships with torchvision.
#   - train=True    -> 60,000 training samples
#   - train=False   -> 10,000 held-out test samples
#   - download=False -> 04_data_setup.sh already downloaded the data to shared
#                       project storage (one copy for all workshop participants).
#   - transform=ToTensor() converts PIL Images (H x W x C, uint8 0-255) into
#     PyTorch tensors (C x H x W, float in [0, 1]). This is a TEMPORARY transform
#     — we replace it below once we have computed the normalization statistics.
train_dataset = datasets.MNIST(DATA_DIR, train=True, download=False, transform=transforms.ToTensor())
test_dataset = datasets.MNIST(DATA_DIR, train=False, transform=transforms.ToTensor())

# --- Compute normalization statistics from the training set ---
# Neural networks train much better when inputs have mean ~0 and std ~1:
# gradients stay in a sensible range, and standard weight-init schemes assume it.
# We compute these statistics ONCE, from the TRAINING data only — never from the
# test set, to avoid leaking information across the train/test split.
#
# torch.stack turns a list of 60,000 tensors of shape [1, 28, 28] into a single
# tensor of shape [60000, 1, 28, 28]. This materializes ~188 MB in RAM — fine for
# MNIST, but for larger datasets (ImageNet, etc.) you would stream the statistics
# batch-by-batch or just use published constants instead.
all_images = torch.stack([img for img, _ in train_dataset])  # `_` discards the label
mean = all_images.mean()   # scalar, ~0.1307 for MNIST
std = all_images.std()     # scalar, ~0.3081 for MNIST
print(f"MNIST mean: {mean:.4f}, std: {std:.4f}")

# --- Build the final transform pipeline ---
# transforms.Compose chains transforms in order, like f(g(x)):
#   1. ToTensor   -> PIL Image to float tensor in [0, 1]
#   2. Normalize  -> (pixel - mean) / std, applied per channel
# The trailing comma in (mean,) makes a single-element tuple: Normalize expects
# one value PER CHANNEL (MNIST is 1-channel grayscale; for RGB you would pass
# three-element tuples like (r_mean, g_mean, b_mean)).
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((mean,), (std,))
])

# Overwrite the initial ToTensor-only transform with the full pipeline.
# Both train AND test datasets use the same transform with the SAME (training)
# statistics — recomputing stats on the test set would cause a silent train/test
# distribution mismatch and quietly hurt reported accuracy.
train_dataset.transform = transform
test_dataset.transform = transform

# num_workers=2 loads data in parallel using 2 CPU cores (see --cpus-per-task in sbatch)
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

# --- Training setup ---
# Instantiate the model and move its weights to the GPU. Everything the model
# touches (inputs, outputs) must live on the SAME device, or PyTorch errors.
model = SimpleCNN().to(device)

# SGD (Stochastic Gradient Descent) is the simplest optimizer
optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE)

# CrossEntropyLoss is the standard loss for multi-class classification. 
# It internally applies softmax to the model's logits and computes the negative
# log-likelihood of the correct class — which is why SimpleCNN.forward returns
# raw logits (NO softmax) from fc2: applying softmax twice would be a bug.
criterion = nn.CrossEntropyLoss()

# --- Training loop ---
# Two nested loops:
#   OUTER (epoch): one full pass over all 60,000 training images.
#   INNER (batch): 64 images at a time — ~938 batches per epoch.
# We train in batches because (a) the full dataset wouldn't fit on the GPU for
# larger models, and (b) noisy per-batch gradients help the optimizer explore.
for epoch in range(EPOCHS):
    # Switch layers like Dropout / BatchNorm into TRAINING behavior. SimpleCNN
    # has neither, so this is a no-op here — but it's best practice to always
    # pair model.train() with model.eval() before evaluation. 
    model.train()

    # Per-epoch metric accumulators, reset at the start of every epoch.
    running_loss = 0.0
    correct = 0
    total = 0

    # train_loader yields (images, labels) tuples:
    #   data   -> shape [64, 1, 28, 28]  (a batch of 64 MNIST images)
    #   target -> shape [64]             (the correct digit 0-9 for each image)
    for batch_idx, (data, target) in enumerate(train_loader):
        # Copy the batch to GPU memory. The model is already on the GPU; inputs
        # and outputs must share its device or PyTorch raises a runtime error.
        data, target = data.to(device), target.to(device)

        # ================================================================
        # The five-step training recipe — the heart of EVERY PyTorch script
        # ================================================================

        # 1. RESET gradients. PyTorch accumulates .grad by default, so without
        #    this line the previous batch's gradients would silently add to
        #    this batch's — training would go off the rails within a few steps.
        optimizer.zero_grad()

        # 2. FORWARD pass. Runs SimpleCNN.forward(data), producing logits of
        #    shape [64, 10]. Along the way, autograd records every operation
        #    into a computation graph so step 4 can walk it backwards.
        output = model(data)

        # 3. LOSS. Compare predictions to the ground truth; returns a single
        #    scalar measuring how wrong the model was on this batch.
        loss = criterion(output, target)

        # 4. BACKWARD pass. Autograd walks the recorded graph and computes derivative
        #    d(loss) / d(w) for EVERY trainable weight, storing it on the
        #    parameter's .grad attribute. 
        loss.backward()

        # 5. UPDATE. The optimizer reads each parameter's .grad and applies
        #    its update rule (for SGD: w <- w - lr * grad).
        optimizer.step()

        # --- Per-batch bookkeeping (no effect on training) ---
        # .item() extracts the Python float AND detaches from the graph, so we
        # don't leak GPU memory by hoarding computation graphs across batches.
        running_loss += loss.item()
        # Turn the 10 scores per image into a single predicted digit:
        # output.max(1) finds the highest score in each row, and its index
        # (0-9) IS the predicted class. We discard the score with `_`.
        _, predicted = output.max(1)
        # Count how many images we've seen (the last batch may be smaller
        # than 64, so we read the actual batch size from the tensor).
        total += target.size(0)
        # Count how many predictions matched the true label in this batch,
        # and add it to the running total for the epoch.
        correct += predicted.eq(target).sum().item()

    # End-of-epoch summary. len(train_loader) is the number of batches (~938).
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