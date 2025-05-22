from json import loads

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_session
from app.api.dependencies.permissions import employer_permission
from app.core.generate.ids import id_generator
from app.schemas.message import Message
from app.schemas.product import (
    ProductBatchRequest,
    ProductBatchUpdate,
    ProductRequest,
    ProductResponse,
    ProductUpdate,
    RecipeRequest,
)
from app.schemas.user import UserResponse
from app.services import ProductService
from app.services.image import ImageService

router = APIRouter(prefix="/product", tags=["product"])


@router.post("/", status_code=201)
async def add_product(
    image: UploadFile = File(),
    form_data: str = Form(),
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> ProductResponse:
    """
    # A route to add a product.

    Product data in JSON format should be sent in the form data with this format:

        - name (str): The name of the product.
        - price_cost (float): The cost price of the product.
        - price_sale (float): The sale price of the product.
        - measure (MeasureEnum): The measure of the product.
        - description (str): The description of the product.
        - mark (str): The mark of the product.
        - min_quantity (float): The minimum quantity of the product.
        - recipe (list[PortionRequest] | None): The recipe of the product.
        - quantity (float): The quantity of the product.
        - validity (date | None): The validity date of the product.

    ## Example
        {
            "name": "Pão Francês",
            "price_cost": 2.50,
            "price_sale": 4.00,
            "measure": "u",
            "description": "Pão francês crocante e fresquinho.",
            "mark": "Padaria Central",
            "min_quantity": 10,
            "recipe": [
                {
                "ingredient_id": "abc123",
                "quantity": 0.5,
                "measure": "KG"
                }
            ],
            "quantity": 100,
            "validity": "2025-06-01"
        }

    ## Args:
        - request (ProductRequest): The request object containing product data.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - ProductResponse: The response object containing the added product data.
    """
    form_data = loads(form_data)

    request = ProductRequest(**form_data)

    file_path = await ImageService.upload_image(
        image=image, filename=id_generator()
    )

    service = ProductService(session)
    response = await service.add(request, file_path)
    return response


@router.get("/")
async def get_products(
    product_id: str | None = None,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> list[ProductResponse]:
    """
    # A route to get all products.

    ## Args:
        - product_id (str | None): The ID of the product to retrieve.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - list[ProductResponse]: A list of product response objects.
    """
    service = ProductService(session)
    if product_id:
        products = await service.get_by_id(product_id)
        return [products]
    products = await service.get_all()
    return products


@router.put("/{product_id}")
async def update_product(
    product_id: str,
    request: ProductUpdate,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> ProductResponse:
    """
    # A route to update a product.

    ## Args:
        - product_id (str): The ID of the product to update.
        - request (ProductUpdate): The request object containing updated product data.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - ProductResponse: The response object containing the updated product data.
    """
    service = ProductService(session)
    response = await service.update(product_id, request)
    return response


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> Message:
    """
    # A route to delete a product.

    ## Args:
        - product_id (str): The ID of the product to delete.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        None
    """
    service = ProductService(session)
    response = await service.delete(product_id)
    return response


@router.post("/batch", status_code=201)
async def add_product_batch(
    request: ProductBatchRequest,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> ProductResponse:
    """
    # A route to add a batch of products.

    ## Args:
        - request (ProductBatchRequest): The request object containing product data.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - list[ProductResponse]: A list of response objects containing the added product data.
    """
    service = ProductService(session)
    response = await service.add_product_batch(request)
    return response


@router.put("/batch/{product_batch_id}")
async def update_product_batch(
    product_batch_id: str,
    request: ProductBatchUpdate,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> ProductResponse:
    """
    # A route to update a batch of products.

    ## Args:
        - request (ProductBatchUpdate): The request object containing updated product data.
        - session (AsyncSession): The database session.
    ## Returns:
        - Message: A message indicating the result of the operation.
    """
    service = ProductService(session)
    response = await service.update_product_batch(product_batch_id, request)
    return response


@router.delete("/batch/{product_batch_id}")
async def delete_product_batch(
    product_batch_id: str,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> Message:
    """
    # A route to delete a batch of products.

    ## Args:
        - product_batch_id (str): The ID of the product batch to delete.
        _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - Message: A message indicating the result of the operation.
    """
    service = ProductService(session)
    response = await service.delete_product_batch(product_batch_id)
    return response


@router.post("/recipe", status_code=201)
async def add_recipe(
    request: RecipeRequest,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> ProductResponse:
    """
    # A route to add a recipe.

    ## Args:
        - request (RecipeRequest): The request object containing recipe data.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - ProductResponse: The response object containing the added recipe data.
    """
    service = ProductService(session)
    response = await service.add_recipe(request)
    return response


@router.put("/recipe/{portion_id}/{quantity}")
async def update_recipe(
    portion_id: str,
    quantity: float,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> ProductResponse:
    """
    # A route to update a recipe.

    ## Args:
        - portion_id (str): The ID of the recipe to update.
        - quantity (float): The new quantity for the recipe.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - ProductResponse: The response object containing the updated recipe data.
    """
    service = ProductService(session)
    response = await service.update_recipe(portion_id, quantity)
    return response


@router.delete("/recipe/{portion_id}")
async def delete_recipe(
    recipe_id: str,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> Message:
    """
    # A route to delete a recipe.

    ## Args:
        - recipe_id (str): The ID of the recipe to delete.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - Message: A message indicating the result of the operation.
    """
    service = ProductService(session)
    response = await service.delete_recipe(recipe_id)
    return response
