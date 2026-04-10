import torch
import torchvision

print("All imports successful!")
print(f"PyTorch version:     {torch.__version__}")
print(f"Torchvision version: {torchvision.__version__}")
print(f"CUDA available:      {torch.cuda.is_available()}")
