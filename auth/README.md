Keycloak es el proveedor de identidad y autenticación para el proyecto.

- Imagen: `quay.io/keycloak/keycloak:24.0.1`
- Modo: `start-dev`
- Puerto expuesto: `8080`
- Admin: `admin` / `admin`
- Base de datos: PostgreSQL, contenedor `keycloak-db`
- Realm sugerido: `medikall`
- Clientes:
  - `api-gateway`: cliente confidencial con acceso a los scopes requeridos