# model_loader.py

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import json
import io

# --- 1. Configuration ---
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH = "potato_disease_resnet18.pth"
CLASS_NAMES_PATH = "potato_class_names.json"

# --- 2. Define the Model Loading Logic ---
def load_model_and_classes():
    """
    Loads the saved model state and class names.
    This function should be called only once when the server starts.
    """
    # Load class names
    with open(CLASS_NAMES_PATH, 'r') as f:
        class_names = json.load(f)
    print(f"Loaded class names: {class_names}")

    # Re-create the model architecture
    # IMPORTANT: The architecture must be EXACTLY the same as during training
    model = models.resnet18(weights=None) # Start with an untrained model
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(class_names)) # Adapt the final layer

    # Load the trained weights (the state_dict)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    
    # Set the model to evaluation mode
    # This is CRUCIAL for getting correct predictions
    model.eval()
    
    model = model.to(DEVICE)
    
    print(f"Model loaded from {MODEL_PATH} and moved to {DEVICE}.")
    return model, class_names

# --- 3. Define the Image Transformation ---
# This must be IDENTICAL to the validation transforms from your training script
def define_transforms():
    """Defines the image transformations for inference."""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

# --- 4. Load Model and Classes ONCE at startup ---
# This code runs when the module is first imported.
MODEL, CLASS_NAMES = load_model_and_classes()
TRANSFORM = define_transforms()

# --- 5. The Prediction Function ---
def predict(image_bytes: bytes) -> tuple[str, float]:
    """
    Receives image bytes, preprocesses the image, and returns the
    predicted class name and confidence score.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Ensure image is in RGB format (e.g., if it's a PNG with an alpha channel)
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Apply transformations and add a batch dimension
        image_tensor = TRANSFORM(image).unsqueeze(0).to(DEVICE)

        # Make a prediction
        with torch.no_grad(): # Disables gradient calculation for inference
            outputs = MODEL(image_tensor)
            
            # Apply softmax to get probabilities
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # Get the top class and its confidence
            confidence, top_class_index = torch.max(probabilities, 0)
            
            predicted_class = CLASS_NAMES[top_class_index.item()]
            confidence_score = confidence.item()

        return predicted_class, confidence_score

    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        # Return a default or error state
        return "Prediction Error", 0.0