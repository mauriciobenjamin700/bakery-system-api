from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import messages
from app.core.errors import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    ServerError,
)
from app.core.generate.ids import id_generator
from app.db.models import (
    IngredientModel,
    PortionModel,
    ProductBatchModel,
    ProductModel,
)
from app.schemas.product import (
    PortionResponse,
    ProductBatchRequest,
    ProductBatchResponse,
    ProductRequest,
    ProductResponse,
    RecipeRequest,
)


class ProductRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add(self, model: ProductModel) -> ProductModel:
        try:
            stmt = select(ProductModel).where(
                ProductModel.name == model.name,
                ProductModel.price_cost == model.price_cost,
                ProductModel.price_sale == model.price_sale,
                ProductModel.measure == model.measure,
                ProductModel.image_path == model.image_path,
                ProductModel.description == model.description,
                ProductModel.mark == model.mark,
                ProductModel.min_quantity == model.min_quantity,
            )

            result = await self.db_session.execute(stmt)
            existing_product = result.unique().scalar_one_or_none()

            if existing_product:
                raise ConflictError(messages.ERROR_DATABASE_PRODUCT_ALREADY_EXISTS)

            self.db_session.add(model)
            await self.db_session.commit()
            await self.db_session.refresh(model)
            return model

        except ConflictError:
            await self.db_session.rollback()
            raise
        except Exception as e:
            await self.db_session.rollback()
            raise ServerError(e)

    async def get(self, product_id: str | None = None) -> ProductModel | Sequence[ProductModel] | None:
        if product_id:
            query = select(ProductModel).where(ProductModel.id == product_id)
            result = await self.db_session.execute(query)
            response = result.unique().scalar_one_or_none()
        else:
            query = select(ProductModel)
            result = await self.db_session.execute(query)
            response = result.unique().scalars().all() or None
        return response

    async def update(self, model: ProductModel) -> ProductModel:
        try:
            await self.db_session.commit()
            await self.db_session.refresh(model)
            return model
        except Exception:
            await self.db_session.rollback()
            raise

    async def delete(self, model: ProductModel | None = None, product_id: str | None = None) -> None:
        try:
            if model is not None:
                await self.db_session.delete(model)
            elif product_id is not None:
                query = delete(ProductModel).where(ProductModel.id == product_id)
                result = await self.db_session.execute(query)
                if result.rowcount == 0:
                    raise NotFoundError(messages.ERROR_DATABASE_PRODUCT_NOT_FOUND)
            else:
                raise BadRequestError("Either model or product_id must be provided")
            await self.db_session.commit()
        except Exception:
            await self.db_session.rollback()
            raise

    async def add_portion(self, portion: PortionModel | list[PortionModel]) -> PortionModel | None:
        try:
            if isinstance(portion, list):
                self.db_session.add_all(portion)
                await self.db_session.commit()
            else:
                self.db_session.add(portion)
                await self.db_session.commit()
                await self.db_session.refresh(portion)
                return portion
        except Exception:
            await self.db_session.rollback()
            raise

    async def get_portion(self, portion_id: str | None = None, product_id: str | None = None, all_results: bool = False) -> PortionModel | Sequence[PortionModel] | None:
        if portion_id:
            query = select(PortionModel).where(PortionModel.id == portion_id)
        elif product_id:
            query = select(PortionModel).where(PortionModel.product_id == product_id)
        else:
            query = select(PortionModel)
        result = await self.db_session.execute(query)
        return result.unique().scalars().all() if all_results else result.unique().scalar_one_or_none()

    async def update_portion(self, portion: PortionModel) -> PortionModel:
        try:
            await self.db_session.commit()
            await self.db_session.refresh(portion)
            return portion
        except Exception:
            await self.db_session.rollback()
            raise

    async def delete_portion(self, portion: PortionModel | None = None, portion_id: str | None = None) -> None:
        try:
            if portion is not None:
                await self.db_session.delete(portion)
            elif portion_id is not None:
                query = delete(PortionModel).where(PortionModel.id == portion_id)
                result = await self.db_session.execute(query)
                if result.rowcount == 0:
                    raise NotFoundError(messages.ERROR_PORTION_NOT_FOUND)
            else:
                raise BadRequestError("Either model or portion_id must be provided")
            await self.db_session.commit()
        except Exception:
            await self.db_session.rollback()
            raise

    async def add_product_batch(self, product_batch: ProductBatchModel) -> ProductBatchModel:
        try:
            self.db_session.add(product_batch)
            await self.db_session.commit()
            await self.db_session.refresh(product_batch)
            return product_batch
        except Exception:
            await self.db_session.rollback()
            raise

    async def get_product_batch(self, product_batch_id: str | None = None, product_id: str | None = None, all_results: bool = False) -> ProductBatchModel | Sequence[ProductBatchModel] | None:
        if product_batch_id:
            query = select(ProductBatchModel).where(ProductBatchModel.id == product_batch_id)
        elif product_id:
            query = select(ProductBatchModel).where(ProductBatchModel.product_id == product_id)
        else:
            query = select(ProductBatchModel)

        result = await self.db_session.execute(query)
        return result.unique().scalars().all() if all_results else result.unique().scalar_one_or_none()

    async def update_product_batch(
        self,
        product_batch: ProductBatchModel,
    ) -> ProductBatchModel:
        """
        Update an existing product batch in the database.
        """
        # DEBUG PRINTS ADICIONADOS AQUI
        print(f"DEBUG REPO: Recebido lote {product_batch.id} para persistir. Qtd: {product_batch.quantity}. Validade: {product_batch.validity}") # <-- ADICIONAR
        
        # CORREÇÃO: Garante que a sessão rastreie as mudanças no objeto
        self.db_session.add(product_batch) # <-- ESSA LINHA É A CORREÇÃO MAIS PROVÁVEL PARA PERSISTÊNCIA
        
        try:
            await self.db_session.commit()
            # DEBUG PRINTS ADICIONADOS AQUI
            print(f"DEBUG REPO: Commit concluído para lote {product_batch.id}.") 
        except Exception as e:
            # DEBUG PRINTS ADICIONADOS AQUI
            print(f"DEBUG REPO: Erro no commit para lote {product_batch.id}: {e}") 
            await self.db_session.rollback() # Garante rollback em caso de erro
            raise ServerError(f"Falha ao atualizar lote no DB: {e}") 
        
        await self.db_session.refresh(product_batch)
        # DEBUG PRINTS ADICIONADOS AQUI
        print(f"DEBUG REPO: Lote {product_batch.id} atualizado e refrescado. Qtd após refresh: {product_batch.quantity}") # <-- ADICIONAR
        return product_batch

    async def delete_product_batch(self, product_batch: ProductBatchModel | None = None, product_batch_id: str | None = None) -> None:
        try:
            if product_batch is not None:
                await self.db_session.delete(product_batch)
            elif product_batch_id is not None:
                query = delete(ProductBatchModel).where(ProductBatchModel.id == product_batch_id)
                result = await self.db_session.execute(query)
                if result.rowcount == 0:
                    raise NotFoundError(messages.ERROR_DATABASE_PRODUCT_BATCH_NOT_FOUND)
            else:
                raise BadRequestError("Either model or product_batch_id must be provided")
            await self.db_session.commit()
        except Exception:
            await self.db_session.rollback()
            raise

    @staticmethod
    def map_product_request_to_model(request: ProductRequest, image_path: str) -> tuple[ProductModel, list[PortionModel], ProductBatchModel]:
        product = ProductModel(**request.to_dict(
            exclude=["recipe", "quantity", "validity"],
            include={"id": id_generator(), "image_path": image_path},
        ))

        portions = [
            PortionModel(**portion.to_dict(include={"id": id_generator(), "product_id": product.id}))
            for portion in request.recipe
        ] if request.recipe else []

        batch = ProductBatchModel(
            id=id_generator(),
            product_id=product.id,
            validity=request.validity,
            quantity=request.quantity,
        )

        return product, portions, batch

    @staticmethod
    def map_product_batch_request_to_model(request: ProductBatchRequest) -> ProductBatchModel:
        return ProductBatchModel(**request.to_dict())

    @staticmethod
    def map_recipe_request_to_models(request: RecipeRequest) -> list[PortionModel]:
        return [
            PortionModel(
                ingredient_id=portion.ingredient_id,
                product_id=request.product_id,
                quantity=portion.quantity,
            )
            for portion in request.recipe
        ]

    async def map_product_model_to_response(self, model: ProductModel) -> ProductResponse:
        batch_models_result = await self.get_product_batch(product_id=model.id, all_results=True)
        batch_models = (
            [batch_models_result]
            if isinstance(batch_models_result, ProductBatchModel)
            else batch_models_result or []
        )

        quantity = sum(batch.quantity for batch in batch_models)
        batches = [ProductBatchResponse(**batch.to_dict()) for batch in batch_models] if batch_models else None

        portions = await self.get_portion(product_id=model.id, all_results=True)
        recipe = []

        if portions:
            for portion in portions:
                stmt = select(IngredientModel).where(IngredientModel.id == portion.ingredient_id)
                result = await self.db_session.execute(stmt)
                ingredient = result.unique().scalar_one_or_none()

                if not ingredient:
                    raise NotFoundError(messages.ERROR_DATABASE_INGREDIENT_NOT_FOUND)

                recipe.append(
                    PortionResponse(
                        **portion.to_dict(
                            include={
                                "ingredient_id": portion.ingredient_id,
                                "ingredient_name": ingredient.name,
                                "ingredient_measure": ingredient.measure,
                                "ingredient_quantity": portion.quantity,
                            }
                        )
                    )
                )

        return ProductResponse(
            **model.to_dict(
                include={
                    "quantity": quantity,
                    "recipe": recipe if recipe else None,
                    "batches": batches if batches else None,
                }
            )
        )

    @staticmethod
    def map_product_batch_request_to_model(
        request: ProductBatchRequest,
    ) -> ProductBatchModel:
        """
        Map a product batch request to a product batch model.

        Args:
            request (ProductBatchRequest): The product batch request to be mapped.

        Returns:
            ProductBatchModel: The mapped product batch model.
        """
        return ProductBatchModel(**request.to_dict())

    @staticmethod
    def map_recipe_request_to_models(
        request: RecipeRequest,
    ) -> list[PortionModel]:
        """
        Map a recipe request to a list of portion models.

        Args:
            request (list[RecipeRequest]): The recipe request to be mapped.

        Returns:
            list[PortionModel]: The mapped list of portion models.
        """
        portions = []

        for portion in request.recipe:
            portions.append(
                PortionModel(
                    ingredient_id=portion.ingredient_id,
                    product_id=request.product_id,
                    quantity=portion.quantity,
                )
            )

        return portions
