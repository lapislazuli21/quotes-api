from fastapi import FastAPI

from .api.v1.routes_health import router as health_router
from .core.config import get_settings


def create_app() -> FastAPI:
    """Factory function to create and configure the FastAPI app."""
    app = FastAPI(
        title=get_settings().project_name,
        version=get_settings().version,
        description="An API for managing and serving quotes.",
    )

    # Include routers
    app.include_router(health_router, prefix=get_settings().api_prefix, tags=["Health"])

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "quotes_api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
