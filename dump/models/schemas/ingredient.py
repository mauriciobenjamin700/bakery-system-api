import datetime

import datetime
from pydantic import (
    field_validator,
    model_validator    
)


from src.models.schemas.base import CustomBaseModel

class IngredientRequest(CustomBaseModel):
    """
    Essa classe serve para inserir um registro de "Ingredient" no banco de dados.

    - Attributes:
        - name: str
        - measure: int
        - image_path: str
        - mark: str
        - description: str
        - value: float
        - validity: date
        - quantity: float
        - min_quantity: float
    """
    name: str | None = None
    measure: int | None = None
    image_path: str | None = None
    mark: str | None = None
    description: str | None = None
    value: float | None = None
    min_quantity: float | None = None
    validity: datetime.date | None = None
    quantity: float | None = None

    
    @field_validator("name")
    def validate_name(cls, v):
        if not v:
            raise ValueError("O nome do ingrediente é obrigatorio")
        
        if v.strip() == "":
            raise ValueError("O nome do ingrediente é obrigatorio")
        return v
    
    @field_validator("measure")
    def validate_measure(cls, v):
        if not v:
            raise ValueError("A medida do ingrediente é obrigatorio")
        
        if v <= 0:
            raise ValueError("A medida do ingrediente deve ser maior que zero")
        return v
    
    @field_validator("value")
    def validate_value(cls, v):
        if not v:
            raise ValueError("O valor do ingrediente é obrigatorio")
        
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
            raise ValueError("A quantidade do ingrediente é obrigatorio")
        
        if v <= 0:
            raise ValueError("A quantidade do ingrediente deve ser maior que zero")
        return v
    
    @field_validator("min_quantity")
    def validate_min_quantity(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("A quantidade minima do ingrediente deve ser maior que zero")
            return v
    

class IngredientUpdate(CustomBaseModel):
    """
    Essa classe serve para atualizar um registro de "Ingredient" no banco de dados.\n
    Obs.: A atualização serve para modificar apenas os atributos de "Ingredient",\n
    caso queira modificar atributos com quantity e validity use a classe LoteIngredientUpdate.

    - Attributes:
        - id: int (O id do ingrediente)
        - name: str
        - measure: int
        - image_path: str
        - mark: str
        - description: str
        - min_quantity: float
    """
    id: int | None = None 
    name: str | None = None
    measure: int | None = None
    image_path: str | None = None
    mark: str | None = None
    description: str | None = None
    min_quantity: float | None = None
    
    @field_validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("O id do ingrediente é obrigatorio")
        
        if v <= 0:
            raise ValueError("O id do ingrediente deve ser maior que zero")
        return v
    
    @model_validator(mode="before")
    def anything(cls, values):
        name = values.get("name")
        measure = values.get("measure")
        image_path = values.get("image_path")
        mark = values.get("mark")
        description = values.get("description")
        min_quantity = values.get("min_quantity")
        
        if (
            not name and
            not measure and
            not image_path and
            not mark and
            not description and
            not min_quantity
        ):
            raise ValueError("Nenhum campo foi selecionado para ser atualizado")
        
        return values

class LoteIngredientRequest(CustomBaseModel):
    """
    Essa classe serve para cadastrar um registro de "LoteIngredient" no banco de dados

    - Attributes:
        - id_ingredient: int (O id do ingrediente)
        - validity: date
        - quantity: float
    """
    id_ingredient: int | None = None
    validity: datetime.date | None = None
    quantity: float | None = None
    
    @field_validator("id_ingredient")
    def validate_id_ingredient(cls, v):
        if not v:
            raise ValueError("O id do ingrediente é obrigatorio")
        
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
            raise ValueError("A quantidade do lote do ingrediente é obrigatorio")
        
        if v <= 0:
            raise ValueError("A quantidade do lote do ingrediente deve ser maior que zero")
        return v
    

class LoteIngredientUpdate(CustomBaseModel):
    """
    Essa classe serve para atualizar um registro de "LoteIngredient" no banco de dados

    - Attributes:
        - id: int (O id do lote do ingrediente)
        - validity: date
        - quantity: float
    """
    id: int | None = None
    validity: datetime.date | None = None
    quantity: float | None = None
    
    @field_validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("O id do lote do ingrediente é obrigatorio")
        
        if v <= 0:
            raise ValueError("O id do lote do ingrediente deve ser maior que zero")
        return v
    
    @model_validator(mode="before")
    def anything(cls, values):
        validity = values.get("validity")
        quantity = values.get("quantity")
        
        if (
            not validity and
            not quantity
        ):
            raise ValueError("Nenhum campo foi selecionado para ser atualizado")
        
        return values
   

class IngredientResponse(CustomBaseModel):
    '''
    Essa classe serve para retornar um registro de "Ingredient" com a quantidade e a validade do lote
    
    - Attributes:
        - id:int (O id do ingrediente)
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
    id:int
    name: str
    measure: int
    image_path: str | None = None
    mark: str | None = None
    description: str | None = None
    value: float
    quantity: float
    min_quantity: float | None = None

class LoteIngredientResponse(CustomBaseModel):
    '''
    Essa classe serve para retornar um registro de "Lote Ingredient" com a quantidade e a validade do lote.
    
    - Attributes:
        - ingredient_id: int (O id do ingrediente)
        - lote_id: int (O id do lote do ingrediente)
        - quantity: float
        - validity: date | None = None
    '''
    id_ingredient: int
    id: int
    quantity: float
    validity: datetime.date | None = None
    register_date: datetime.datetime | None = None