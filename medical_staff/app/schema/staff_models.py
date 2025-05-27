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
        from_attributes = True

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
        from_attributes = True
        
class LogOut(BaseModel):
    id: str
    action: str
    date_create: datetime
    staff_id: Optional[str]
    shift_id: Optional[str]

    class Config:
        from_attributes = True