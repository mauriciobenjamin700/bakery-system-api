from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.db.repositories.ingredient import IngredientRepository
from app.schemas.ingredient import (
    IngredientBatchRequest,
    IngredientBatchResponse,
    IngredientRequest,
    IngredientResponse,
)
from app.schemas.message import Message


class IngredientService:
    """
    Service class for managing ingredients.
    This class provides methods to add, update, delete, and retrieve ingredients
    and their batches from the database.
    It uses the IngredientRepository to interact with the database.
    Args:
        db_session (AsyncSession): The database session to be used for operations.

    Methods:
        add(request: IngredientRequest) -> IngredientResponse:
            Add a new ingredient to the database.
        get(ingredient_id: int) -> IngredientResponse:
            Get an ingredient by its ID.
        get_all() -> list[IngredientResponse]:
            Get all ingredients.
        update(ingredient_id: int, request: IngredientRequest) -> IngredientResponse:
            Update an ingredient by its ID.
        delete(ingredient_id: int) -> Message:
            Delete an ingredient by its ID.
        add_batch(request: IngredientBatchRequest) -> IngredientBatchResponse:
            Add a new batch of ingredients to the database.
        update_batch(batch_id: str, request: IngredientBatchRequest) -> IngredientBatchResponse:
            Update a batch of ingredients by its ID.
        delete_batch(batch_id: str) -> Message:
            Delete a batch of ingredients by its ID.

    """

    def __init__(self, db_session: AsyncSession) -> None:
        self.repository = IngredientRepository(db_session)

    async def add(
        self,
        request: IngredientRequest,
    ) -> IngredientResponse:
        """
        Add a new ingredient to the database.

        Args:
            ingredient (IngredientRequest): The ingredient to be added.

        Returns:
            IngredientResponse: The added ingredient.
        """

        model = self.repository.map_request_to_model(request)

        ingredient = await self.repository.add(model)

        batch = self.repository.create_ingredient_batch(
            ingredient.id,
            validity=request.validity,
            quantity=request.quantity,
        )

        batch = await self.repository.add_batch(batch)

        response = await self.repository.map_model_to_response(ingredient)

        return response

    async def get(
        self,
        ingredient_id: int,
    ) -> IngredientResponse:
        """
        Get an ingredient by its ID.

        Args:
            ingredient_id (int): The ID of the ingredient to retrieve.

        Returns:
            IngredientResponse: The retrieved ingredient.
        """

        ingredient = await self.repository.get(ingredient_id)

        if not ingredient:
            raise NotFoundError(
                "Ingredient not found",
            )

        response = await self.repository.map_model_to_response(ingredient)

        return response

    async def get_all(
        self,
    ) -> list[IngredientResponse]:
        """
        Get all ingredients.

        Returns:
            list[IngredientResponse]: A list of all ingredients.
        """

        ingredients = await self.repository.get(all=True)

        if not ingredients:
            raise NotFoundError(
                "No ingredients found",
            )

        response = await self.repository.map_model_to_response(ingredients)

        return response

    async def update(
        self,
        ingredient_id: int,
        request: IngredientRequest,
    ) -> IngredientResponse:
        """
        Update an ingredient by its ID.

        Args:
            ingredient_id (int): The ID of the ingredient to update.
            ingredient (IngredientRequest): The updated ingredient data.

        Returns:
            IngredientResponse: The updated ingredient.
        """

        ingredient = await self.repository.get(ingredient_id)

        if not ingredient:
            raise NotFoundError(
                "Ingredient not found",
            )

        for key, value in request.to_dict(
            exclude=["quantity", "validity"]
        ).items():
            if value is not None:
                setattr(ingredient, key, value)

        ingredient = await self.repository.update(ingredient)

        response = await self.repository.map_model_to_response(ingredient)

        return response

    async def delete(
        self,
        ingredient_id: int,
    ) -> Message:
        """
        Delete an ingredient by its ID.

        Args:
            ingredient_id (int): The ID of the ingredient to delete.

        Returns:
            IngredientResponse: The deleted ingredient.
        """

        await self.repository.delete(id=ingredient_id)

        return Message(
            detail="Ingredient deleted successfully",
        )

    async def add_batch(
        self,
        request: IngredientBatchRequest,
    ) -> IngredientBatchResponse:
        """
        Add a new batch of ingredients to the database.

        Args:
            ingredient_id (int): The ID of the ingredient to add a batch for.
            batch (IngredientBatchRequest): The batch to be added.

        Returns:
            IngredientBatchResponse: The added batch.
        """

        model = self.repository.map_batch_request_to_model(request)

        batch = await self.repository.add_batch(model)

        response: IngredientBatchResponse = (
            self.repository.map_batch_model_to_response(batch)
        )

        return response

    async def update_batch(
        self,
        bach_id: str,
        request: IngredientBatchRequest,
    ) -> IngredientBatchResponse:
        """
        Update a batch of ingredients by its ID.
        Args:
            bach_id (str): The ID of the batch to update.
            batch (IngredientBatchRequest): The updated batch data.
        Returns:
            IngredientBatchResponse: The updated batch.
        """
        batch = await self.repository.get_batch(bach_id)

        if not batch:
            raise NotFoundError(
                "Batch not found",
            )

        for key, value in request.to_dict(
            exclude=["quantity", "validity"]
        ).items():
            if value is not None:
                setattr(batch, key, value)

        batch = await self.repository.update_batch(batch)

        response = await self.repository.map_batch_model_to_response(batch)

        return response

    async def delete_batch(
        self,
        batch_id: str,
    ) -> Message:
        """
        Delete a batch of ingredients by its ID.

        Args:
            batch_id (str): The ID of the batch to delete.

        Returns:
            IngredientBatchResponse: The deleted batch.
        """

        await self.repository.delete_batch(id=batch_id)

        return Message(
            detail="Batch deleted successfully",
        )
