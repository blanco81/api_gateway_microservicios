MEDIKALL - Plataforma de Gestión de Servicios de Salud
MEDIKALL es una plataforma modular desarrollada bajo una arquitectura de microservicios, orientada a optimizar la gestión de servicios médicos en clínicas y hospitales. El sistema permite la integración de múltiples áreas como la administración de personal médico, gestión de pacientes, programación de citas, y más, ofreciendo una solución escalable, segura y eficiente.

🚀 Características principales
🔐 Autenticación centralizada con Keycloak para control de acceso seguro.

⚙️ Microservicios independientes para cada módulo (personal, pacientes, citas, etc.).

📦 Base de datos PostgreSQL con esquemas separados por servicio.

🐇 Comunicación entre servicios mediante RabbitMQ o API Gateway.

📊 Gestión de datos mediante SQLAlchemy y migraciones por microservicio con Alembic.

🌍 Preparado para escalar y desplegar en entornos distribuidos (Docker, Kubernetes...).

🧱 Estructura del proyecto
/medikall
├── gateway/                # API Gateway
├── auth/                   # Servicio de autenticación (Keycloak)
├── medical_staff/          # Microservicio para gestión de personal
├── patients/               # Microservicio para gestión de pacientes
├── appointments/           # Microservicio para programación de citas
└── docker-compose.yml      # Orquestación de servicios

🛠 Tecnologías utilizadas
FastAPI – Backend moderno, rápido y asincrónico

PostgreSQL – Base de datos relacional robusta

SQLAlchemy + Alembic – ORM y control de versiones de la base de datos

RabbitMQ – Cola de mensajes para comunicación entre servicios

Keycloak – Autenticación y gestión de usuarios

Docker – Contenedores para despliegue

📚 Objetivo del proyecto
Desarrollar una plataforma flexible y modular que permita a instituciones de salud mejorar la gestión de sus procesos internos, facilitando el acceso a la información, automatizando tareas administrativas y permitiendo una atención más eficiente y segura a los pacientes.
