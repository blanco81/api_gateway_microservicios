from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.models import MedicalStaff
from app.schema.staff_models import StaffCreate, StaffOut
from app.db.session import get_db

router = APIRouter(prefix="/staff", tags=["Medical Staff"])

@router.post("/", response_model=StaffOut)
async def create_staff(data: StaffCreate, db: AsyncSession = Depends(get_db)):
    staff = MedicalStaff(**data.dict())
    db.add(staff)
    await db.commit()
    await db.refresh(staff)
    return staff

@router.get("/", response_model=list[StaffOut])
async def list_staff(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MedicalStaff))
    return result.scalars().all()