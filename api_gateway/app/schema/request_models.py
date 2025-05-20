from typing import Optional
from pydantic import BaseModel
from datetime import date
from datetime import datetime

class StaffCreate(BaseModel):
    name_complete: str
    specialty: str
    license_number: str

class StaffOut(BaseModel):
    id: str
    name_complete: str
    specialty: str
    license_number: str

    class Config:
        orm_mode = True
        
class ShiftCreate(BaseModel):
    staff_id: str
    shift_date: date
    shift_type: str

class ShiftOut(BaseModel):
    id: str
    shift_date: date
    shift_type: str
    staff: Optional[StaffOut]

    class Config:
        orm_mode = True