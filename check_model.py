import torch

checkpoint = torch.load("model/best_model.pt", map_location="cpu", weights_only=False)

print("Checkpoint type:")
print(type(checkpoint))

print("\nCheckpoint contents:")

if isinstance(checkpoint, dict):
    print(checkpoint.keys())
else:
    print(checkpoint)