from fastapi import APIRouter, HTTPException, Depends
import httpx
from app.security.keycloak import has_role
from fastapi.encoders import jsonable_encoder
import logging

router = APIRouter()

# Configuración
MEDICAL_STAFF_URL = "http://localhost:8001"  # Usar nombre del servicio en Docker o URL correcta
TIMEOUT = 10.0  # Tiempo de espera en segundos

# Configurar logging
logger = logging.getLogger(__name__)

@router.get("/api/v1/staff/", response_model=list)
async def get_staff_members(user: dict = Depends(has_role("admin"))):    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{MEDICAL_STAFF_URL}/staff/")
            response.raise_for_status()
            return response.json()
            
    except httpx.ConnectError as e:
        logger.error(f"Connection error to medical service: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail="Medical service unavailable"
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"Medical service error: {str(e)}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=jsonable_encoder(e.response.json())
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.get("/api/v1/shift/", response_model=list)
async def get_shift(user: dict = Depends(has_role("admin"))):   
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{MEDICAL_STAFF_URL}/shift/")
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=jsonable_encoder(e.response.json())
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/api/v1/log/", response_model=list)
async def get_log(user: dict = Depends(has_role("admin"))):   
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{MEDICAL_STAFF_URL}/log/")
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=jsonable_encoder(e.response.json())
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )