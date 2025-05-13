from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.db import get_session
from app.api.dependencies.permissions import employer_permission
from app.schemas.ingredient import (
    IngredientBatchRequest,
    IngredientRequest,
    IngredientResponse,
)
from app.schemas.message import Message
from app.schemas.user import UserResponse
from app.services.ingredient import IngredientService

router = APIRouter(prefix="/ingredient", tags=["Ingredient"])


@router.post("/", status_code=201)
async def add_ingredient(
    request: IngredientRequest,
    _: UserResponse = Depends(employer_permission),
    session: AsyncSession = Depends(get_session),
) -> IngredientResponse:
    """
    # A route to add an ingredient.

    ## Args:
        - request (IngredientRequest): The request object containing ingredient data.
        - _ (UserResponse): The user making the request.
        - session (AsyncSession): The database session.
    ## Returns:
        - IngredientResponse: The response object containing the added ingredient data.
    """
    service = IngredientService(session)
    ingredient = await service.add(request)
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
        ingredients = await service.get(ingredient_id)
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
