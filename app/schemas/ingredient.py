import datetime

from pydantic import Field, field_validator

from app.core.constants.enums.ingredient import IngredientMeasureEnum
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
    name: str = Field(
        examples=["Farinha de trigo", "Açúcar", "Sal"],
        default=None,
        validate_default=True,
    )
    measure: IngredientMeasureEnum = Field(
        examples=[
            IngredientMeasureEnum.KG,
            IngredientMeasureEnum.L,
            IngredientMeasureEnum.UNITY,
        ],
        default=None,
        validate_default=True,
    )
    mark: str = Field(
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
        examples=[1.5, 2.0, 3.0], default=None, validate_default=True
    )
    min_quantity: float = Field(
        examples=[0.5, 1.0, 2.0], default=None, validate_default=True
    )
    quantity: float = Field(
        examples=[10.0, 20.0, 30.0], default=None, validate_default=True
    )

class IngredientRequest(IngredientBase):
    """
    A schema with data to create a new ingredient on db
    
    Attributes:
        name (str): The name of the ingredient
        measure (int): The measure of the ingredient
        mark (str): The mark of the ingredient
        description (str): The description of the ingredient
        value (float): The value of the ingredient
        min_quantity (float): The minimum quantity of the ingredient
        validity (date): The validity of the ingredient
        quantity (float): The quantity of the ingredient
    """


    validity: datetime.date | None = Field(
        examples=["2023-12-31", "2024-01-01", "2024-02-28"],
        default=None
    )


    @field_validator("value")
    def validate_value(cls, v):
        """
        Implementar
        """
        if not v:
            raise ValueError("O valor do ingrediente é obrigatório")

        if v <= 0:
            raise ValueError("O valor do ingrediente deve ser maior que zero")
        return v

    @field_validator("validity")
    def validate_validity(cls, v):
        """
        Implementar
        """

        if v is not None:
            if v < datetime.date.today():
                raise ValueError(
                    "A validade do ingrediente não pode ser menor que a data atual"
                )
            return v

    @field_validator("quantity")
    def validate_quantity(cls, v):
        """
        Implementar
        """
        if not v:
            raise ValueError("A quantidade do ingrediente é obrigatório")

        if v <= 0:
            raise ValueError(
                "A quantidade do ingrediente deve ser maior que zero"
            )
        return v

    @field_validator("min_quantity")
    def validate_min_quantity(cls, v):
        """
        Implementar
        """
        if v is not None:
            if v <= 0:
                raise ValueError(
                    "A quantidade minima do ingrediente deve ser maior que zero"
                )
            return v
        


class IngredientBatchBase(IngredientBase):
    ingredient_id: str = Field(
        examples=["1", "2", "3"]
    )
    validity: datetime.date = Field(
        examples=[
            "2023-12-31", 
            "2024-01-01", 
            "2024-02-28"
        ]
    )
    quantity: float = Field(
        examples=[10.0, 20.0, 30.0]
    )
    
    
    @field_validator("ingredient_id")
    def validate_id_ingredient(cls, v):
        """
        Implementar
        """
        if not v:
            raise ValueError("O id do ingrediente é obrigatório")

        if v <= 0:
            raise ValueError("O id do ingrediente deve ser maior que zero")
        return v

    @field_validator("validity")
    def validate_validity(cls, v):
        """
        Implementar
        """
        if v is not None:
            if v < datetime.date.today():
                raise ValueError(
                    "A validade do lote do ingrediente não pode ser menor que a data atual"
                )
            return v

    @field_validator("quantity")
    def validate_quantity(cls, v):
        """
        Valida a quantidade do lote do ingrediente"""
        if not v:
            raise ValueError(
                "A quantidade do lote do ingrediente é obrigatório"
            )

        if v <= 0:
            raise ValueError(
                "A quantidade do lote do ingrediente deve ser maior que zero"
            )
        return v
    
class IngredientBatchRequest(IngredientBatchBase):
    """
    Essa classe serve para cadastrar um registro de "LoteIngredient" no banco de dados

    - Attributes:
        - ingredient_id: str (O id do ingrediente)
        - validity: date
        - quantity: float
    """
    pass


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

    
    id: str = Field(examples=["1", "2", "3"])
    created_at: str = Field(
        examples=["2023-12-31 12:00:00", "2024-01-01 12:00:00", "2024-02-28 12:00:00"]
    )
    updated_at : str = Field(
        examples=["2023-12-31 12:00:00", "2024-01-01 12:00:00", "2024-02-28 12:00:00"]
    )


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
    """

    id: str = Field(examples=["1", "2", "3"])
    image_path: str | None = Field(
        examples=[
            "/images/farinha.jpg",
            "/images/açúcar.jpg",
            "/images/sal.jpg",
        ]
    )
    batches: list[IngredientBatchResponse]