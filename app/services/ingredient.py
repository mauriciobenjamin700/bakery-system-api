"""
Esse pacote contem todos as funções do objeto Ingredient

classes:
    IngredientService

"""

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import IngredientModel, LoteIngredientModel
from app.db.repositories.ingredient import IngredientRepository
from app.schemas.ingredient import (
    IngredientRequest,
    IngredientResponse,
    LoteIngredientRequest,
    LoteIngredientResponse,
)


class IngredientService:

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
        