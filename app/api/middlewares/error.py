from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.errors import (
    ConflictError,
    NotFoundError,
    ValidationError as CustomValidationError
)


# Configurar o logger
logger = logging.getLogger("custom_error_logger")
handler = logging.FileHandler("app/logs/errors.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)


class CustomErrorMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle custom errors.
    """
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except ConflictError as e:

            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )

        except NotFoundError as e:

            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )

        except CustomValidationError as e:

            return JSONResponse(
                status_code=e.status_code,
                content={
                    "detail": e.detail,
                    "field": e.field
                }
            )

        except ValidationError as e:
            # Formatação de erro de validação do Pydantic
            return JSONResponse(
                status_code=422,
                content={"detail": "Validation Error", "errors": e.errors()},
            )
        except HTTPException as e:

            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )
        except Exception as e:
            message = f"Internal Server Error: {str(e)}"
            logger.error(message)
            return JSONResponse(
                status_code=500,
                content={"detail": message},
            )
