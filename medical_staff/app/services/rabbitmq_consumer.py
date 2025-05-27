import aio_pika
import asyncio
import json
from aio_pika import Exchange, ExchangeType
from sqlalchemy import select
from app.db.session import async_session
from app.model.models import MedicalStaff
from app.config import settings

async def handle_message(message: aio_pika.IncomingMessage):
    async with message.process():
        # 1) Decodificar payload JSON
        try:
            payload = json.loads(message.body.decode())
            medical_staff_id = payload.get("medical_staff_id")
            print(f"[RECEIVED] Validando medical_staff_id: {medical_staff_id}")
        except Exception as e:
            print(f"[ERROR] al decodificar mensaje: {e}")
            return

        # 2) Consulta asíncrona a la base de datos
        async with async_session() as session:
            try:
                result = await session.execute(
                    select(MedicalStaff).where(MedicalStaff.id == medical_staff_id)
                )
                staff = result.scalar()
                is_valid = staff is not None
                print(f"[DB] Resultado de consulta: {staff}")
            except Exception as e:
                print(f"[ERROR DB] {e}")
                is_valid = False

        # 3) Preparar respuesta
        response = {"valid": is_valid}
        print(f"[RESPONSE] {response}")

        # 4) Publicar respuesta (CORRECTO para aio_pika 9.5.5)
        if message.reply_to:
            try:
                # Crear el mensaje primero (con body obligatorio)
                msg = aio_pika.Message(
                    body=json.dumps(response).encode(),  # <-- Body es obligatorio
                    correlation_id=message.correlation_id  # <-- Otras propiedades se pasan aquí
                )
                
                # Publicar usando basic_publish (sin el parámetro 'message')
                await message.channel.basic_publish(
                    exchange="",  # Exchange por defecto
                    routing_key=message.reply_to,
                    body=msg.body,          # <-- Pasar body directamente
                    properties=msg.properties  # <-- Pasar propiedades
                )
                print(f"[SENT] Respuesta enviada a '{message.reply_to}'")
            except Exception as e:
                print(f"[ERROR] al enviar respuesta: {e}")

async def consume():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    queue = await channel.declare_queue(
        settings.MEDICAL_STAFF_VALIDATION_QUEUE, durable=True
    )
    await queue.consume(handle_message)
    print(f"[STARTED] Consumidor escuchando en '{settings.MEDICAL_STAFF_VALIDATION_QUEUE}'")
    return connection

if __name__ == "__main__":
    asyncio.run(consume())
