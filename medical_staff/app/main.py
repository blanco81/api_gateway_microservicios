from fastapi import FastAPI
from app.services import staff_service, shift_service

app = FastAPI(title="Medical Staff Microservice")
app.include_router(staff_service.router)
app.include_router(shift_service.router)

