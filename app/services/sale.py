from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError, ValidationError
from app.core.generate.ids import code_generator
from app.db.models import ProductModel, SaleModel, UserModel
from app.db.repositories import (
    ProductRepository,
    SaleRepository,
    UserRepository,
)
from app.schemas import (
    Message,
    SaleNoteRequest,
    SaleNoteResponse,
    SaleRequest,
    SaleResponse,
)


class SaleService:
    """
    Service class for handling Sale operations.

    Attributes:
        repository (SaleRepository): The repository instance for database operations.
    Methods:
        add(request: SaleRequest | SaleNoteRequest) -> SaleResponse | SaleNoteResponse:
            Adds a SaleModel to the database.

        get_sales_by_employee_id(employee_id: str) -> list[SaleResponse]:
            Retrieves sales by employee ID.

        get_sales_by_product_id(product_id: str) -> list[SaleResponse]:
            Retrieves sales by product ID.

        get_sales_by_sale_code(sale_code: str) -> list[SaleResponse]:
            Retrieves sales by sale code.

        get_sale_note_by_sale_code(sale_code: str) -> SaleNoteResponse:
            Retrieves a sale note by sale code.

        get_all() -> list[SaleResponse]:
            Retrieves all sales.

        delete(sale_id: str) -> Message:
            Deletes a sale by ID.

        confirm_sale(sale_code: str) -> SaleNoteResponse:
            Confirms a sale note by sale code.

        cancel_sale_note(sale_code: str) -> Message:
            Cancels a sale note by sale code.

        build_sale_note_response(employee: UserModel, products: list[ProductModel], sales: list[SaleModel]) -> SaleNoteResponse:
            Builds a SaleNoteResponse object from the given data.
    """

    def __init__(self, db_session: AsyncSession):
        self.repository = SaleRepository(db_session)
        self.product_repository = ProductRepository(db_session)

    async def add(
        self, request: SaleRequest | SaleNoteRequest
    ) -> SaleResponse | SaleNoteResponse:
        """
        Async method to add a SaleModel to the database.

        Args:
            model (SaleRequest): The model object to add.

        Returns:
            SaleResponse: The added model object.
        """

        if not isinstance(request, (SaleRequest, SaleNoteRequest)):
            raise ValidationError(
                "request",
                "request must be of type SaleRequest or SaleNoteRequest",
            )

        sale_code = code_generator()

        if type(request) is SaleRequest:
            model = await self.repository.map_request_to_model(
                request, sale_code
            )

            model = await self.repository.add(model)

            response = await self.repository.map_model_to_response(model)  # type: ignore

        elif type(request) is SaleNoteRequest:

            for sale in request.sales:

                model = await self.repository.map_request_to_model(
                    sale, sale_code
                )

                model = await self.repository.add(model)

            employee, products, sales = (
                await self.repository.get_sale_note_data(sale_code=sale_code)  # type: ignore
            )

            response = await self.build_sale_note_response(
                employee=employee,
                products=products,  # type: ignore
                sales=sales,  # type: ignore
            )

        return response  # type: ignore

    async def get_sales_by_employee_id(
        self, employee_id: str
    ) -> list[SaleResponse]:
        """
        Get sales by employee ID.

        Args:
            employee_id (str): The ID of the employee.

        Returns:
            list[SaleResponse]: List of SaleResponse objects.
        """

        sales = await self.repository.get(
            user_id=employee_id, all_results=True
        )
        if not sales:
            raise NotFoundError(
                "sales not found",
            )

        return [self.repository.map_model_to_response(sale) for sale in sales]  # type: ignore

    async def get_sales_by_product_id(
        self, product_id: str
    ) -> list[SaleResponse]:
        """
        Get sales by product ID.

        Args:
            product_id (str): The ID of the product.

        Returns:
            list[SaleResponse]: List of SaleResponse objects.
        """

        sales = await self.repository.get(
            product_id=product_id, all_results=True
        )
        if not sales:
            raise NotFoundError(
                "sales not found",
            )

        return [self.repository.map_model_to_response(sale) for sale in sales]  # type: ignore

    async def get_sales_by_sale_code(
        self, sale_code: str
    ) -> list[SaleResponse]:
        """
        Get sales by sale code.
        Args:
            sale_code (str): The sale code of the sales to retrieve.
        Returns:
            list[SaleResponse]: List of SaleResponse objects.
        """
        sales = await self.repository.get(
            sale_code=sale_code, all_results=True
        )
        if not sales:
            raise NotFoundError(
                "sales not found",
            )

        return [self.repository.map_model_to_response(sale) for sale in sales]  # type: ignore

    async def get_all(self) -> list[SaleResponse]:
        """
        Get all sales.

        Returns:
            list[SaleResponse]: List of SaleResponse objects.
        """

        sales = await self.repository.get(all_results=True)
        if not sales:
            raise NotFoundError(
                "sales not found",
            )

        return [self.repository.map_model_to_response(sale) for sale in sales]  # type: ignore

    async def get_sale_note_by_sale_code(
        self, sale_code: str
    ) -> SaleNoteResponse:
        """
        Get a sale note by sale code.

        Args:
            sale_code (str): The sale code of the sale note to retrieve.

        Returns:
            SaleNoteResponse: The SaleNoteResponse object.
        """

        employee, products, sales = await self.repository.get_sale_note_data(
            sale_code=sale_code  # type: ignore
        )

        if not employee or not products or not sales:
            raise NotFoundError(
                "sale note not found",
            )

        return await self.build_sale_note_response(
            employee=employee,
            products=products,  # type: ignore
            sales=sales,  # type: ignore
        )

    async def delete(self, sale_id: str) -> Message:
        """
        Delete a sale by ID.

        Args:
            sale_id (str): The ID of the sale to delete.

        Returns:
            SaleResponse: The deleted SaleResponse object.
        """

        sale = await self.repository.delete(sale_id)
        if not sale:
            raise NotFoundError(
                "sale not found",
            )

        return Message(
            detail="sale deleted",
        )

    async def confirm_sale(self, sale_code: str) -> SaleNoteResponse:
        """
        Confirm a sale note by sale code.
        Args:
            sale_code (str): The sale code of the sale note to confirm.
        Returns:
            SaleNoteResponse: The confirmed SaleNoteResponse object.
        """
        sales = await self.repository.get(
            sale_code=sale_code, all_results=True
        )

        if not sales:
            raise NotFoundError(
                "sale note not found",
            )

        for sale in sales:  # type: ignore
            sale.is_paid = True
            await self.repository.update(model=sale)

        employee, products, sales = await self.repository.get_sale_note_data(
            sale_code=sale_code  # type: ignore
        )

        return await self.build_sale_note_response(
            employee=employee,
            products=products,  # type: ignore
            sales=sales,  # type: ignore
        )

    async def cancel_sale_note(self, sale_code: str) -> Message:
        """
        Cancel a sale note by sale code.

        Args:
            sale_code (str): The sale code of the sale note to cancel.

        Returns:
            SaleNoteResponse: The canceled SaleNoteResponse object.
        """

        sales = await self.repository.get(
            sale_code=sale_code, all_results=True
        )

        if not sales:
            raise NotFoundError(
                "sale note not found",
            )

        for sale in sales:  # type: ignore

            await self.repository.delete(model=sale)

        return Message(
            detail="sale note canceled",  # type: ignore
        )

    async def build_sale_note_response(
        self,
        employee: UserModel,
        products: list[ProductModel],
        sales: list[SaleModel],
    ) -> SaleNoteResponse:
        """
        Build a SaleNoteResponse object from the given data.

        Args:
            employee (UserModel): The employee user model.
            products (list[ProductModel]): List of product models.
            sales (list[SaleModel]): List of sale models.

        Returns:
            SaleNoteResponse: The constructed SaleNoteResponse object.
        """

        seller = UserRepository.map_model_to_response(employee)  # type: ignore
        product_responses = [
            await self.product_repository.map_product_model_to_response(
                product
            )
            for product in products
        ]
        notes = [
            await self.repository.map_model_to_response(sale) for sale in sales  # type: ignore
        ]
        total_value = sum([sale.value for sale in sales])

        return SaleNoteResponse(
            seller=seller,
            products=product_responses,
            notes=notes,
            total_value=total_value,
        )
