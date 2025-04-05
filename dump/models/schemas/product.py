from datetime import date
from pydantic import (
    field_validator,
    model_validator
)


from src.models.schemas.base import CustomBaseModel

class ProductRequest(CustomBaseModel):
    """
    Essa classe serve para inserir um registro de "Product" no banco de dados.\n
    Quando esse registro for feito, um registro de "LoteProduct" será gerado em conjunto no banco de dados.

    - Attributes:
        - name: str
        - price_cost: float
        - price_sale: float
        - measure: int 
        - image_path: str
        - description: str
        - mark: str
        - validity: date
        - quantity: float
        - min_quantity: float
    """

    name: str | None = None
    price_cost: float | None = None
    price_sale: float | None = None
    measure: int | None = None
    image_path: str | None = None
    description: str | None = None
    mark: str | None = None
    min_quantity: float | None = None
    quantity: float | None = None
    validity: date | None = None
    
    @field_validator("name")
    def validate_name(cls, v):
        if not v:
            raise ValueError("O nome do produto é obrigatorio")
        
        if v.strip() == "":
            raise ValueError("O nome do produto é obrigatorio")
        return v
    
    @field_validator("price_cost")
    def validate_price_cost(cls, v):
        if not v:
            raise ValueError("O preço de custo do produto é obrigatorio")
        
        if v <= 0:
            raise ValueError("O preço de custo do produto deve ser maior que zero")
        return v
    
    @field_validator("price_sale")
    def validate_price_sale(cls, v):
        if not v:
            raise ValueError("O preço de venda do produto é obrigatorio")
        
        if v <= 0:
            raise ValueError("O preço de venda do produto deve ser maior que zero")
        return v
    
    
    @field_validator("measure")
    def validate_measure(cls, v):
        if not v:
            raise ValueError("A medida do produto é obrigatorio")
        
        if v <= 0:
            raise ValueError("A medida do produto deve ser maior que zero")
        return v
    
    

class ProductUpdate(CustomBaseModel):
    """
    Essa classe serve para atualizar um registro de "Product" no banco de dados.\n
    Obs.: A atualização serve para modificar apenas os atributos de "Product",\n
    caso queira modificar atributos com quantity e validity use a classe LoteProductUpdate.

    - Attributes:
        - id: int (O id do produto)
        - name: str
        - price_cost: float
        - price_sale: float
        - measure: int 
        - image_path: str
        - description: str
        - mark: str
        - min_quantity: float
    """
    id: int | None = None
    name: str | None = None
    price_cost: float | None = None
    price_sale: float | None = None
    measure: int | None = None
    image_path: str | None = None
    description: str | None = None
    mark: str | None = None
    min_quantity: float | None = None
    
    @field_validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("O id do produto é obrigatorio")
        
        if v <= 0:
            raise ValueError("O id do produto deve ser maior que zero")
        return v
    
    @model_validator(mode="before")
    def anything(cls, values):
        name = values.get("name")
        price_cost = values.get("price_cost")
        price_sale = values.get("price_sale")
        measure = values.get("measure")
        image_path = values.get("image_path")
        description = values.get("description")
        mark = values.get("mark")
        min_quantity = values.get("min_quantity")
        quantity = values.get("quantity")
        
        if (
            not name and
            not price_cost and
            not price_sale and
            not measure and
            not image_path and
            not description and
            not mark and
            not min_quantity
        ):
            raise ValueError("Nenhum campo foi preenchido para atualização")
        return values
    

class LoteProductRequest(CustomBaseModel):
    """
    Essa classe serve para cadastrar um registro de "LoteProduct" no banco de dados

    - Attributes:
        - product_id: int (O id do produto)
        - validity: date
        - quantity: float
    """
    product_id: int | None = None
    validity: date | None = None
    quantity: float | None = None
    
    @field_validator("product_id")
    def validate_id_product(cls, v):
        if not v:
            raise ValueError("O id do produto é obrigatorio")
        
        if v <= 0:
            raise ValueError("O id do produto deve ser maior que zero")
        return v
    
    @field_validator("quantity")
    def validate_quantity(cls, v):
        if not v:
            raise ValueError("A quantidade do lote é obrigatorio")
        
        if v <= 0:
            raise ValueError("A quantidade do lote deve ser maior que zero")
        return v
    
class LoteProductUpdate(CustomBaseModel):
    """
    Essa classe serve para atualizar um registro de "LoteProduct" no banco de dados

    - Attributes:
        - id: int (O id do lote do produto)
        - validity: date
        - quantity: float
    """
    id: int | None = None
    validity: date | None = None
    quantity: float | None = None
    
    @field_validator("id")
    def validate_id(cls, v):
        if not v:
            raise ValueError("O id do lote do produto é obrigatorio")
        
        if v <= 0:
            raise ValueError("O id do lote do produto deve ser maior que zero")
        return v
    
    @model_validator(mode="before")
    def anything(cls, values):
        validity = values.get("validity")
        quantity = values.get("quantity")
        
        if (
            not validity and
            not quantity
        ):
            raise ValueError("Nenhum campo foi preenchido para atualização")
        return values

    
class ProductResponse(CustomBaseModel):
    """
    Essa classe serve para retornar um registro de "Product" do banco de dados
    
    - Attributes:
        - id: int | None = None (O id do produto)
        - name: str | None = None
        - price_cost: float | None = None
        - price_sale: float | None = None
        - measure: int | None = None
        - image_path: str | None = None
        - description: str | None = None
        - mark: str | None = None
        - quantity: float | None = None
        - min_quantity: float | None = None
    """
    id: int | None = None
    name: str | None = None
    price_cost: float | None = None
    price_sale: float | None = None
    measure: int | None = None
    image_path: str | None = None
    description: str | None = None
    mark: str | None = None
    quantity: float | None = None
    min_quantity: float | None = None
    

class LoteProductResponse(CustomBaseModel):
    '''
    Essa classe serve para retornar um registro de "LoteProduct" do banco de dados
    - lote_id: int
    - product_id:int
    - validity: date | None = None
    - quantity: float
    '''

    lote_id: int
    product_id:int
    validity: date | None = None
    quantity: float