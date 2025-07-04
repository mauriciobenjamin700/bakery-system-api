from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import messages
from app.core.errors import BadRequestError, NotFoundError
from app.db.models import ProductBatchModel, ProductModel, SaleModel, UserModel
from app.schemas import SaleRequest, SaleResponse


class SaleRepository:
    """
    Repository class for handling Sale operations.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add(self, model: SaleModel | list[SaleModel]) -> SaleModel:
        """
        Async method to add a SaleModel to the database.
        """

        async def local_add(model: SaleModel) -> None:
            """
            Local function to add a SaleModel to the database.
            """

            query = select(ProductModel).where(
                ProductModel.id == model.product_id
            )

            result = await self.db_session.execute(query)

            product = result.unique().scalars().first()

            if not product:
                raise NotFoundError(messages.ERROR_DATABASE_PRODUCT_NOT_FOUND)

            query = select(UserModel).where(UserModel.id == model.user_id)

            result = await self.db_session.execute(query)

            user = result.unique().scalar_one_or_none()

            if not user:
                raise NotFoundError(messages.ERROR_DATABASE_USER_NOT_FOUND)

            query = (
                select(ProductBatchModel)
                .where(ProductBatchModel.product_id == model.product_id)
                .order_by(ProductBatchModel.validity.asc())
            )

            result = await self.db_session.execute(query)

            batches = result.unique().scalars().all()

            if not batches:
                raise NotFoundError(
                    messages.ERROR_DATABASE_PRODUCT_BATCH_NOT_FOUND
                )

            quantity = sum([batch.quantity for batch in batches])

            if quantity < model.quantity:
                raise NotFoundError(messages.ERROR_NOT_ENOUGH_PRODUCT_IN_STOCK)

            products_sold = model.quantity

            # AQUI ESTÁ A CORREÇÃO PRINCIPAL: NÃO DELETAR, APENAS ATUALIZAR
            for batch in batches:
                if products_sold <= 0: # Se já vendemos o suficiente, para de processar lotes
                    break

                if batch.quantity > products_sold:
                    batch.quantity -= products_sold
                    # Não precisamos de self.db_session.add(batch) aqui, pois o batch
                    # já está "attached" à sessão se veio de uma query.
                    # As alterações serão detectadas no commit.
                    products_sold = 0 # Zerar o que precisa vender
                else:
                    products_sold -= batch.quantity
                    batch.quantity = 0 # <-- CORRIGIDO: Define a quantidade para 0
                    # self.db_session.add(batch) # Não é estritamente necessário aqui se o batch já está attached
            
            # Força o SQLAlchemy a ver que esses objetos 'batch' foram modificados
            # Mesmo que eles já estejam "attached", adicionar garante que as mudanças sejam rastreadas.
            self.db_session.add_all(batches) # Adiciona todos os lotes de volta para a sessão rastrear as mudanças

            self.db_session.add(model) # Adiciona o registro da venda

        if isinstance(model, list): # `type(model) is list` é mais robusto em Python
            for item in model:
                await local_add(item)
            model = model[0]
        else:
            await local_add(model)

        await self.db_session.commit() # Comita todas as mudanças (lotes e vendas)

        await self.db_session.refresh(model)

        return model
    async def get(
        self,
        id: str | None = None,
        user_id: str | None = None,
        product_id: str | None = None,
        sale_code: str | None = None,
        all_results: bool = False,
    ) -> SaleModel | Sequence[SaleModel] | None:
        """
        Async method to get SaleModel(s) from the database.

        Args:
            id (str | None): The ID of the SaleModel to retrieve.
            user_id (str | None): The user ID associated with the SaleModel.
            product_id (str | None): The product ID associated with the SaleModel.
            all_results (bool): Flag to indicate if all results should be returned.

        Returns:
            SaleModel | list[SaleModel] | None: The retrieved model(s) or None.
        """

        query = select(SaleModel)

        if id:
            query = query.where(SaleModel.id == id).order_by(
                SaleModel.created_at.desc()
            )

        elif user_id:
            query = query.where(SaleModel.user_id == user_id).order_by(
                SaleModel.created_at.desc()
            )

        elif product_id:
            query = query.where(SaleModel.product_id == product_id).order_by(
                SaleModel.created_at.desc()
            )
        elif sale_code:
            query = query.where(SaleModel.sale_code == sale_code).order_by(
                SaleModel.created_at.desc()
            )

        result = await self.db_session.execute(query)

        if all_results:
            return result.scalars().all()

        return result.unique().scalar_one_or_none()

    async def update(self, model: SaleModel) -> SaleModel:
        """
        Async method to update a SaleModel in the database.

        Args:
            model (SaleModel): The model object to update.

        Returns:
            SaleModel: The updated model object.
        """

        await self.db_session.commit()
        await self.db_session.refresh(model)

        return model

    async def delete(
        self,
        id: str | None = None,
        model: SaleModel | None = None,
    ) -> bool:
        """
        Async method to delete a SaleModel from the database.

        Args:
            id (str | None): The ID of the SaleModel to delete.
            model (SaleModel | None): The model object to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """

        if not id and not model:
            raise BadRequestError("ID or model must be provided")

        if model:
            query = delete(SaleModel).where(SaleModel.id == model.id)
        else:
            query = delete(SaleModel).where(SaleModel.id == id)

        result = await self.db_session.execute(query)

        await self.db_session.commit()

        return result.rowcount > 0

    async def get_sale_note_data(
        self, sale_code: str
    ) -> tuple[UserModel, Sequence[ProductModel], Sequence[SaleModel]] | None:
        """
        Get a sale note for a given sale code.
        Args:
            sale_code (str): The sale code to retrieve the note for.
        Returns:
            tuple: A tuple containing the products, user, and total value of the sale.
        """

        result = await self.get(sale_code=sale_code, all_results=True)

        if not result:
            return None

        if isinstance(result, list) or isinstance(result, Sequence):
            sales: list[SaleModel] = list(result)
        else:
            sales: list[SaleModel] = [result]

        product_ids = [model.product_id for model in sales]
        user_id = sales[0].user_id

        query = select(ProductModel).where(ProductModel.id.in_(product_ids))

        result = await self.db_session.execute(query)

        products = result.unique().scalars().all()

        query = select(UserModel).where(UserModel.id == user_id)

        result = await self.db_session.execute(query)

        employee = result.unique().scalar_one_or_none()

        if employee is None:
            return None

        return employee, products, sales

    async def map_request_to_model(
        self, request: SaleRequest, sale_code: str
    ) -> SaleModel:
        """
        Async method to map a SaleRequest to a SaleModel.

        Args:
            request (SaleRequest): The request object to map.

        Returns:
            SaleModel: The mapped model object.
        """

        query = select(ProductModel).where(
            ProductModel.id == request.product_id
        )

        result = await self.db_session.execute(query)

        product = result.unique().scalars().first()

        if not product:
            raise NotFoundError(messages.ERROR_DATABASE_PRODUCT_NOT_FOUND)

        value = product.price_sale * request.quantity

        return SaleModel(
            **request.to_dict(include={"value": value, "sale_code": sale_code})
        )

    def map_model_to_response(self, model: SaleModel) -> SaleResponse:
        """
        method to map a SaleModel to a SaleResponse.

        Args:
            model (SaleModel): The model object to map.

        Returns:
            SaleResponse: The mapped response object.
        """

        return SaleResponse(
            **model.to_dict(),
        )
