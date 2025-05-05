from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import BadRequestError, NotFoundError
from app.db.models import PortionModel, ProductBatchModel, ProductModel

class ProductRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


    async def add(self, model: ProductModel) -> ProductModel:
        """
        Add a new product to the database.

        Args:
            model (ProductModel): The product model to be added.

        Returns:
            ProductModel: The added product model.
        """
        self.db_session.add(model)
        await self.db_session.commit()
        await self.db_session.refresh(model)
        return model
    
    async def get(self, product_id: str | None = None) -> ProductModel | list[ProductModel] | None:
        """
        Get a product by its ID.

        Args:
            product_id (str): The ID of the product to retrieve.

        Returns:
            ProductModel: The retrieved product model.
        """

        if product_id:
        
            query = select(ProductModel).where(ProductModel.id == product_id)

            result = await self.db_session.execute(query)

            response = result.unique().scalar_one_or_none()

        else:
            query = select(ProductModel)
            result = await self.db_session.execute(query)
            response = result.unique().scalars().all()

        return response
    

    async def update(self, model: ProductModel) -> ProductModel:
        """
        Update an existing product in the database.

        Args:
            model (ProductModel): The product model to be updated.

        Returns:
            ProductModel: The updated product model.
        """
        await self.db_session.commit()
        await self.db_session.refresh(model)
        return model
    

    async def delete(
        self,
        model: ProductModel | None = None,
        product_id: str | None = None,
    ) -> None:
        """
        Delete a product from the database.

        Args:
            model (ProductModel | None): The product model to be deleted.
            product_id (str | None): The ID of the product to be deleted.

        Returns:
            None
        """
        if model is not None:
            await self.db_session.delete(model)
        elif product_id is not None:
            query = delete(ProductModel).where(ProductModel.id == product_id)
            result = await self.db_session.execute(query)
            if result.rowcount == 0:
                raise NotFoundError("Product not found")
        else:
            raise BadRequestError("Either model or product_id must be provided")
        
        await self.db_session.commit()


    async def add_portion(
        self,
        portion: PortionModel,
    ) -> PortionModel:
        """
        Add a portion to a product.

        Args:
            product (ProductModel): The product to which the portion will be added.
            portion (PortionModel): The portion to be added.

        Returns:
            PortionModel: The added portion model.
        """
        self.db_session.add(portion)
        await self.db_session.commit()
        await self.db_session.refresh(portion)
        return portion
    

    async def get_portion(
        self,
        portion_id: str | None = None,
        product_id: str | None = None,
        all_results: bool = False,
    ) -> PortionModel | list[PortionModel] | None:
        """
        Get a portion by its ID.

        Args:
            product_id (str): The ID of the product to retrieve.

        Returns:
            PortionModel: The retrieved portion model.
        """
        if portion_id:
            query = select(PortionModel).where(PortionModel.id == portion_id)
            result = await self.db_session.execute(query)
            
        elif product_id:
            query = select(PortionModel).where(PortionModel.id == product_id)
            result = await self.db_session.execute(query)
        else:
            query = select(PortionModel)
            result = await self.db_session.execute(query)

        if all_results:
            response = result.unique().scalars().all()
        else:
            response = result.unique().scalar_one_or_none()

        return response
    

    async def update_portion(
        self,
        portion: PortionModel,
    ) -> PortionModel:
        """
        Update an existing portion in the database.

        Args:
            portion (PortionModel): The portion model to be updated.

        Returns:
            PortionModel: The updated portion model.
        """
        await self.db_session.commit()
        await self.db_session.refresh(portion)
        return portion
    

    async def delete_portion(
        self,
        portion: PortionModel | None = None,
        portion_id: str | None = None,
    ) -> None:
        """
        Delete a portion from the database.

        Args:
            model (PortionModel | None): The portion model to be deleted.
            portion_id (str | None): The ID of the portion to be deleted.

        Returns:
            None
        """
        if portion is not None:
            await self.db_session.delete(portion)
        elif portion_id is not None:
            query = delete(PortionModel).where(PortionModel.id == portion_id)
            result = await self.db_session.execute(query)
            if result.rowcount == 0:
                raise NotFoundError("Portion not found")
        else:
            raise BadRequestError("Either model or portion_id must be provided")
        
        await self.db_session.commit()


    async def add_product_batch(
        self,
        product_batch: ProductBatchModel,
    ) -> ProductBatchModel:
        """
        Add a product batch to a product.

        Args:
            product (ProductModel): The product to which the batch will be added.
            product_batch (ProductBatchModel): The batch to be added.

        Returns:
            ProductBatchModel: The added batch model.
        """
        self.db_session.add(product_batch)
        await self.db_session.commit()
        await self.db_session.refresh(product_batch)
        return product_batch


    async def get_product_batch(
        self,
        product_batch_id: str | None = None,
        product_id: str | None = None,
        all_results: bool = False,
    ) -> ProductBatchModel | list[ProductBatchModel] | None:
        """
        Get a product batch by its ID.

        Args:
            product_batch_id (str): The ID of the product batch to retrieve.

        Returns:
            ProductBatchModel: The retrieved product batch model.
        """
        if product_batch_id:
            query = select(ProductBatchModel).where(ProductBatchModel.id == product_batch_id)
            result = await self.db_session.execute(query)
            
        elif product_id:
            query = select(ProductBatchModel).where(ProductBatchModel.product_id == product_id)
            result = await self.db_session.execute(query)
        else:
            query = select(ProductBatchModel)
            result = await self.db_session.execute(query)

        if all_results:
            response = result.unique().scalars().all()
        else:
            response = result.unique().scalar_one_or_none()

        return response


    async def update_product_batch(
        self,
        product_batch: ProductBatchModel,
    ) -> ProductBatchModel:
        """
        Update an existing product batch in the database.

        Args:
            product_batch (ProductBatchModel): The product batch model to be updated.

        Returns:
            ProductBatchModel: The updated product batch model.
        """
        await self.db_session.commit()
        await self.db_session.refresh(product_batch)
        return product_batch
    

    async def delete_product_batch(
        self,
        product_batch: ProductBatchModel | None = None,
        product_batch_id: str | None = None,
    ) -> None:
        """
        Delete a product batch from the database.

        Args:
            model (ProductBatchModel | None): The product batch model to be deleted.
            product_batch_id (str | None): The ID of the product batch to be deleted.

        Returns:
            None
        """
        if product_batch is not None:
            await self.db_session.delete(product_batch)
        elif product_batch_id is not None:
            query = delete(ProductBatchModel).where(ProductBatchModel.id == product_batch_id)
            result = await self.db_session.execute(query)
            if result.rowcount == 0:
                raise NotFoundError("Product batch not found")
        else:
            raise BadRequestError("Either model or product_batch_id must be provided")
        
        await self.db_session.commit()