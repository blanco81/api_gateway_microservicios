from fastapi import FastAPI
from app.services import patient_service, log_service

app = FastAPI(title="Patients Microservice")
app.include_router(patient_service.router, prefix="/patient")
app.include_router(log_service.router, prefix="/log")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=False)