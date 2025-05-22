from datetime import date

from pydantic import Field

from app.core.constants.enums.base import MeasureEnum
from app.schemas.settings import validators
from app.schemas.settings.base import BaseSchema


class ProductBase(BaseSchema):
    """
    Base schema for product.

    Attributes:
        name (str): The name of the product.
        price_cost (float): The cost price of the product.
        price_sale (float): The sale price of the product.
        measure (MeasureEnum): The measure of the product.
        description (str): The description of the product.
        mark (str | None): The mark of the product.
        min_quantity (float | None): The minimum quantity of the product.
    """

    name: str = Field(
        examples=["Farinha de trigo", "Açúcar", "Sal"],
        description="Name of the product",
    )
    price_cost: float = Field(
        examples=[1.5, 2.0, 3.0], ge=0, description="Cost price of the product"
    )
    price_sale: float = Field(
        examples=[1.5, 2.0, 3.0], ge=0, description="Sale price of the product"
    )
    measure: MeasureEnum
    description: str = Field(
        examples=[
            "Farinha de trigo para bolos",
            "Açúcar cristal",
            "Sal refinado",
        ]
    )
    mark: str | None = Field(
        examples=["Marca A", "Marca B", "Marca C"],
        default=None,
        description="Mark of the product",
    )
    min_quantity: float | None = Field(
        examples=[0.5, 1.0, 2.0],
        ge=0,
        default=None,
        description="Minimum quantity of the product",
    )


class BasePortion(BaseSchema):
    """
    Base schema for portion.

    Attributes:
        ingredient_id (str): The ID of the ingredient.
        quantity (float): The quantity of the ingredient.
    """

    ingredient_id: str
    quantity: float


class PortionRequest(BasePortion):
    """
    Additional request schema for portion.

    Attributes:
        ingredient_id (str): The ID of the ingredient.
        quantity (float): The quantity of the ingredient.
    """

    pass


class BaseProductBatch(BaseSchema):
    """
    Base schema for product batch.
    Attributes:
        product_id (str): The ID of the product.
        validity (date | None): The validity date of the product.
        quantity (float): The quantity of the product.
    """

    product_id: str
    validity: date | None = None
    quantity: float


class ProductRequest(ProductBase):
    """
    Request schema for product.

    Attributes:
        name (str): The name of the product.
        price_cost (float): The cost price of the product.
        price_sale (float): The sale price of the product.
        measure (MeasureEnum): The measure of the product.
        description (str): The description of the product.
        mark (str): The mark of the product.
        min_quantity (float): The minimum quantity of the product.
        recipe (list[PortionRequest] | None): The recipe of the product.
        quantity (float): The quantity of the product.
        validity (date | None): The validity date of the product.
    """

    recipe: list[PortionRequest] | None = None
    quantity: float = Field(
        examples=[0.5, 1.0, 2.0], ge=0, description="Quantity of the product"
    )
    validity: date | None = Field(
        examples=["2025-10-02", "2025-12-31"],
        description="Validity date of the product",
        default=None,
    )


class ProductUpdate(BaseSchema):
    """
    Class for updating product details.
    Attributes:
        name (str | None): The name of the product.
        price_cost (float | None): The cost price of the product.
        price_sale (float | None): The sale price of the product.
        measure (MeasureEnum | None): The measure of the product.
        description (str | None): The description of the product.
        mark (str | None): The mark of the product.
        min_quantity (float | None): The minimum quantity of the product.
    """

    name: str | None = None
    price_cost: float | None = None
    price_sale: float | None = None
    measure: MeasureEnum | None = None
    description: str | None = None
    mark: str | None = None
    min_quantity: float | None = None


class RecipeRequest(BaseSchema):
    """
    Request schema for recipe.

    Attributes:
        product_id (str): The ID of the product.
        recipe (list[PortionRequest]): The recipe of the product.
    """

    product_id: str
    recipe: list[PortionRequest]


class ProductBatchRequest(BaseProductBatch):
    """
    Request schema for product batch.

    Attributes:
        product_id (str): The ID of the product.
        validity (date | None): The validity date of the product.
        quantity (float): The quantity of the product.
    """

    pass


class ProductBatchUpdate(BaseSchema):
    """
    Class for updating product batch details.
    Attributes:
        validity (date | None): The validity date of the product.
        quantity (float | None): The quantity of the product.
    """

    validity: date | None = None
    quantity: float | None = None


class PortionResponse(BaseSchema):
    """
    Response schema for portion.

    Attributes:
        id (str): The ID of the portion.
        ingredient_id (str): The ID of the ingredient.
        ingredient_name (str): The name of the ingredient.
        ingredient_measure (MeasureEnum): The measure of the ingredient.
        ingredient_quantity (float): The quantity of the ingredient.
    """

    id: str
    ingredient_id: str
    ingredient_name: str
    ingredient_measure: MeasureEnum
    ingredient_quantity: float


class RecipeResponse(BaseSchema):
    """
    Response schema for recipe.

    Attributes:
        recipe (list[PortionResponse]): The recipe of the product.
    """

    recipe: list[PortionResponse]


class ProductBatchResponse(BaseProductBatch):
    """
    Response schema for product batch.

    Attributes:
        product_id (str): The ID of the product.
        validity (date | None): The validity date of the product.
        quantity (float): The quantity of the product.
        id (str): The ID of the product batch.
        created_at (str): The creation date of the product batch.
        updated_at (str): The last update date of the product batch.
    """

    id: str
    created_at: str
    updated_at: str

    _parse_created_at = validators.validate_created_at
    _parse_updated_at = validators.validate_updated_at


class ProductResponse(ProductBase):
    """
    Response schema for product.

    Attributes:
        name (str): The name of the product.
        price_cost (float): The cost price of the product.
        price_sale (float): The sale price of the product.
        measure (MeasureEnum): The measure of the product.
        description (str): The description of the product.
        mark (str): The mark of the product.
        min_quantity (float): The minimum quantity of the product.
        id (str): The ID of the product.
        image_path (str): The path to the product image.
        quantity (float): The quantity of the product.
        recipe (list[PortionResponse] | None): The recipe of the product.
        batches (list[ProductBatchResponse] | None): The batches of the product.
        created_at (str): The creation date of the product.
        updated_at (str): The last update date of the product.
    """

    id: str
    image_path: str
    quantity: float
    recipe: list[PortionResponse] | None = None
    batches: list[ProductBatchResponse] | None = None
    created_at: str = Field("examples=2025-10-02 12:00:00")
    updated_at: str = Field("examples=2025-10-02 12:00:00")

    _parse_created_at = validators.validate_created_at
    _parse_updated_at = validators.validate_updated_at
