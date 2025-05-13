from datetime import datetime

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.errors import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    ServerError,
    UnauthorizedError,
)
from app.core.errors import ValidationError as CustomValidationError
from app.core.security.tokens import TokenManager
from app.logging import LogManager
from app.schemas.user import TokenData


class CustomErrorMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle custom errors.
    """

    async def dispatch(self, request: Request, call_next):
        """
        A method to dispatch the request and handle errors.
        - Args:
            - request: The request object.
            - call_next: The next middleware or endpoint to call.
        - Returns:
            - response: The response object.
        """
        try:
            start_request = datetime.now()

            response = await call_next(request)

            end_request = datetime.now()

            duration = (
                end_request - start_request
            ).total_seconds() * 1000  # Milliseconds

            LogManager.create_info_log(
                **self.get_log_data(request), request_time=duration
            )
            return response

        except BadRequestError as e:
            self.register_error_log(request, e)

            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )

        except ConflictError as e:

            self.register_error_log(request, e)

            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )

        except NotFoundError as e:

            self.register_error_log(request, e)

            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )

        except ServerError as e:

            self.register_error_log(request, e)

            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )

        except UnauthorizedError as e:

            self.register_error_log(request, e)

            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )

        except CustomValidationError as e:

            self.register_error_log(request, e)

            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail, "field": e.field},
            )

        except ValidationError as e:

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

            return JSONResponse(
                status_code=500,
                content={"detail": message},
            )

    def get_log_data(self, request: Request):
        """
        A method to get log data from the request.
        - Args:
            - request: The request object.
        - Returns:
            - dict: A dictionary containing log data.
        """
        data = {}

        token = request.headers.get("Authorization")

        agente = request.client.host if request.client else "N/A"
        agente_role = None

        if token and "Bearer" in token:
            token = token.split(" ")[1]
            payload = TokenManager.verify_token(token)
            token = TokenData(**payload)
            agente = token.user_id
            agente_role = token.user_role.value

        data["action"] = request.method
        data["local"] = request.url.path
        data["agente"] = agente
        data["agente_role"] = agente_role

        return data

    def register_error_log(self, request: Request, error):
        """
        A method to register error logs.
        - Args:
            - request: The request object.
            - error: The error object.
        - Returns:
            - None
        """
        data = self.get_log_data(request)

        LogManager.create_error_log(
            action=data["action"],
            agente=data["agente"],
            agente_role=data["agente_role"],
            status=error.status_code,
            detail=error.detail,
        )
