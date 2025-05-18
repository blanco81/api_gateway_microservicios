from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.models import MedicalStaff, Log
from app.schema.staff_models import StaffCreate, StaffOut
from app.db.session import get_db

router = APIRouter(prefix="/staff", tags=["Medical Staff"])

@router.post("/", response_model=StaffOut)
async def create_staff(data: StaffCreate, db: AsyncSession = Depends(get_db)):
    staff = MedicalStaff(**data.dict())
    db.add(staff)
    await db.commit()
    await db.refresh(staff)
    
    staff_log = Log(
        action=f"Staff {staff.name_complete} especialista en {staff.specialty}, fue creado.",
        date_create=datetime.now(pytz.utc),
        staff_id=staff.id
    )
    db.add(staff_log)
    await db.commit()
    await db.refresh(staff_log)
    
    return staff

@router.get("/", response_model=list[StaffOut])
async def list_staff(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MedicalStaff))
    return result.scalars().all()