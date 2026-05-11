from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

router = APIRouter()

@router.post("/book")
def book(app: schemas.AppointmentCreate, db: Session = Depends(SessionLocal)):
    db_app = models.Appointment(**app.dict())
    db.add(db_app)
    db.commit()
    return {"message": "Appointment booked"}
