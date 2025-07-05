# train_potato_model.py

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

# --- 1. Configuration & Hyperparameters ---
# Use a GPU if available, otherwise use the CPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {DEVICE} device")

# Set the path to your pre-filtered potato dataset
DATASET_PATH = "./potato_dataset" 

# Model hyperparameters
LEARNING_RATE = 0.001
BATCH_SIZE = 32
NUM_EPOCHS = 10 # Increase for better performance, 10 is good for a start
VALIDATION_SPLIT = 0.2 # 20% of data will be used for validation

# Output files
MODEL_SAVE_PATH = "potato_disease_resnet18.pth"
CLASS_NAMES_PATH = "potato_class_names.json"

# --- 2. Data Preparation ---
# Define transformations for the training and validation sets
# For training, we apply augmentation to make the model more robust
train_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# For validation, we only resize and normalize
val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load the dataset using ImageFolder
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Dataset directory not found at {DATASET_PATH}. Please follow Step 1.")
    
full_dataset = datasets.ImageFolder(root=DATASET_PATH)

# Save the class names for later use in the app
class_names = full_dataset.classes
with open(CLASS_NAMES_PATH, 'w') as f:
    json.dump(class_names, f)
print(f"Found {len(class_names)} classes: {class_names}")
print(f"Saved class names to {CLASS_NAMES_PATH}")

# Split the dataset into training and validation sets
val_size = int(len(full_dataset) * VALIDATION_SPLIT)
train_size = len(full_dataset) - val_size
train_subset, val_subset = random_split(full_dataset, [train_size, val_size])

# Apply the respective transformations
train_subset.dataset.transform = train_transforms
val_subset.dataset.transform = val_transforms

# Create DataLoaders
train_loader = DataLoader(train_subset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_subset, batch_size=BATCH_SIZE, shuffle=False)

# --- 3. Model Definition ---
# Load a pretrained ResNet18 model
model = models.resnet18(pretrained=True)

# Freeze all the parameters in the pre-trained model
for param in model.parameters():
    param.requires_grad = False

# Replace the final fully connected layer to match our number of classes (3)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(class_names))

# Move the model to the selected device
model = model.to(DEVICE)

# --- 4. Training Setup ---
criterion = nn.CrossEntropyLoss()
# We only train the parameters of the final layer
optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE)

# --- 5. Training & Validation Loop ---
for epoch in range(NUM_EPOCHS):
    # Training phase
    model.train()
    running_loss = 0.0
    
    # Use tqdm for a progress bar
    train_progress = tqdm(train_loader, desc=f"Epoch {epoch+1}/{NUM_EPOCHS} [Training]")
    for inputs, labels in train_progress:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

        # Zero the parameter gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward pass and optimize
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        train_progress.set_postfix({'loss': running_loss / len(train_loader)})

    # Validation phase
    model.eval()
    val_loss = 0.0
    correct = 0
    total = 0
    
    val_progress = tqdm(val_loader, desc=f"Epoch {epoch+1}/{NUM_EPOCHS} [Validation]")
    with torch.no_grad(): # No need to calculate gradients for validation
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
    print(f"Epoch {epoch+1}/{NUM_EPOCHS} | "
          f"Train Loss: {running_loss/len(train_loader):.4f} | "
          f"Val Loss: {val_loss/len(val_loader):.4f} | "
          f"Val Acc: {val_accuracy:.2f}%")

print("\nFinished Training!")

# --- 6. Save the Model ---
torch.save(model.state_dict(), MODEL_SAVE_PATH)
print(f"Model state saved to {MODEL_SAVE_PATH}")