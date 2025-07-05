# train_potato_model_final.py

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from tqdm import tqdm
import os
import json

# All definitions and configurations can stay at the global level.
# They don't *start* any processes, so they are safe to be imported.

# --- 1. Configuration & Hyperparameters ---
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DATASET_PATH = "./potato/color"
LEARNING_RATE = 0.001
BATCH_SIZE = 32
NUM_EPOCHS = 10
VALIDATION_SPLIT = 0.2
MODEL_SAVE_PATH = "potato_disease_resnet18.pth"
CLASS_NAMES_PATH = "potato_class_names.json"


def main():
    """
    Main function to run the data loading, training, and saving process.
    """
    print(f"Using {DEVICE} device")

    # --- 2. Data Preparation ---
    train_transforms = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset directory not found at '{DATASET_PATH}'.")
    
    full_dataset = datasets.ImageFolder(root=DATASET_PATH)
    
    class_names = full_dataset.classes
    with open(CLASS_NAMES_PATH, 'w') as f:
        json.dump(class_names, f)
    print(f"Successfully loaded {len(full_dataset)} images from '{DATASET_PATH}'.")
    print(f"Found {len(class_names)} classes: {class_names}")

    val_size = int(len(full_dataset) * VALIDATION_SPLIT)
    train_size = len(full_dataset) - val_size
    train_subset, val_subset = random_split(full_dataset, [train_size, val_size])

    train_subset.dataset.transform = train_transforms
    val_subset.dataset.transform = val_transforms
    
    # This is the line that causes the issue if not protected
    train_loader = DataLoader(train_subset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_subset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

    # --- 3. Model Definition ---
    # The warning you see is normal and can be ignored. It's just torchvision updating its API.
    model = models.resnet18(weights='IMAGENET1K_V1') # Using new recommended syntax
    
    for param in model.parameters():
        param.requires_grad = False
    
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(class_names))
    model = model.to(DEVICE)

    # --- 4. Training Setup ---
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE)

    # --- 5. Training & Validation Loop ---
    for epoch in range(NUM_EPOCHS):
        model.train()
        running_loss = 0.0
        train_progress = tqdm(train_loader, desc=f"Epoch {epoch+1}/{NUM_EPOCHS} [Training]")
        
        for inputs, labels in train_progress:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            train_progress.set_postfix({'loss': running_loss / len(train_loader)})

        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        val_progress = tqdm(val_loader, desc=f"Epoch {epoch+1}/{NUM_EPOCHS} [Validation]")
        
        with torch.no_grad():
            for inputs, labels in val_progress:
                inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                val_progress.set_postfix({'val_loss': val_loss / len(val_loader)})

        val_accuracy = 100 * correct / total
        print(f"Epoch {epoch+1}/{NUM_EPOCHS} | Train Loss: {running_loss/len(train_loader):.4f} | Val Loss: {val_loss/len(val_loader):.4f} | Val Acc: {val_accuracy:.2f}%")

    print("\nFinished Training!")

    # --- 6. Save the Model ---
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Model state saved to {MODEL_SAVE_PATH}")


# --- THIS IS THE CRUCIAL FIX ---
# This block ensures that the main() function is called only when
# you run the script directly, not when it's imported by another process.
if __name__ == '__main__':
    main()