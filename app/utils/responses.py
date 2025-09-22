from typing import Any, Optional
from fastapi import status
from fastapi.responses import JSONResponse


class APIResponse:
    """Standardized API response utility - similar to Express.js res.json()"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK
    ) -> JSONResponse:
        """Return a successful response"""
        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": data
            }
        )
    
    @staticmethod
    def error(
        message: str = "An error occurred",
        error_code: Optional[str] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Any = None
    ) -> JSONResponse:
        """Return an error response"""
        content = {
            "success": False,
            "message": message,
            "error_code": error_code
        }
        
        if details:
            content["details"] = details
            
        return JSONResponse(
            status_code=status_code,
            content=content
        )
    
    @staticmethod
    def created(data: Any = None, message: str = "Created successfully") -> JSONResponse:
        """Return a created response (201)"""
        return APIResponse.success(
            data=data,
            message=message,
            status_code=status.HTTP_201_CREATED
        )
    
    @staticmethod
    def not_found(message: str = "Resource not found") -> JSONResponse:
        """Return a not found response (404)"""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def unauthorized(message: str = "Unauthorized") -> JSONResponse:
        """Return an unauthorized response (401)"""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden(message: str = "Forbidden") -> JSONResponse:
        """Return a forbidden response (403)"""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )