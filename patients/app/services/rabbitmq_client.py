import asyncio
import aio_pika
import json
from app.config import settings
from aio_pika.exceptions import AMQPConnectionError

async def validate_medical_staff_id(medical_staff_id: str) -> bool:
    try:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    except AMQPConnectionError:
        print("[ERROR] No se pudo conectar a RabbitMQ.")
        return False

    async with connection:
        channel = await connection.channel()
        callback_queue = await channel.declare_queue(exclusive=True)

        corr_id = str(medical_staff_id)
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        async def on_response(message: aio_pika.IncomingMessage):
            print(f"[RESPONSE] Mensaje recibido: {message.body.decode()}")
            if message.correlation_id == corr_id:
                response = json.loads(message.body.decode())
                if not future.done():
                    future.set_result(response.get("valid", False))

        await callback_queue.consume(on_response, no_ack=True)

        # Datos a enviar
        payload = {"medical_staff_id": medical_staff_id}

        print(f"[SEND] Enviando mensaje a la cola '{settings.MEDICAL_STAFF_VALIDATION_QUEUE}': {payload}")

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode(),
                reply_to=callback_queue.name,
                correlation_id=corr_id,
            ),
            routing_key=settings.MEDICAL_STAFF_VALIDATION_QUEUE,
        )

        try:
            return await asyncio.wait_for(future, timeout=5)
        except asyncio.TimeoutError:
            print("[TIMEOUT] No se recibió respuesta del microservicio `medical_staff`.")
            return False
