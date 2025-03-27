"""The healthcheck endpoint."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health", tags=["Health Check"])
async def health_check():
    return JSONResponse(status_code=200, content={"status": "healthy"})
