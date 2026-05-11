
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Path Setup --------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_PATH = os.path.join(BASE_DIR, "frontend")

# Serve static files (if you add CSS/JS later)
app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

# -------------------- Models --------------------
class Patient(BaseModel):
    name: str
    age: int
    symptoms: str

class Appointment(BaseModel):
    patient_name: str
    doctor: str

# -------------------- Dummy DB --------------------
patients: List[Patient] = []
appointments: List[Appointment] = []

doctors = {
    "fever": "General Physician",
    "cough": "General Physician",
    "heart": "Cardiologist",
    "skin": "Dermatologist"
}

# -------------------- Routes --------------------

# ✅ THIS IS THE IMPORTANT CHANGE
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))

@app.post("/register")
def register_patient(patient: Patient):
    patients.append(patient)
    return {"message": "Patient registered successfully"}

@app.post("/suggest-doctor")
def suggest_doctor(symptoms: dict):
    symptom = symptoms.get("symptoms", "").lower()
    for key in doctors:
        if key in symptom:
            return {"doctor": doctors[key]}
    return {"doctor": "General Physician"}

@app.post("/book")
def book_appointment(appointment: Appointment):
    appointments.append(appointment)
    return {"message": "Appointment booked"}

@app.get("/appointments")
def get_appointments():
    return appointments


