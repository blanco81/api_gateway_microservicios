# 🏥 Microservicio: Patients

Este microservicio gestiona los datos de pacientes en el ecosistema de MEDIKALL.

## 📦 Estructura

- `app/main.py`: Punto de entrada FastAPI
- `app/schema/`: Modelos Pydantic
- `app/db/`: Conexión y modelos SQLAlchemy
- `app/services/`: Lógica de negocio

## ⚙️ Variables de entorno

Ver archivo `env_example.txt`.

## 🚀 Iniciar servicio

```bash
docker-compose up --build
