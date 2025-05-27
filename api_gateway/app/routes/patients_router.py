import logging
import httpx
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from app.security.keycloak import has_role
from app.schema.patients_request import PatientCreate, PatientOut
from app.config import settings

router = APIRouter()

# Configuración
TIMEOUT = 10.0  # Tiempo de espera en segundos
MICRO_SERVICE_URL=settings.PATIENTS_URL

# Configurar logging
logger = logging.getLogger(__name__)

@router.get("/patient", response_model=list)
async def get_patients(user: dict = Depends(has_role("admin"))):    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{MICRO_SERVICE_URL}/patient/")
            response.raise_for_status()
            return response.json()
            
    except httpx.ConnectError as e:
        logger.error(f"Connection error to patients service: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail="Patients service unavailable"
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"Patients service error: {str(e)}")
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
        
@router.post("/patient", response_model=PatientOut)
async def post_patients(patient_data: PatientCreate, user: dict = Depends(has_role("admin"))):    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f"{MICRO_SERVICE_URL}/patient/",
                json=jsonable_encoder(patient_data))
            response.raise_for_status()
            return response.json()
            
    except httpx.ConnectError as e:
        logger.error(f"Connection error to patients service: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail="Patients service unavailable"
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"Patients service error: {str(e)}")
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


@router.get("/log_patients", response_model=list)
async def get_log(user: dict = Depends(has_role("admin"))):   
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{MICRO_SERVICE_URL}/log/")
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