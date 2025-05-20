from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.db.repositories import ProductRepository
from app.schemas.message import Message
from app.schemas.product import (
    ProductBatchRequest,
    ProductBatchUpdate,
    ProductRequest,
    ProductResponse,
    ProductUpdate,
    RecipeRequest,
)


class ProductService:
    """
    Class for managing product-related operations.

    Methods:
        add_product(request: ProductRequest) -> ProductResponse:
            Add a new product to the database.

        get_product_by_id(product_id: str) -> ProductResponse:
            Get a product by its ID.

        get_all_products() -> list[ProductResponse]:
            Get all products from the database.

        update_product(product_id: str, request: ProductUpdate) -> ProductResponse:
            Update a product in the database.

        delete_product(product_id: str) -> None:
            Delete a product from the database.

        add_product_batch(request: ProductBatchRequest) -> ProductResponse:
            Add a batch of products to the database.

        update_product_batch(product_batch_id: str, request: ProductBatchUpdate) -> ProductResponse:
            Update a batch of products in the database.

        delete_product_batch(product_batch_id: str) -> Message:
            Delete a batch of products from the database.

        add_recipe(request: RecipeRequest) -> ProductResponse:
            Add a recipe to a product in the database.

        update_recipe(portion_id: str, new_quantity: float) -> ProductResponse:
            Update a recipe in the database.

        delete_recipe(portion_id: str) -> Message:
            Delete a recipe from the database.
    """

    def __init__(self, session: AsyncSession):
        self.repository = ProductRepository(session)

    async def add(self, request: ProductRequest) -> ProductResponse:
        """
        Add a new product to the database.

        Args:
            request (ProductRequest): The product request object containing product details.

        Returns:
            ProductResponse: The response object containing the added product details.
        """

        product_model, portion_models, batch_model = (
            self.repository.map_product_request_to_model(request)
        )

        product_model = await self.repository.add(product_model)

        await self.repository.add_product_batch(batch_model)

        if portion_models:
            for portion_model in portion_models:
                await self.repository.add_portion(portion_model)

        response = await self.repository.map_product_model_to_response(
            product_model
        )

        return response

    async def get_by_id(self, product_id: str) -> ProductResponse:
        """
        Get a product by its ID.

        Args:
            product_id (str): The ID of the product to retrieve.

        Returns:
            ProductResponse: The response object containing the product details.
        """

        product_model = await self.repository.get(product_id=product_id)

        if not product_model:

            raise NotFoundError(f"Product with ID {product_id} not found.")

        response = await self.repository.map_product_model_to_response(
            product_model  # type: ignore
        )

        return response

    async def get_all(self) -> list[ProductResponse]:
        """
        Get all products from the database.

        Returns:
            list[ProductResponse]: A list of response objects containing product details.
        """

        product_models = await self.repository.get()

        if not product_models:
            raise NotFoundError("No products found.")

        response = []

        for model in product_models:  # type: ignore
            result = await self.repository.map_product_model_to_response(model)
            response.append(result)

        return response

    async def update(
        self, product_id: str, request: ProductUpdate
    ) -> ProductResponse:
        """
        Update a product in the database.

        Args:
            product_id (str): The ID of the product to update.
            request (ProductRequest): The product request object containing updated product details.

        Returns:
            ProductResponse: The response object containing the updated product details.
        """

        product_model = await self.repository.get(product_id=product_id)

        if not product_model:
            raise NotFoundError(f"Product with ID {product_id} not found.")

        for key, value in request.to_dict().items():
            if value is not None:
                setattr(product_model, key, value)

        product_model = await self.repository.update(product_model)  # type: ignore

        response = await self.repository.map_product_model_to_response(
            product_model
        )

        return response

    async def delete(self, product_id: str) -> Message:
        """
        Delete a product from the database.

        Args:
            product_id (str): The ID of the product to delete.

        Returns:
            Message: A message indicating the result of the deletion.
        """

        await self.repository.delete(product_id=product_id)

        return Message(
            detail=f"Product with ID {product_id} deleted successfully."
        )

    async def add_product_batch(
        self, request: ProductBatchRequest
    ) -> ProductResponse:
        """
        Add a batch of products to the database.

        Args:
            request (ProductBatchRequest): The product batch request object containing product details.

        Returns:
            ProductResponse: The response object containing the added product details.
        """

        batch_model = self.repository.map_product_batch_request_to_model(
            request
        )

        batch_model = await self.repository.add_product_batch(batch_model)

        product_model = await self.repository.get(
            product_id=batch_model.product_id
        )

        response = await self.repository.map_product_model_to_response(
            product_model  # type: ignore
        )

        return response

    async def update_product_batch(
        self, product_batch_id: str, request: ProductBatchUpdate
    ) -> ProductResponse:
        """
        Update a batch of products in the database.

        Args:
            product_batch_id (str): The ID of the product batch to update.
            request (ProductBatchUpdate): The product batch request object containing updated product details.

        Returns:
            ProductResponse: The response object containing the updated product details.
        """

        batch_model = await self.repository.get_product_batch(
            product_batch_id=product_batch_id
        )

        if not batch_model:
            raise NotFoundError(
                f"Product batch with ID {product_batch_id} not found."
            )

        for key, value in request.to_dict().items():
            if value is not None:
                setattr(batch_model, key, value)

        batch_model = await self.repository.update_product_batch(batch_model)  # type: ignore

        product_model = await self.repository.get(
            product_id=batch_model.product_id
        )

        response = await self.repository.map_product_model_to_response(
            product_model  # type: ignore
        )

        return response

    async def delete_product_batch(self, product_batch_id: str) -> Message:
        """
        Delete a batch of products from the database.

        Args:
            product_batch_id (str): The ID of the product batch to delete.

        Returns:
            Message: A message indicating the result of the deletion.
        """

        await self.repository.delete_product_batch(
            product_batch_id=product_batch_id
        )

        return Message(
            detail=f"Product batch with ID {product_batch_id} deleted successfully."
        )

    async def add_recipe(self, request: RecipeRequest) -> ProductResponse:
        """
        Add a recipe to a product in the database.

        Args:
            product_id (str): The ID of the product to add the recipe to.
            request (RecipeRequest): The recipe request object containing recipe details.

        Returns:
            ProductResponse: The response object containing the updated product details.
        """

        product_model = await self.repository.get(
            product_id=request.product_id
        )
        if not product_model:
            raise NotFoundError(
                f"Product with ID {request.product_id} not found."
            )

        portion_models = self.repository.map_recipe_request_to_models(request)

        await self.repository.add_portion(portion_models)

        response = await self.repository.map_product_model_to_response(
            product_model  # type: ignore
        )

        return response

    async def update_recipe(
        self, portion_id: str, new_quantity: float
    ) -> ProductResponse:
        """
        Update a recipe in the database.

        Args:
            portion_id (str): The ID of the portion to update.
            new_quantity (float): The new quantity of the ingredient.

        Returns:
            ProductResponse: The response object containing the updated product details.
        """

        portion_model = await self.repository.get_portion(
            portion_id=portion_id
        )

        if not portion_model:
            raise NotFoundError(f"Portion with ID {portion_id} not found.")

        portion_model.quantity = new_quantity  # type: ignore

        await self.repository.update_portion(portion_model)  # type: ignore

        product_model = await self.repository.get(
            product_id=portion_model.product_id  # type: ignore
        )

        response = await self.repository.map_product_model_to_response(
            product_model  # type: ignore
        )

        return response

    async def delete_recipe(self, portion_id: str) -> Message:
        """
        Delete a recipe from the database.

        Args:
            portion_id (str): The ID of the portion to delete.

        Returns:
            Message: A message indicating the result of the deletion.
        """

        await self.repository.delete_portion(portion_id=portion_id)

        return Message(
            detail=f"Portion with ID {portion_id} deleted successfully."
        )
