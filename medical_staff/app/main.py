from fastapi import FastAPI
from app.services import staff_service, shift_service, log_service

app = FastAPI(title="Medical Staff Microservice")
app.include_router(staff_service.router, prefix="/medical_staff")
app.include_router(shift_service.router, prefix="/medical_staff")
app.include_router(log_service.router, prefix="/medical_staff")

