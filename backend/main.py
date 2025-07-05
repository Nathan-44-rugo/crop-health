# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# --- Import our new REAL prediction function ---
from model_loader import predict

# --- Import the Mistral client ---
from mistral_client import get_treatment_advice

# --- Placeholder for database logging ---
def log_to_database(disease: str, confidence: float, advice: str) -> str:
    import uuid
    log_id = str(uuid.uuid4())
    print(f"LOGGING (id: {log_id}): Disease='{disease}', Confidence={confidence:.2f}")
    return log_id
# ----------------------------------------------------

class DiagnosisResponse(BaseModel):
    disease_class: str
    confidence: float
    treatment_advice: str
    log_id: str

app = FastAPI(title="Crop Health Diagnosis API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Crop Health Diagnosis API is running!"}

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_plant(file: UploadFile = File(...)):
    """
    Receives an image, runs REAL inference, gets treatment advice from Mistral,
    and logs the result.
    """
    try:
        print(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        # 1. Read image bytes from upload
        image_bytes = await file.read()
        print(f"Image bytes length: {len(image_bytes)}")
        
        # 2. Get prediction from our loaded vision model
        disease_prediction, confidence_score = predict(image_bytes)
        print(f"Prediction: {disease_prediction}, Confidence: {confidence_score}")

        # 3. Query Mistral for treatment advice using the disease name
        treatment = get_treatment_advice(disease_prediction)
        print(f"Treatment advice generated: {len(treatment)} characters")

        # 4. Log the complete result
        log_id = log_to_database(
            disease=disease_prediction,
            confidence=confidence_score,
            advice=treatment
        )

        return DiagnosisResponse(
            disease_class=disease_prediction,
            confidence=confidence_score,
            treatment_advice=treatment,
            log_id=log_id,
        )
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise

# Good practice to protect the server run command
if __name__ == "__main__":
    print("Starting server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)