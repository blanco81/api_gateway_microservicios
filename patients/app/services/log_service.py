from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.models import Log
from app.schema.patient_models import LogOut
from app.db.session import get_db

router = APIRouter(tags=["Patients"])


@router.get("/", response_model=list[LogOut])
async def list_log(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Log))
    return result.scalars().all()