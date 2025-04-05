from fastapi import (
    FastAPI,
    Request
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.endpoints.user import router as user_router
from app.api.middlewares.error import CustomErrorMiddleware


app = FastAPI(
    title="Template de API com FastAPI",
    summary="Um modelo de API com FastAPI",
    description="Um modelo de API com FastAPI para ajudar pessoas a começar a desenvolver suas APIs de forma organizada",
    version="0.0.1",
    root_path="/api"
)

# Configurando o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"]
)
app.add_middleware(CustomErrorMiddleware)

# Sobrescrevendo o manipulador de exceções para erros de validação do Pydantic
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    pydantic_errors = exc.errors()
    msg = pydantic_errors[0]["msg"]
    loc, field = pydantic_errors[0]["loc"]
    detail = f"{msg} {field} in {loc}"

    return JSONResponse(
        status_code=422,
        content={"detail": detail}
    )

# Incluindo os roteadores
app.include_router(user_router)


@app.get('/')
def test_api():
    return {"detail": "API rodando!"}
