from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError, ValidationError
from app.db.models import ProductBatchModel, ProductModel, SaleModel, UserModel
from app.schemas import SaleRequest, SaleResponse


class SaleRepository:
    """
    Repository class for handling Sale operations.

    Methods:
        add(model: SaleModel) -> SaleModel:
            Adds a SaleModel to the database.

        get(id: str | None = None, user_id: str | None = None, product_id: str | None = None, all_results: bool = False) -> SaleModel | list[SaleModel] | None:
            Retrieves SaleModel(s) from the database.

        update(model: SaleModel) -> SaleModel:
            Updates a SaleModel in the database.

        delete(id: str | None = None, model: SaleModel | None = None) -> bool:
            Deletes a SaleModel from the database.

        get_sale_note_data(sale_code: str) -> tuple[UserModel, list[ProductModel], list[SaleModel]] | None:
            Retrieves sale note data for a given sale code.

        map_request_to_model(request: SaleRequest, sale_code: str) -> SaleModel:
            Maps a SaleRequest to a SaleModel.

        map_model_to_response(model: SaleModel) -> SaleResponse:
            Maps a SaleModel to a SaleResponse.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add(self, model: SaleModel) -> SaleModel:
        """
        Async method to add a SaleModel to the database.

        Args:
            model (SaleModel): The model object to add.

        Returns:
            SaleModel: The added model object.
        """

        query = select(ProductModel).where(ProductModel.id == model.product_id)

        result = await self.db_session.execute(query)

        product = result.unique().scalars().first()

        if not product:
            raise NotFoundError("Product not found")

        query = (
            select(ProductBatchModel)
            .where(ProductBatchModel.product_id == model.product_id)
            .order_by(ProductBatchModel.validity.asc())
        )

        result = await self.db_session.execute(query)

        batches = result.unique().scalars().all()

        if not batches:
            raise NotFoundError("Product batch not found")

        quantity = sum([batch.quantity for batch in batches])

        if quantity < model.quantity:
            raise NotFoundError("Not enough product in stock")

        query = select(UserModel).where(UserModel.id == model.user_id)

        result = await self.db_session.execute(query)

        user = result.unique().scalar_one_or_none()

        if not user:

            raise NotFoundError("User not found")

        products_sold = model.quantity

        for batch in batches:
            if batch.quantity >= products_sold:
                batch.quantity -= products_sold
                break
            else:
                products_sold -= batch.quantity
                await self.db_session.delete(batch)

        self.db_session.add(model)

        await self.db_session.commit()
        await self.db_session.refresh(model)

        return model

    async def get(
        self,
        id: str | None = None,
        user_id: str | None = None,
        product_id: str | None = None,
        sale_code: str | None = None,
        all_results: bool = False,
    ) -> SaleModel | list[SaleModel] | None:
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
            raise ValidationError("ID or model must be provided")

        if model:
            query = delete(SaleModel).where(SaleModel.id == model.id)
        else:
            query = delete(SaleModel).where(SaleModel.id == id)

        result = await self.db_session.execute(query)

        await self.db_session.commit()

        return result.rowcount > 0

    async def get_sale_note_data(
        self, sale_code: str
    ) -> tuple[UserModel, list[ProductModel], list[SaleModel]] | None:
        """
        Get a sale note for a given sale code.
        Args:
            sale_code (str): The sale code to retrieve the note for.
        Returns:
            tuple: A tuple containing the products, user, and total value of the sale.
        """

        sales: list[SaleModel] = await self.get(
            sale_code=sale_code, all_results=True
        )

        if not sales:
            return None

        product_ids = [model.product_id for model in sales]
        user_id = sales[0].user_id

        query = select(ProductModel).where(ProductModel.id.in_(product_ids))

        result = await self.db_session.execute(query)

        products = result.unique().scalars().all()

        query = select(UserModel).where(UserModel.id == user_id)

        result = await self.db_session.execute(query)

        client = result.unique().scalar_one_or_none()

        return client, products, sales

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
            raise NotFoundError("Product not found")

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
            model.to_dict(),
        )
