import torch

if torch.cuda.is_available():
    print(f"CUDA is available!")
    print(f"Device count: {torch.cuda.device_count()}")
    print(f"Device name:  {torch.cuda.get_device_name(0)}")
    print(f"Memory:       {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
else:
    print("WARNING: CUDA is NOT available. Did you request a GPU with --gpus?")
