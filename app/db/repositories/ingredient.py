from datetime import date
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import BadRequestError, UnprocessableEntityError
from app.db.models import IngredientModel, IngredientBatchModel
from app.schemas.ingredient import IngredientBatchResponse, IngredientRequest, IngredientResponse


class IngredientRepository:
    """
    Ingredient Repository Class to handle all database operations related to Ingredient

    - Attributes:
        - db_session: AsyncSession

    - Methods:
        - add: Add a new Ingredient to the database
        - get: Get an Ingredient from the database
        - update: Update an Ingredient in the database
        - delete: Delete an Ingredient from the database
    """

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
    
    async def add(self, model: IngredientModel) -> IngredientModel:
        """
        Add a new Ingredient to the database

        Args:
            model (IngredientModel): The Ingredient model to be added to the database

        Returns:
            IngredientModel: The added Ingredient model
        """

        try:
            self.db_session.add(model)
            await self.db_session.commit()
            await self.db_session.refresh(model)
            return model

        except Exception as e:
            await self.db_session.rollback()
            raise BadRequestError(str(e))
        
    
    async def get(
        self, 
        id: str = None, 
        name: str = None, 
        all_results=False
    ) -> None | IngredientModel | list[IngredientModel]:
        """
        Get an Ingredient from the database by id or name. If all_results is True, return all results found in the database.

        Args:
            id (str, optional): The id of the Ingredient to be retrieved. Defaults to None.
            name (str, optional): The name of the Ingredient to be retrieved. Defaults to None.
            all_results (bool, optional): If True, return all results found in the database. Defaults to False.
        Returns:
            None | IngredientModel | list[IngredientModel]: The retrieved Ingredient model or list of Ingredient models
        """
        if all_results:
            if name:
                result = await self.db_session.execute(
                    select(IngredientModel)
                    .where(IngredientModel.name == name)
                )
                return result.unique().scalars().all
            result = await self.db_session.execute(select(IngredientModel))
            return result.unique().scalars().all()

        if id:
            result = await self.db_session.execute(
                select(IngredientModel)
                .where(IngredientModel.id == id)
            )
            
            return result.unique().scalars().one_or_none()

        if name:
            result = await self.db_session.execute(
                select(IngredientModel)
                .where(IngredientModel.name == name)
            )
            
            return result.unique().scalars().one_or_none()

        return None
    
    async def update(self, model: IngredientModel) -> IngredientModel:
        """
        Update an Ingredient in the database

        Args:
            model (IngredientModel): The Ingredient model to be updated in the database

        Returns:
            IngredientModel: The updated Ingredient model
        """
        await self.db_session.commit()
        await self.db_session.refresh(model)
        return model
    
    
    async def delete(self, model: IngredientModel = None, id: str = None) -> None:
        """
        Delete an Ingredient from the database. If model is provided, delete the model. If id is provided, delete the model with the id.

        Args:
            model (IngredientModel, optional): The Ingredient model to be deleted. Defaults to None.
            id (str, optional): The id of the Ingredient model to be deleted. Defaults to None.

        Returns:
            None
        """
        if model:
            await self.db_session.delete(model)
            await self.db_session.commit()
        elif id:
            stmt = delete(IngredientModel).where(IngredientModel.id == id)
            result = await self.db_session.execute(stmt)
            await self.db_session.commit()
            
            if result.rowcount == 0:
                raise ConflictError("Ingredient not found")
        else:
            raise UnprocessableEntityError("Ingredient not found")
    
        return None
    
    
    async def add_batch(
        self, 
        model: IngredientBatchModel
    ) -> IngredientBatchModel:
        """
        Add a new IngredientBatch to the database

        Args:
            model (IngredientBatchModel): The IngredientBatch model to be added to the database

        Returns:
            IngredientBatchModel: The added IngredientBatch model
        """
        try:
            self.db_session.add(model)
            await self.db_session.commit()
            await self.db_session.refresh(model)
            return model

        except Exception as e:
            await self.db_session.rollback()
            raise BadRequestError(str(e))
        
        
    async def get_batch(
        self, 
        id: str = None, 
        ingredient_id: str = None, 
        all_results=False
    ) -> None | IngredientBatchModel | list[IngredientBatchModel]:
        """
        Get an IngredientBatch from the database by id or ingredient_id. If all_results is True, return all results found in the database.

        Args:
            id (str, optional): The id of the IngredientBatch to be retrieved. Defaults to None.
            ingredient_id (str, optional): The ingredient_id of the IngredientBatch to be retrieved. Defaults to None.
            all_results (bool, optional): If True, return all results found in the database. Defaults to False.

        Returns:
            None | IngredientBatchModel | list[IngredientBatchModel]: The retrieved IngredientBatch model or list of IngredientBatch models
        """
        if all_results:
            if ingredient_id:
                result = await self.db_session.execute(
                    select(IngredientBatchModel)
                    .where(IngredientBatchModel.ingredient_id == ingredient_id)
                )
                return result.unique().scalars().all()
            result = await self.db_session.execute(select(IngredientBatchModel))
            return result.unique().scalars().all()

        if id:
            result = await self.db_session.execute(
                select(IngredientBatchModel)
                .where(IngredientBatchModel.id == id)
            )
            
            return result.unique().scalars().one_or_none()

        if ingredient_id:
            result = await self.db_session.execute(
                select(IngredientBatchModel)
                .where(IngredientBatchModel.ingredient_id == ingredient_id)
            )
            
            return result.unique().scalars().one_or_none()

        return None
    
    async def update_batch(
        self, 
        model: IngredientBatchModel
    ) -> IngredientBatchModel:
        """
        Update an IngredientBatch in the database

        Args:
            model (IngredientBatchModel): The IngredientBatch model to be updated in the database

        Returns:
            IngredientBatchModel: The updated IngredientBatch model
        """
        await self.db_session.commit()
        await self.db_session.refresh(model)
        return model
    
    async def delete_batch(
        self, 
        model: IngredientBatchModel = None, 
        id: str = None
    ) -> None:
        """
        Delete an IngredientBatch from the database. If model is provided, delete the model. If id is provided, delete the model with the id.

        Args:
            model (IngredientBatchModel, optional): The IngredientBatch model to be deleted. Defaults to None.
            id (str, optional): The id of the IngredientBatch model to be deleted. Defaults to None.

        Returns:
            None
        """
        if model:
            await self.db_session.delete(model)
            await self.db_session.commit()
        elif id:
            stmt = delete(IngredientBatchModel).where(IngredientBatchModel.id == id)
            result = await self.db_session.execute(stmt)
            await self.db_session.commit()
            
            if result.rowcount == 0:
                raise ConflictError("IngredientBatch not found")
        else:
            raise UnprocessableEntityError("IngredientBatch not found")
    
        return None
    
    
    @staticmethod
    def map_request_to_model(request: IngredientRequest, image_path: str) -> IngredientModel:
        
        model = IngredientModel(
            **request.to_dict(),
            image_path=image_path
        )
        
        return model
    
    async def map_model_to_response(self, model: IngredientModel) -> IngredientResponse:
        """
        Async method to map a model to a response
        
        Args:
            model (IngredientModel): The model to be mapped
        Returns:
            IngredientResponse: The mapped response
        """
        
        batches = model.ingredients_batch
        
        quantity = 0
        
        batches_response = []
        
        for batch in batches:
            quantity += batch.quantity
            batches_response.append(
                self.map_batch_model_to_response(batch)
            )
        
        response = IngredientResponse(
            **model.to_dict(),
            quantity=quantity,
            batches=batches_response
        )
        
        return response
        
    @staticmethod
    def create_ingredient_batch(
        ingredient_id: str,
        validity: date,
        quantity: float
    ) -> IngredientBatchModel:
        """
        A static method to build a IngredientBatch model by passing the ingredient_id, validity and quantity

        Args:
            ingredient_id (str): The id of the ingredient
            validity (date): The validity date of the ingredient batch
            quantity (float): The quantity of the ingredient batch

        Returns:
            IngredientBatchModel: The mapped IngredientBatch model
        """
        return IngredientBatchModel(
            ingredient_id=ingredient_id,
            validity=validity,
            quantity=quantity
        )
    
    
    @staticmethod
    def map_batch_model_to_response(
        model: IngredientBatchModel
    ) -> IngredientBatchResponse:
        """
        Map a batch model to a response

        Args:
            model (IngredientBatchModel): The model to be mapped

        Returns:
            IngredientBatchModel: The mapped response
        """
        return IngredientBatchModel(
            **model.to_dict()
        )