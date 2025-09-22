from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.utils.responses import APIResponse


class CustomHTTPException(HTTPException):
    """Custom HTTP Exception with additional fields"""
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = None,
        details: dict = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details
        super().__init__(status_code=status_code, detail=message)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Global HTTP exception handler"""
    if isinstance(exc, CustomHTTPException):
        return APIResponse.error(
            message=exc.message,
            error_code=exc.error_code,
            status_code=exc.status_code,
            details=exc.details
        )
    
    return APIResponse.error(
        message=str(exc.detail),
        status_code=exc.status_code
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle validation errors"""
    return APIResponse.error(
        message="Validation error",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details=str(exc)
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions"""
    return APIResponse.error(
        message="Internal server error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        details=str(exc) if hasattr(exc, '__str__') else "Unknown error"
    )