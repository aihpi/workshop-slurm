"""
Download datasets to shared project storage.

This script downloads MNIST and CIFAR-100 to /sc/projects/sci-aisc/workshop-slurm/data/.
Datasets are only downloaded on the first run — subsequent runs skip if the data already exists.

Why shared storage?
  - Home folders (/sc/home/) have limited space (quota).
  - Shared storage (/sc/projects/sci-aisc/) has more room and is accessible to all team members.
  - Download once, use everywhere — no need for each user to download their own copy.
"""

from torchvision import datasets

DATA_DIR = "/sc/projects/sci-aisc/workshop-slurm/data"

# --- Download MNIST ---
# Used by scripts 05 (training) and 06 (array jobs).
# Small dataset (~50MB): 60k training + 10k test images of handwritten digits (28x28, grayscale).
print("=== MNIST ===")
print("Downloading MNIST (if not already present)...")
train = datasets.MNIST(DATA_DIR, train=True, download=True)
test = datasets.MNIST(DATA_DIR, train=False, download=True)
print(f"  Training samples: {len(train)}")
print(f"  Test samples:     {len(test)}")
print("  MNIST ready.")

print("")

# --- Download CIFAR-100 ---
# Used by scripts 07 (single GPU) and 08 (multi GPU).
# Larger dataset (~170MB): 50k training + 10k test color images (32x32, RGB) across 100 classes.
print("=== CIFAR-100 ===")
print("Downloading CIFAR-100 (if not already present)...")
train = datasets.CIFAR100(DATA_DIR, train=True, download=True)
test = datasets.CIFAR100(DATA_DIR, train=False, download=True)
print(f"  Training samples: {len(train)}")
print(f"  Test samples:     {len(test)}")
print("  CIFAR-100 ready.")

print("")
print(f"All datasets stored in: {DATA_DIR}")
