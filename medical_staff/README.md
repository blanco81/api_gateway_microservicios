# 🩺 Microservicio: Medical Staff

Este microservicio forma parte del sistema **MEDIKALL** y se encarga de gestionar la información del personal médico (doctores, enfermeros, técnicos, etc.).

## 📌 Características

- API RESTful basada en FastAPI
- Gestión de CRUD del personal médico
- Autenticación mediante Keycloak
- Conexión a base de datos PostgreSQL
- Comunicación con otros microservicios a través de API Gateway

---

## 🚀 Tecnologías

- Python 3.10
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (migraciones)
- Docker & Docker Compose

---

## ⚙️ Variables de entorno

Asegúrate de configurar las siguientes variables de entorno (puedes copiar `env_example.txt`):

Endpoints principales
La documentación interactiva estará disponible en:
http://localhost:8001/docs

GET /staff/ - Lista todo el personal médico

POST /staff/ - Crea un nuevo profesional

GET /staff/{id} - Consulta por ID

PUT /staff/{id} - Actualiza información

DELETE /staff/{id} - Soft delete
