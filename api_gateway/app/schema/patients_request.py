from typing import Optional
from pydantic import BaseModel
from datetime import date
from datetime import datetime

class PatientCreate(BaseModel):
    name_complete: str
    medical_staff_id: str

class PatientOut(BaseModel):
    id: str
    name_complete: str
    medical_staff_id: str

    class Config:
        from_attributes = True        
