from json import loads
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.db import get_session
from app.api.dependencies.permissions import employer_permission
from app.core.generate.ids import id_generator
from app.schemas.ingredient import (
    IngredientBatchRequest,
    IngredientRequest,
    IngredientResponse,
)
from app.schemas.message import Message
from app.schemas.user import UserResponse
from app.services.image import ImageService
from app.services.ingredient import IngredientService

router = APIRouter(prefix="/ingredient", tags=["Ingredient"])


@router.post("/", status_code=201)
async def add_ingredient(
    image: UploadFile = File(),
    form_data: str = Form(),
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> IngredientResponse:
    """
    # A route to add an ingredient.

    ## Ingredient Data:

    Send the ingredient data as a JSON string in the form data with this format:

        - name (str): The name of the ingredient
        - measure (MeasureEnum): The measure of the ingredient
        - mark (str): The mark of the ingredient
        - description (str): The description of the ingredient
        - value (float): The value of the ingredient
        - min_quantity (float): The minimum quantity of the ingredient
        - validity (date | None): The validity of the ingredient
        - quantity (float): The quantity of the ingredient

    ## Example:

        {
            "name": "Farinha de Trigo",
            "measure": "kg",
            "mark": "Dona Benta",
            "description": "Farinha de trigo tipo 1, ideal para pães e bolos.",
            "value": 5.75,
            "min_quantity": 20,
            "validity": "2025-12-31",
            "quantity": 100
        }

    ## Args:
        - image (UploadFile): The image file of the ingredient.
        - form_data (str): The form data containing ingredient details.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - IngredientResponse: The response object containing the added ingredient data.
    """

    form_data = loads(form_data)

    request = IngredientRequest(**form_data)

    file_path = await ImageService.upload_image(
        image=image,
        filename=id_generator()
    )

    service = IngredientService(session)
    ingredient = await service.add(request, file_path)
    return ingredient


@router.get("/", response_model=list[IngredientResponse])
async def get_ingredients(
    ingredient_id: str | None = None,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> list[IngredientResponse]:
    """
    # A route to get all ingredients.

    ## Args:
        - ingredient_id (str | None): The ID of the ingredient to retrieve.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - list[IngredientResponse]: A list of ingredient response objects.
    """
    service = IngredientService(session)
    if ingredient_id:
        ingredients = await service.get_by_id(ingredient_id)
        return [ingredients]
    ingredients = await service.get_all()
    return ingredients


@router.put("/{ingredient_id}", status_code=200)
async def update_ingredient(
    ingredient_id: str,
    request: IngredientRequest,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> IngredientResponse:
    """
    #  A route to update an ingredient.

    ## Args:
        - ingredient_id (str): The ID of the ingredient to be updated.
        - request (IngredientRequest): The request object containing updated ingredient data.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - IngredientResponse: The response object containing the updated ingredient data.
    """
    service = IngredientService(session)
    ingredient = await service.update(ingredient_id, request)
    return ingredient


@router.delete("/{ingredient_id}", status_code=200)
async def delete_ingredient(
    ingredient_id: str,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> Message:
    """
    # A route to delete an ingredient.

    ## Args:
        - ingredient_id (str): The ID of the ingredient to be deleted.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - Message: A message indicating the result of the deletion.
    """
    service = IngredientService(session)
    response = await service.delete(ingredient_id)
    return response


@router.post("/batch", status_code=201)
async def add_ingredient_batch(
    request: IngredientBatchRequest,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> IngredientResponse:
    """
    # A route to add a batch of ingredients.

    ## Args:
        - request (IngredientBatchRequest): The request object containing ingredient data.
        - _: UserResponse: The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - IngredientResponse: The response object containing the added ingredient data.
    """
    service = IngredientService(session)
    ingredient = await service.add_batch(request)
    return ingredient


@router.put("/batch/{batch_id}", status_code=200)
async def update_ingredient_batch(
    batch_id: str,
    request: IngredientBatchRequest,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> IngredientResponse:
    """
    # A route to update a batch of ingredients.
    ## Args:
        - batch_id (str): The ID of the batch to be updated.
        - request (IngredientBatchRequest): The request object containing updated ingredient data.
        - _: UserResponse: The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - IngredientResponse: The response object containing the updated ingredient data.
    """
    service = IngredientService(session)
    ingredient = await service.update_batch(batch_id, request)
    return ingredient


@router.delete("/batch/{batch_id}", status_code=200)
async def delete_ingredient_batch(
    batch_id: str,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> Message:
    """
    # A route to delete a batch of ingredients.
    ## Args:
        - batch_id (str): The ID of the batch to be deleted.
        - _: UserResponse: The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - Message: A message indicating the result of the deletion.
    """
    service = IngredientService(session)
    response = await service.delete_batch(batch_id)
    return response
