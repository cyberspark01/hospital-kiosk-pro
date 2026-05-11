from pydantic import BaseModel

class PatientCreate(BaseModel):
    name: str
    age: int
    symptoms: str

class AppointmentCreate(BaseModel):
    patient_name: str
    doctor: str
