# app/main.py
from fastapi import FastAPI
from app.services import staff_service, shift_service, log_service
from app.services.rabbitmq_consumer import consume

app = FastAPI(title="Medical Staff Microservice")
app.include_router(staff_service.router, prefix="/staff")
app.include_router(shift_service.router, prefix="/shift")
app.include_router(log_service.router, prefix="/log")

# Variable para mantener la conexión
rabbitmq_connection = None

@app.on_event("startup")
async def startup_event():
    global rabbitmq_connection
    rabbitmq_connection = await consume()  # Lanzamos el consumidor al iniciar

@app.on_event("shutdown")
async def shutdown_event():
    if rabbitmq_connection:
        await rabbitmq_connection.close()  # Cerramos la conexión con RabbitMQ al apagar
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=False)
