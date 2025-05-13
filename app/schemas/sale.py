from pydantic import Field

from app.schemas.product import ProductResponse
from app.schemas.settings.base import BaseSchema
from app.schemas.user import UserResponse


class SaleBase(BaseSchema):
    """
    Base schema for sale.

    Attributes:
        product_id (str): The ID of the product.
        user_id (str): The ID of the user.
        quantity (float): The quantity of the product sold.
    """

    product_id: str = Field(examples=["1234567890"])
    user_id: str = Field(examples=["0987654321"])
    quantity: float = Field(examples=[1.0])


class SaleRequest(SaleBase):
    """
    Request schema for sale.

    Attributes:
        product_id (str): The ID of the product.
        user_id (str): The ID of the user.
        quantity (float): The quantity of the product sold.
    """

    pass


class SaleResponse(SaleBase):
    """
    Response schema for sale.

    Attributes:
        product_id (str): The ID of the product.
        user_id (str): The ID of the user.
        quantity (float): The quantity of the product sold.
    """

    id: str = Field(examples=["1234567890"])
    is_paid: bool = Field(examples=[True])
    value: float = Field(examples=[10.0])
    created_at: str = Field(examples=["2023-10-01T12:00:00Z"])


class SaleNoteRequest(BaseSchema):
    """
    Request schema for sale note.

    Attributes:
        sales (list[SaleRequest]): A list of sales.
    """

    sales: list[SaleRequest]


class SaleNoteResponse(BaseSchema):
    """
    Response schema for sale note.
    Attributes:
        client (UserResponse): The user who made the sale.
        products (list[ProductResponse]): A list of products sold.
        notes (list[SaleResponse]): A list of sales.
        total_value (float): The total value of the sale.
    """

    client: UserResponse
    products: list[ProductResponse]
    notes: list[SaleResponse]
    total_value: float
