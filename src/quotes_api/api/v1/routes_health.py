from fastapi import APIRouter

router = APIRouter()

@router.get("/health", summary="Health Check", response_model=dict)
async def health_check():
    """
    Simple health check endpoint to verify API is running.
    """
    return {"status": "ok"}
