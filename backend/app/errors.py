from fastapi import Request, status
from fastapi.responses import JSONResponse

class DomainError(Exception):
    def __init__(self, message: str, code: str = "domain_error") -> None:
        self.message = message
        self.code = code
        super().__init__(message)

async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:  # type: ignore[override]
    return JSONResponse(
        {"error": {"code": exc.code, "message": exc.message}},
        status_code=status.HTTP_400_BAD_REQUEST,
    )

async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:  # type: ignore[override]
    return JSONResponse(
        {"error": {"code": "internal_error", "message": "An internal error occurred."}},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
