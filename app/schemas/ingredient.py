import datetime
from pydantic import (
    Field,
    field_validator
)


from app.core.constants.enums.ingredient import IngredientMeasureEnum
from app.schemas.settings.base import BaseSchema

class IngredientRequest(BaseSchema):
    """
    A schema with data to create a new ingredient on db

    A
    """
    name: str = Field(
        examples=["Farinha de trigo", "Açúcar", "Sal"],
        default=None
        validate_default=True
    )
    measure: IngredientMeasureEnum = Field(
        examples=[IngredientMeasureEnum.KG, IngredientMeasureEnum.L, IngredientMeasureEnum.UNITY],
        default=None,
        validate_default=True
    )
    mark: str = Field(
        examples=["Marca A", "Marca B", "Marca C"],
        default=None,
        validate_default=True
    )
    description: str = Field(
        examples=["Farinha de trigo para bolos", "Açúcar cristal", "Sal refinado"],
        default=None,
        validate_default=True
    )
    value: float = Field(
        examples=[1.5, 2.0, 3.0],
        default=None,
        validate_default=True
    )
    min_quantity: float = Field(
        examples=[0.5, 1.0, 2.0],
        default=None,
        validate_default=True
    )
    validity: datetime.date | None = Field(
        examples=["2023-12-31", "2024-01-01", "2024-02-28"], 
        default=None
    )
    quantity: float =  Field(
        examples=[10.0, 20.0, 30.0],
        default=None,
        validate_default=True
    )

    
    @field_validator("name")
    def validate_name(cls, v):
        if not v:
            raise ValueError("O nome do ingrediente é obrigatório")
        
        if v.strip() == "":
            raise ValueError("O nome do ingrediente é obrigatório")
        return v
    
    @field_validator("measure")
    def validate_measure(cls, v):
        if not v:
            raise ValueError("A medida do ingrediente é obrigatório")
        
        if v not in IngredientMeasureEnum.values():
            raise ValueError("A medida do ingrediente deve ser maior que zero")
        return v
    
    @field_validator("mark")
    def validate_mark(cls, v):
        if not v:
            raise ValueError("A marca do ingrediente é obrigatório")
        if isinstance(v, str):
            v.strip()
            if v.strip() == "":
                raise ValueError("A marca do ingrediente é obrigatória")
        return v
    
    @field_validator("value")
    def validate_value(cls, v):
        if not v:
            raise ValueError("O valor do ingrediente é obrigatório")
        
        if v <= 0:
            raise ValueError("O valor do ingrediente deve ser maior que zero")
        return v
    
    @field_validator("validity")
    def validate_validity(cls, v):
        
        if v is not None:
            if v < datetime.date.today():
                raise ValueError("A validade do ingrediente não pode ser menor que a data atual")
            return v
    
    @field_validator("quantity")
    def validate_quantity(cls, v):
        if not v:
            raise ValueError("A quantidade do ingrediente é obrigatório")
        
        if v <= 0:
            raise ValueError("A quantidade do ingrediente deve ser maior que zero")
        return v
    
    @field_validator("min_quantity")
    def validate_min_quantity(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("A quantidade minima do ingrediente deve ser maior que zero")
            return v
        

class LoteIngredientRequest(BaseSchema):
    """
    Essa classe serve para cadastrar um registro de "LoteIngredient" no banco de dados

    - Attributes:
        - ingredient_id: str (O id do ingrediente)
        - validity: date
        - quantity: float
    """
    ingredient_id: str = Field(examples=["1", "2", "3"])
    validity: datetime.date = Field(examples=["2023-12-31", "2024-01-01", "2024-02-28"])
    quantity: float = Field(examples=[10.0, 20.0, 30.0])
    
    @field_validator("ingredient_id")
    def validate_id_ingredient(cls, v):
        if not v:
            raise ValueError("O id do ingrediente é obrigatório")
        
        if v <= 0:
            raise ValueError("O id do ingrediente deve ser maior que zero")
        return v
    
    @field_validator("validity")
    def validate_validity(cls, v):
        if v is not None:
            if v < datetime.date.today():
                raise ValueError("A validade do lote do ingrediente não pode ser menor que a data atual")
            return v
        
    @field_validator("quantity")
    def validate_quantity(cls, v):
        if not v:
            raise ValueError("A quantidade do lote do ingrediente é obrigatório")
        
        if v <= 0:
            raise ValueError("A quantidade do lote do ingrediente deve ser maior que zero")
        return v
    

class IngredientResponse(BaseSchema):
    '''
    Essa classe serve para retornar um registro de "Ingredient" com a quantidade e a validade do lote
    
    - Attributes:
        - id:str (O id do ingrediente)
        - name: str
        - measure: int
        - image_path: str | None = None
        - mark: str | None = None
        - description: str | None = None
        - value: float
        - validity: date | None = None
        - quantity: float
        - min_quantity: float | None = None
    '''
    id:str = Field(examples=["1", "2", "3"])
    name: str = Field(examples=["Farinha de trigo", "Açúcar", "Sal"])
    measure: IngredientMeasureEnum = Field(examples=[IngredientMeasureEnum.KG, IngredientMeasureEnum.L, IngredientMeasureEnum.UNITY])
    image_path: str | None = Field(examples=["/images/farinha.jpg", "/images/acucar.jpg", "/images/sal.jpg"])
    mark: str | None = Field(examples=["Marca A", "Marca B", "Marca C"])
    description: str | None = Field(examples=["Farinha de trigo para bolos", "Açúcar cristal", "Sal refinado"])
    value: float = Field(examples=[1.5, 2.0, 3.0])
    quantity: float = Field(examples=[10.0, 20.0, 30.0])
    min_quantity: float | None = Field(examples=[0.5, 1.0, 2.0])

class LoteIngredientResponse(BaseSchema):
    '''
    Essa classe serve para retornar um registro de "Lote Ingredient" com a quantidade e a validade do lote.
    
    - Attributes:
        - ingredient_id: str (O id do ingrediente)
        - id: str (O id do lote do ingrediente)
        - quantity: float
        - validity: date | None = None
        - register_date: datetime | None = None
    '''
    ingredient_id: str = Field(examples=["1", "2", "3"])
    id: str = Field(examples=["1", "2", "3"])
    quantity: float = Field(examples=[10.0, 20.0, 30.0])
    validity: datetime.date | None = Field(examples=["2023-12-31", "2024-01-01", "2024-02-28"])
    register_date: datetime.datetime | None = Field(examples=["2023-12-31", "2024-01-01", "2024-02-28"])