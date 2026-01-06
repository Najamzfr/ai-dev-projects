"""Custom exceptions and error handling."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class APIException(Exception):
    """Base API exception."""
    
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 500,
        details: dict | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


# Specific exception types
class ValidationError(APIException):
    """Validation error (400)."""
    
    def __init__(self, message: str, details: dict | None = None):
        super().__init__("VALIDATION_ERROR", message, 400, details)


class ScoreInvalidError(APIException):
    """Invalid score error (400)."""
    
    def __init__(self, message: str = "Score must be between 0 and 999999"):
        super().__init__("SCORE_INVALID", message, 400)


class UsernameInvalidError(APIException):
    """Invalid username error (400)."""
    
    def __init__(self, message: str = "Username doesn't meet requirements"):
        super().__init__("USERNAME_INVALID", message, 400)


class DuplicateSubmissionError(APIException):
    """Duplicate submission error (409)."""
    
    def __init__(self, message: str = "Same score submitted recently"):
        super().__init__("DUPLICATE_SUBMISSION", message, 409)


class RateLimitError(APIException):
    """Rate limit exceeded error (429)."""
    
    def __init__(self, message: str = "Too many requests"):
        super().__init__("RATE_LIMIT_EXCEEDED", message, 429)


class NotFoundError(APIException):
    """Resource not found error (404)."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__("NOT_FOUND", message, 404)


class ServerError(APIException):
    """Internal server error (500)."""
    
    def __init__(self, message: str = "Internal server error"):
        super().__init__("SERVER_ERROR", message, 500)


class DatabaseError(APIException):
    """Database operation error (500)."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__("DATABASE_ERROR", message, 500)


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """Handle custom API exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": {"validation_errors": errors},
            }
        },
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "details": {},
            }
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    import logging
    
    logger = logging.getLogger(__name__)
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.error(
        "Unhandled exception",
        extra={"request_id": request_id, "error": str(exc)},
        exc_info=True,
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": {},
            }
        },
    )

