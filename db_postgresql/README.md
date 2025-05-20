Microservicio: db_postgresql
Este microservicio proporciona la base de datos central PostgreSQL utilizada por los distintos componentes del sistema MEDIKALL. Cada microservicio (como medical_staff, appointments, etc.) podrá conectarse a esta base de datos mediante su propio esquema y usuario si es necesario.

Tecnologías
PostgreSQL 15 (contenedor oficial)

Docker Compose

Red compartida medikall-network

Estructura del Proyecto
db_postgresql/
├── docker-compose.yml         # Define el servicio PostgreSQL
├── .env                   
└── README.md

Variables de Entorno
Estas variables se definen dentro del archivo docker-compose.yml:

| Variable           | Valor por defecto | Descripción                               |
| ------------------ | ----------------- | ----------------------------------------- |
| POSTGRES\_USER     | `medikall_admin`  | Usuario administrador de la base de datos |
| POSTGRES\_PASSWORD | `medikall_pass`   | Contraseña del usuario administrador      |
| POSTGRES\_DB       | `medikall_db`     | Nombre de la base de datos principal      |

