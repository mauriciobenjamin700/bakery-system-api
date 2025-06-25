from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.endpoints.ingredient import router as ingredient_router
from app.api.endpoints.product import router as product_router
from app.api.endpoints.report import router as report_router
from app.api.endpoints.sale import router as sale_router
from app.api.endpoints.user import router as user_router
from app.api.middlewares.error import CustomErrorMiddleware

app = FastAPI(
    title="Bakery System API",
    summary="A system to manage bakery sales",
    description="This API is designed to manage bakery sales, including products, ingredients, and users.",
    version="1.0.0",
    root_path="/api",
)

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://bakery-system-web"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)
app.add_middleware(CustomErrorMiddleware)

app.mount("/images", StaticFiles(directory="app/images"), name="images")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request, exc: RequestValidationError
):
    """
    Exception handler for RequestValidationError.

    Args:
        request (Request): The request object.
        exc (RequestValidationError): The exception object.
    Returns:
        JSONResponse: A JSON response with the error details.
    """
    pydantic_errors = exc.errors()
    msg = pydantic_errors[0]["msg"]
    loc = pydantic_errors[0]["loc"]
    field = loc[-1] if isinstance(loc, (list, tuple)) and len(loc) > 0 else loc
    detail = f"{msg} {field} in {loc}"

    return JSONResponse(status_code=422, content={"detail": detail})


app.include_router(ingredient_router)
app.include_router(product_router)
app.include_router(report_router)
app.include_router(sale_router)
app.include_router(user_router)


@app.get("/")
def test_api():
    """
    A test endpoint to check if the API is running.
    Returns:
        dict: A dictionary with a message indicating the API is running.
    """
    return {"detail": "API online!"}
