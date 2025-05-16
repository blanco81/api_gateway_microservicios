import datetime
from nanoid import generate
import pytz
from sqlalchemy import Column, DateTime, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.config import settings
from app.utils.mixins import SoftDeleteMixin, TimestampMixin 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from app.config import settings


SCHEMA_NAME = settings.DB_SCHEMA
KEY = settings.DB_SECRET_KEY

metadata = MetaData(schema=SCHEMA_NAME)
Base = declarative_base(metadata=metadata)


class MedicalStaff(Base, SoftDeleteMixin, TimestampMixin):
    __table_args__ = {"schema": SCHEMA_NAME}
    __tablename__ = "medical_staff"
    

    id = Column(String(40), primary_key=True, default=generate)
    name_complete = Column(String(200), nullable=False)
    specialty = Column(String(200), nullable=False)
    license_number = Column(String(200), unique=True)
    logs = relationship("Log", back_populates="staff")

class Shift(Base, SoftDeleteMixin, TimestampMixin): #Turnos
    __table_args__ = {"schema": SCHEMA_NAME}
    __tablename__ = "shifts"

    id = Column(String(40), primary_key=True, default=generate)
    staff_id = Column(String(40), ForeignKey(f"{SCHEMA_NAME}.medical_staff.id"))
    shift_date = Column(Date)
    shift_type = Column(String(200), nullable=False)  # Ej: "Diurno", "Nocturno"
    logs = relationship("Log", back_populates="shift")
    
class Log(Base):
    __table_args__ = {"schema": SCHEMA_NAME}
    __tablename__ = "logs"

    id = Column(String(40), primary_key=True, default=generate)
    action = Column(String(200), nullable=False)  
    date_create = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(pytz.utc))  
    
    staff_id = Column(String(40), ForeignKey(f"{SCHEMA_NAME}.medical_staff.id"))
    staff = relationship("MedicalStaff", back_populates="logs", lazy="selectin")
    
    shift_id = Column(String(40), ForeignKey(f"{SCHEMA_NAME}.shifts.id"))
    shift = relationship("Shift", back_populates="logs", lazy="selectin")