from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakError, KeycloakAuthenticationError
from app.config import settings
import logging

# Configuración del logger
logger = logging.getLogger(__name__)

# Configuración del cliente Keycloak
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=None,  # Configurar si el cliente es confidencial
    verify=True
)

bearer_scheme = HTTPBearer()

async def verify_token_str(token: str):    
    try:
        # Obtener la clave pública de Keycloak
        public_key = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
        
        # Verificación completa del token
        options={
            "verify_signature": True,
            "verify_exp": True,
            "verify_iat": True,
            "verify_nbf": True,
            "verify_iss": True,
            "verify_sub": True,
            "verify_jti": True,
            "verify_aud": False     # <<< desactiva la validación de audiencia
        }
        
        payload = keycloak_openid.decode_token(
            token,
            key=public_key,
            options=options
        )
        return {"active": True, "payload": payload}
        
    except KeycloakAuthenticationError as e:
        logger.error(f"Token verification failed: {str(e)}")
        return {"active": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {str(e)}")
        return {"active": False, "error": "Token validation error"}

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        # Obtener la clave pública correctamente formateada
        public_key = f"-----BEGIN PUBLIC KEY-----\n{keycloak_openid.public_key()}\n-----END PUBLIC KEY-----"
        
        # Decodificar el token con la audiencia correcta
        return keycloak_openid.decode_token(
            token,
            key=public_key,
            options={
                "verify_signature": True,
                "verify_aud": True,
                "verify_exp": True,
                "verify_aud": False,     # <<< desactiva la validación de audiencia
                "audience": settings.KEYCLOAK_CLIENT_ID  # Asegurar que valide contra el client_id correcto
            }
        )
    except KeycloakAuthenticationError as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
    )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Internal authentication error"
        )

def has_role(required_role: str):
    async def role_checker(payload: dict = Depends(verify_token)):
        # Verificar tanto roles de realm como de cliente
        realm_roles = payload.get("realm_access", {}).get("roles", [])
        client_roles = payload.get("resource_access", {}).get(settings.KEYCLOAK_CLIENT_ID, {}).get("roles", [])
        
        if required_role not in realm_roles and required_role not in client_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required role: {required_role}"
            )
        return payload
    return role_checker