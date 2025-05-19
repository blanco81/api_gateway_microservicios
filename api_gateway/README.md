# 🛡️ API Gateway - MEDIKALL

Este microservicio actúa como puerta de entrada (API Gateway) para el ecosistema de microservicios de la plataforma **MEDIKALL**. Su principal responsabilidad es manejar:

- La autenticación y autorización de solicitudes entrantes mediante **Keycloak**.
- La validación de tokens JWT usando claves públicas del servidor de identidad.
- La redirección segura hacia los microservicios correspondientes.
- El soporte de middleware y dependencias de seguridad basadas en roles.

---

## 📦 Estructura del Proyecto

api_gateway/
├── app/
│ ├── config.py # Variables de entorno y configuración de Keycloak
│ ├── main.py # Inicialización de FastAPI y middleware de autenticación
│ ├── security/
│ │ └── keycloak.py # Lógica de validación de tokens y roles
│ └── routes/
│ └── router.py # Rutas gestionadas por el Gateway
├── requirements.txt
├── Dockerfile
└── README.md


## ⚙️ Requisitos

- Python 3.10+
- Docker y Docker Compose (recomendado)
- Keycloak configurado y en ejecución
- Variables de entorno para conexión con Keycloak

---

## 🔐 Configuración de Keycloak

Este microservicio espera un servidor Keycloak disponible en la URL y realm especificados. Asegúrate de tener:

- Un **cliente confidencial (confidential client)** configurado.
- Roles definidos en el realm o cliente.
- Habilitado el protocolo OpenID Connect.

Ejemplo de variables esperadas:

```env
KEYCLOAK_SERVER_URL=http://keycloak:8080
KEYCLOAK_REALM=medikall
KEYCLOAK_CLIENT_ID=api-gateway

Ejemplo de protección por rol en una ruta:

from app.security.keycloak import has_role

@router.get("/admin-only", dependencies=[Depends(has_role("admin"))])
async def admin_route():
    return {"message": "Solo usuarios con rol admin pueden ver esto."}
