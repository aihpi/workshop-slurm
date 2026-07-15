"""
Download datasets to shared project storage.

This script downloads MNIST and CIFAR-100 to /sc/projects/sci-aisc/workshop-slurm/data/.

--- Idempotency: safe to run multiple times ---
`datasets.MNIST(..., download=True)` (and CIFAR-100) does NOT unconditionally
download. torchvision's Dataset class internally calls a `_check_exists()`
method BEFORE fetching anything:
  - MNIST checks for the extracted archives in <DATA_DIR>/MNIST/raw/
  - CIFAR-100 checks for the extracted archive in <DATA_DIR>/cifar-100-python/
If those files are present (and their sizes/MD5 match), `download()` becomes a
no-op — no bytes are fetched, no files are overwritten. So running this script
a second time on a populated data directory is safe and prints "already
present" for each dataset.

The two prints below (via `report()`) mirror the same existence check
torchvision performs, purely so the log shows the user what will happen.

--- Why shared storage? ---
  - Home folders (/sc/home/) have limited space (quota).
  - Shared storage (/sc/projects/sci-aisc/) has more room and is accessible to all team members.
  - Download once, use everywhere — no need for each user to download their own copy.
"""

from pathlib import Path

from torchvision import datasets

DATA_DIR = "/sc/projects/sci-aisc/workshop-slurm/data"


def report(name: str, marker_path: Path) -> None:
    """
    Print whether the dataset will be downloaded or is already there.

    We check the same folder torchvision's own `_check_exists()` looks at.
    This is purely for user-facing clarity: torchvision will do its own check
    right after and skip the download regardless of what we print here.
    """
    if marker_path.exists():
        print(f"{name} already present at {marker_path.parent} — torchvision will skip the download.")
    else:
        print(f"{name} not found on disk — torchvision will download it now.")


# --- MNIST ---
# Used by scripts 05 (training) and 06 (array jobs).
# Small dataset (~50MB): 60k training + 10k test images of handwritten digits (28x28, grayscale).
print("=== MNIST ===")
report("MNIST", Path(DATA_DIR) / "MNIST" / "raw")
train = datasets.MNIST(DATA_DIR, train=True, download=True)
test = datasets.MNIST(DATA_DIR, train=False, download=True)
print(f"  Training samples: {len(train)}")
print(f"  Test samples:     {len(test)}")
print("  MNIST ready.")

print("")

# --- CIFAR-100 ---
# Used by scripts 07 (single GPU) and 08 (multi GPU).
# Larger dataset (~170MB): 50k training + 10k test color images (32x32, RGB) across 100 classes.
print("=== CIFAR-100 ===")
report("CIFAR-100", Path(DATA_DIR) / "cifar-100-python")
train = datasets.CIFAR100(DATA_DIR, train=True, download=True)
test = datasets.CIFAR100(DATA_DIR, train=False, download=True)
print(f"  Training samples: {len(train)}")
print(f"  Test samples:     {len(test)}")
print("  CIFAR-100 ready.")

print("")
print(f"All datasets stored in: {DATA_DIR}")
