from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
# from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.asyncio import AsyncSession

# Importações dos routers
from app.api.endpoints.ingredient import router as ingredient_router
from app.api.endpoints.product import router as product_router
from app.api.endpoints.report import router as report_router
from app.api.endpoints.sale import router as sale_router
from app.api.endpoints.user import router as user_router

# Importações adicionais necessárias para a rota direta de teste/fallback
from app.schemas.ingredient import IngredientRequest, IngredientResponse
from app.api.dependencies.db import get_session
from app.api.dependencies.permissions import employer_permission
from app.services.ingredient import IngredientService
from app.schemas.user import UserResponse # Garante que UserResponse esteja disponível para a rota direta
# O CustomErrorMiddleware pode ser importado aqui se estiver em app.api.middlewares.error
# from app.api.middlewares.error import CustomErrorMiddleware # Descomente se for usado


app = FastAPI(
    title="Bakery System API",
    summary="A system to manage bakery sales",
    description="This API is designed to manage bakery sales, including products, ingredients, and users.",
    version="1.0.0",
    root_path="/api", # Mantido como por sua configuração original
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)
# app.add_middleware(CustomErrorMiddleware) # Descomente se estiver usando este middleware


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """
    Exception handler for RequestValidationError.
    """
    pydantic_errors = exc.errors()
    # Assegure-se de que pydantic_errors não está vazio para evitar IndexError
    if pydantic_errors:
        msg = pydantic_errors[0]["msg"]
        # 'loc' pode ser uma tupla de strings ou inteiros. Acessar o último elemento para o nome do campo.
        loc_path = pydantic_errors[0]["loc"]
        field = loc_path[-1] if loc_path else "unknown_field"
        detail = f"{msg} for field '{field}' in {loc_path}" # Mensagem mais robusta
    else:
        detail = "Validation error without specific details."


    return JSONResponse(status_code=422, content={"detail": detail})


# Inclui os APIRouters existentes
app.include_router(ingredient_router)
app.include_router(product_router)
app.include_router(report_router)
app.include_router(sale_router)
app.include_router(user_router)


# --- ROTA DE TESTE DEFINITIVA PARA '/ingredients' (PLURAL) ---
# Esta rota é adicionada DIRETAMENTE ao objeto 'app' para contornar qualquer
# problema de interpretação de prefixos do APIRouter ou root_path no ambiente Docker.
# Ela serve como um fallback para garantir que o POST /ingredients seja reconhecido.
@app.post("/ingredients", status_code=201, tags=["Ingredient"]) # Adicione tags para organização na documentação
async def add_ingredient_direct_from_main(
    request: IngredientRequest,
    _: UserResponse = Depends(employer_permission), # Certifique-se de que UserResponse está importado
    session: AsyncSession = Depends(get_session), # Certifique-se de que get_session está importado
) -> IngredientResponse:
    """
    Endpoint direto para adicionar um ingrediente (plural /ingredients).
    Esta rota é um fallback para garantir que o POST /ingredients seja reconhecido.
    """
    print("\n!!!!!!!!!!!!!!! ROTA /ingredients (PLURAL) ATINGIDA DIRETAMENTE NO main.py !!!!!!!!!!!!!!!!!")
    service = IngredientService(session) # Certifique-se de que IngredientService está importado
    ingredient = await service.add(request, "Adicionado via /ingredients direto")
    return ingredient
# --- FIM DA ROTA DE TESTE DEFINITIVA ---


@app.get("/")
def test_api():
    """
    A test endpoint to check if the API is running.
    """
    return {"detail": "API online!"}