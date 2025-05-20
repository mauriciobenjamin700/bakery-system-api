import datetime

from pydantic import Field

from app.core.constants.enums.ingredient import IngredientMeasureEnum
from app.schemas.settings import validators
from app.schemas.settings.base import BaseSchema


class IngredientBase(BaseSchema):
    """
    Base schema for Ingredient

    Attributes:
        name (str): The name of the ingredient
        measure (IngredientMeasureEnum): The measure of the ingredient
        mark (str): The mark of the ingredient
        description (str): The description of the ingredient
        value (float): The value of the ingredient
        min_quantity (float): The minimum quantity of the ingredient
        quantity (float): The quantity of the ingredient
    """

    name: str = Field(examples=["Farinha de trigo", "Açúcar", "Sal"])
    measure: IngredientMeasureEnum = Field(
        examples=[
            IngredientMeasureEnum.KG,
            IngredientMeasureEnum.L,
            IngredientMeasureEnum.UNITY,
        ]
    )
    mark: str | None = Field(
        examples=["Marca A", "Marca B", "Marca C"],
        default=None,
        validate_default=True,
    )
    description: str = Field(
        examples=[
            "Farinha de trigo para bolos",
            "Açúcar cristal",
            "Sal refinado",
        ],
        default=None,
        validate_default=True,
    )
    value: float = Field(
        examples=[1.5, 2.0, 3.0],
        ge=0,
    )
    min_quantity: float = Field(examples=[0.5, 1.0, 2.0], ge=0)

    _validate_name = validators.validate_name
    _validate_mark = validators.validate_mark
    _validate_description = validators.validate_description


class IngredientRequest(IngredientBase):
    """
    A schema with data to create a new ingredient on db

    Attributes:
        name (str): The name of the ingredient
        measure (IngredientMeasureEnum): The measure of the ingredient
        mark (str): The mark of the ingredient
        description (str): The description of the ingredient
        value (float): The value of the ingredient
        min_quantity (float): The minimum quantity of the ingredient
        validity (date | None): The validity of the ingredient
        quantity (float): The quantity of the ingredient
    """

    quantity: float = Field(examples=[10.0, 20.0, 30.0], ge=0)
    validity: datetime.date | None = Field(
        examples=["2023-12-31", "2024-01-01", "2024-02-28"], default=None
    )


class IngredientUpdate(IngredientBase):
    """
    A schema with data to update an ingredient on db

    Attributes:
        name (str): The name of the ingredient
        measure (IngredientMeasureEnum): The measure of the ingredient
        mark (str): The mark of the ingredient
        description (str): The description of the ingredient
        value (float): The value of the ingredient
        min_quantity (float): The minimum quantity of the ingredient
        validity (date | None): The validity of the ingredient
    """

    pass


class IngredientBatchBase(BaseSchema):
    """
    Base schema for IngredientBatch

    Attributes:
        ingredient_id (str): The id of the ingredient
        validity (date | None): The validity of the ingredient
        quantity (float): The quantity of the ingredient

    """

    ingredient_id: str = Field(examples=["1", "2", "3"])
    validity: datetime.date | None = Field(
        examples=["2023-12-31", "2024-01-01", "2024-02-28"], default=None
    )
    quantity: float = Field(
        examples=[10.0, 20.0, 30.0],
        ge=0,
    )


class IngredientBatchRequest(IngredientBatchBase):
    """
    Essa classe serve para cadastrar um registro de "LoteIngredient" no banco de dados

    - Attributes:
        - ingredient_id: str (O id do ingrediente)
        - validity: date
        - quantity: float
    """

    pass


class IngredientBatchUpdate(BaseSchema):
    """
    Essa classe serve para atualizar um registro de "LoteIngredient" no banco de dados

    - Attributes:
        - validity: date | None
        - quantity: float | None
    """

    validity: datetime.date | None = Field(
        examples=["2023-12-31", "2024-01-01", "2024-02-28"], default=None
    )
    quantity: float | None = Field(
        examples=[10.0, 20.0, 30.0],
        ge=0,
    )


class IngredientBatchResponse(IngredientBatchBase):
    """
    A schema with data to create a new ingredient on db

    Attributes:
        ingredient_id (str): The id of the ingredient
        id (str): The id of the ingredient
        quantity (float): The quantity of the ingredient
        validity (date): The validity of the ingredient
        created_at (str): The date and time when the ingredient was created
        updated_at (str): The date and time when the ingredient was last updated
    """

    id: str = Field(
        description="O id do lote do ingrediente", examples=["1", "2", "3"]
    )
    created_at: str = Field(
        description="A data e hora em que o lote do ingrediente foi criado",
        examples=[
            "2023-12-31 12:00",
            "2024-01-01 12:00",
            "2024-02-28 12:00",
        ],
    )
    updated_at: str = Field(
        description="A data e hora em que o lote do ingrediente foi atualizado",
        examples=[
            "2023-12-31 12:00",
            "2024-01-01 12:00",
            "2024-02-28 12:00",
        ],
    )
    _validate_created_at = validators.validate_created_at
    _validate_updated_at = validators.validate_updated_at


class IngredientResponse(IngredientBase):
    """
    Essa classe serve para retornar um registro de "Ingredient" com a quantidade e a validade do lote

    Attributes:
        id (str): The id of the ingredient
        name (str): The name of the ingredient
        measure (int): The measure of the ingredient
        mark (str): The mark of the ingredient
        description (str): The description of the ingredient
        value (float): The value of the ingredient
        min_quantity (float): The minimum quantity of the ingredient
        quantity (float): The quantity of the ingredient
        image_path (str): The path to the image of the ingredient
        created_at (str): The date and time when the ingredient was created
        updated_at (str): The date and time when the ingredient was last updated
        batches (list[IngredientBatchResponse]): The list of batches of the ingredient
    """

    id: str = Field(
        description="O id do ingrediente", examples=["1", "2", "3"]
    )
    image_path: str | None = Field(
        examples=[
            "/images/farinha.jpg",
            "/images/açúcar.jpg",
            "/images/sal.jpg",
        ],
        default=None,
    )
    quantity: float = Field(examples=[10.0, 20.0, 30.0], ge=0)
    created_at: str = Field(
        description="A data e hora em que o ingrediente foi criado",
        examples=[
            "2023-12-31 12:00",
            "2024-01-01 12:00",
            "2024-02-28 12:00",
        ],
    )
    updated_at: str = Field(
        description="A data e hora em que o ingrediente foi atualizado",
        examples=[
            "2023-12-31 12:00",
            "2024-01-01 12:00",
            "2024-02-28 12:00",
        ],
    )
    batches: list[IngredientBatchResponse]

    _validate_created_at = validators.validate_created_at
    _validate_updated_at = validators.validate_updated_at
