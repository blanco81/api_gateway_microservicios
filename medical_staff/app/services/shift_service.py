from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.models import Shift
from app.schema.staff_models import ShiftCreate, ShiftOut
from app.db.session import get_db

router = APIRouter(prefix="/shifts", tags=["Shifts"])

@router.post("/", response_model=ShiftOut)
async def create_shift(data: ShiftCreate, db: AsyncSession = Depends(get_db)):
    shift = Shift(**data.dict())
    db.add(shift)
    await db.commit()
    await db.refresh(shift)
    return shift

@router.get("/", response_model=list[ShiftOut])
async def list_shifts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Shift))
    return result.scalars().all()