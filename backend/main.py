# main.py
from fastapi import FastAPI, UploadFile, File
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

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_plant(file: UploadFile = File(...)):
    """
    Receives an image, runs REAL inference, gets treatment advice from Mistral,
    and logs the result.
    """
    # 1. Read image bytes from upload
    image_bytes = await file.read()
    
    # 2. Get prediction from our loaded vision model
    disease_prediction, confidence_score = predict(image_bytes)

    # 3. Query Mistral for treatment advice using the disease name
    treatment = get_treatment_advice(disease_prediction)

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

# Good practice to protect the server run command
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)