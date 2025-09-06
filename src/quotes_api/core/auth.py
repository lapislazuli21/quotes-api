from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from .config import get_settings

api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Security(api_key_header)):
    """
    Checks if the provided API key in the 'X-API-Key' header is valid.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key not found.",
        )
    settings = get_settings()
    if api_key == settings.api_key:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )