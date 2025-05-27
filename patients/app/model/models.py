import datetime
from nanoid import generate
import pytz
from sqlalchemy import Column, DateTime, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import StringEncryptedType
from app.config import settings
from app.utils.mixins import SoftDeleteMixin, TimestampMixin 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from app.config import settings


SCHEMA_NAME = settings.DB_SCHEMA
KEY = settings.DB_SECRET_KEY

metadata = MetaData(schema=SCHEMA_NAME)
Base = declarative_base(metadata=metadata)


class Patient(Base, SoftDeleteMixin, TimestampMixin):
    __table_args__ = {"schema": SCHEMA_NAME}
    __tablename__ = "patients"
    

    id = Column(String(40), primary_key=True, default=generate)
    name_complete = Column(String(200), nullable=False)
    medical_staff_id = Column(String(40), nullable=False)  
    logs = relationship("Log", back_populates="patient")
    
class Log(Base):
    __table_args__ = {"schema": SCHEMA_NAME}
    __tablename__ = "logs"

    id = Column(String(40), primary_key=True, default=generate)
    action = Column(String(200), nullable=False)  
    date_create = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(pytz.utc))  
    
    patient_id = Column(String(40), ForeignKey(f"{SCHEMA_NAME}.patients.id"))
    patient = relationship("Patient", back_populates="logs", lazy="selectin")