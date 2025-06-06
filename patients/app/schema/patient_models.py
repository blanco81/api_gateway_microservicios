from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PatientCreate(BaseModel):
    name_complete: str
    medical_staff_id: str

class PatientOut(BaseModel):
    id: str
    name_complete: str
    medical_staff_id: str

    class Config:
        from_attributes = True
        
class LogOut(BaseModel):
    id: str
    action: str
    date_create: datetime
    patient_id: Optional[str]

    class Config:
        from_attributes = True