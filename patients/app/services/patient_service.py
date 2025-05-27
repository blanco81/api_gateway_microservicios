from datetime import datetime
from fastapi import APIRouter, Depends
import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model.models import Patient, Log
from app.schema.patient_models import PatientCreate, PatientOut
from app.services.rabbitmq_client import validate_medical_staff_id
from app.db.session import get_db


router = APIRouter(tags=["Patients"])

@router.get("/", response_model=list[PatientOut])
async def get_patients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient))
    return result.scalars().all()


@router.post("/", response_model=PatientOut)
async def create_patient(data: PatientCreate, db: AsyncSession = Depends(get_db)):
    is_valid = await validate_medical_staff_id(data.medical_staff_id)
    if not is_valid:
        raise ValueError("El ID del personal médico no es válido.")

    patient = Patient(**data.dict())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    
    patient_log = Log(
        action=f"Patient {patient.name_complete}, fue creado.",
        date_create=datetime.now(pytz.utc),
        patient_id=patient.id
    )
    db.add(patient_log)
    await db.commit()
    await db.refresh(patient_log)
    
    return patient


