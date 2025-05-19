from datetime import datetime
from fastapi import APIRouter, Depends
import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.model.models import Shift, Log
from app.schema.staff_models import ShiftCreate, ShiftOut
from app.db.session import get_db

router = APIRouter(tags=["Medical Staff"])

@router.get("/", response_model=list[ShiftOut])
async def list_shifts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Shift).options(selectinload(Shift.staff)))
    return result.scalars().all()

@router.post("/", response_model=ShiftOut)
async def create_shift(data: ShiftCreate, db: AsyncSession = Depends(get_db)):
    shift = Shift(**data.dict())
    db.add(shift)
    await db.commit()
    await db.refresh(shift)
    
    shift_log = Log(
        action=f"Shift {shift.shift_type} con especialista {shift.staff_id}, fue creado.",
        date_create=datetime.now(pytz.utc),
        shift_id=shift.id
    )
    db.add(shift_log)
    await db.commit()
    await db.refresh(shift_log)
    
    return shift

