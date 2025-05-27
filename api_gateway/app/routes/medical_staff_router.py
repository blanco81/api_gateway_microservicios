import logging
import httpx
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from app.security.keycloak import has_role
from app.schema.medical_staff_request import StaffCreate, StaffOut, ShiftCreate, ShiftOut
from app.config import settings

router = APIRouter()

# Configuración
TIMEOUT = 10.0  # Tiempo de espera en segundos
MICRO_SERVICE_URL=settings.MEDICAL_STAFF_URL

# Configurar logging
logger = logging.getLogger(__name__)

@router.get("/staff", response_model=list)
async def get_staff_members(user: dict = Depends(has_role("admin"))):    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{MICRO_SERVICE_URL}/staff/")
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
        
@router.post("/staff", response_model=StaffOut)
async def post_staff_members(staff_data: StaffCreate, user: dict = Depends(has_role("admin"))):    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f"{MICRO_SERVICE_URL}/staff/",
                json=jsonable_encoder(staff_data))
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

@router.get("/shift", response_model=list)
async def get_shift(user: dict = Depends(has_role("admin"))):   
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{MICRO_SERVICE_URL}/shift/")
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
        
@router.post("/shift", response_model=ShiftOut)
async def post_shift(shift_data: ShiftCreate, user: dict = Depends(has_role("admin"))):   
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f"{MICRO_SERVICE_URL}/shift/",
                json=jsonable_encoder(shift_data))
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

@router.get("/log_medical_staff", response_model=list)
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