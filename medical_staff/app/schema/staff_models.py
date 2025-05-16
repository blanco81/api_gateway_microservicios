from pydantic import BaseModel
from datetime import date

class StaffCreate(BaseModel):
    name_complete: str
    specialty: str
    license_number: str

class StaffOut(BaseModel):
    id: int
    name_complete: str
    specialty: str
    license_number: str

    class Config:
        orm_mode = True

class ShiftCreate(BaseModel):
    staff_id: int
    shift_date: date
    shift_type: str

class ShiftOut(BaseModel):
    id: int
    shift_date: date
    shift_type: str

    class Config:
        orm_mode = True