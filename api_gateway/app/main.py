from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from app.routes.router import router
from app.security.keycloak import verify_token_str, verify_token
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
import httpx
from datetime import datetime
import os

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme para documentación Swagger
bearer_scheme = HTTPBearer()

# Lista de rutas públicas que no requieren autenticación
PUBLIC_ROUTES = {
    "/",
    "/api/v1/health",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/favicon.ico"
}

@app.get("/api/v1/health", tags=["Monitoring"], summary="Health Check", description="Verifica el estado del servicio y sus dependencias")
async def health_check():    
    health_status = {
        "status": "OK",
        "timestamp": datetime.utcnow().isoformat(),
        "service": os.getenv("SERVICE_NAME", "api-gateway"),
        "version": os.getenv("VERSION", "1.0.0"),
        "dependencies": {}
    }

    # Verificar conexión con Keycloak
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{os.getenv('KEYCLOAK_SERVER_URL')}/realms/{os.getenv('KEYCLOAK_REALM')}")
            health_status["dependencies"]["keycloak"] = {
                "status": "OK" if response.status_code == 200 else "ERROR",
                "response_time_ms": response.elapsed.total_seconds() * 1000
            }
    except Exception as e:
        health_status["dependencies"]["keycloak"] = {
            "status": "ERROR",
            "error": str(e)
        }
        health_status["status"] = "WARNING"

    # Aquí añadir más verificaciones de dependencias

    return JSONResponse(
        content=health_status,
        status_code=200 if health_status["status"] == "OK" else 503
    )

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if any(request.url.path.startswith(route) for route in PUBLIC_ROUTES):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Formato de token inválido. Use: Bearer <token>"
        )

    token = auth_header[7:].strip()
    
    try:
        verification = await verify_token_str(token)
        if not verification.get("active"):
            raise HTTPException(
                status_code=401,
                detail=verification.get("error", "Token inválido")
            )
        
        request.state.user = verification["payload"]
        return await call_next(request)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
           status_code=500,
            detail=f"Error de autenticación: {str(e)}"
        )

# Incluir el router principal
app.include_router(router)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "API Service is running"}