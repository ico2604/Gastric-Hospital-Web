from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.patient import Patient, PatientCreate, PatientUpdate
from app.models.patient import Patient as PatientModel

router = APIRouter()

@router.get("/", response_model=List[Patient])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(PatientModel).offset(skip).limit(limit).all()
    return patients

@router.post("/", response_model=Patient)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = PatientModel(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/{patient_id}", response_model=Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
