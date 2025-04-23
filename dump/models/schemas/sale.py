from datetime import datetime
from pydantic import (
    field_validator
)


from src.models.schemas.base import CustomBaseModel

class ProductSaleRequest(CustomBaseModel):
    """
    Essa classe representa um produto vendido.
    Primeiro crie uma instancia de "SaleNoteResponse" e insira as instancias desta classe no atributo 
    "products" existente na classe "SaleNoteResponse".

    - Attributes:
        - product_name: str | None
        - quantity: float | None
        - unit_cost: float | None
        - id_sale_note: int | None
    """
    product_name: str | None = None 
    quantity: float | None = None
    unit_cost: float | None = None
    id_sale_note: int | None = None    
    id_product: int | None = None
    
    @field_validator("product_name")
    def validate_product_name(cls, v):
        if not v:
            raise ValueError("O nome do produto é obrigatorio")
        
        if v.strip() == "":
            raise ValueError("O nome do produto é obrigatorio")
        return v
    
    @field_validator("quantity")
    def validate_quantity(cls, v):
        if not v:
            raise ValueError("A quantidade do produto é obrigatorio")
        
        if v <= 0:
            raise ValueError("A quantidade do produto deve ser maior que zero")
        return v
    
    @field_validator("unit_cost")
    def validate_unit_cost(cls, v):
        if not v:
            raise ValueError("O custo unitario do produto é obrigatorio")
        
        if v <= 0:
            raise ValueError("O custo unitario do produto deve ser maior que zero")
        return v
    
    @field_validator("id_product")
    def validate_id_product(cls, v):
        if not v:
            raise ValueError("O id do produto é obrigatorio")
        
        if v <= 0:
            raise ValueError("O id do produto deve ser maior que zero")
        return v
    
    
    

class SaleNoteResponse(CustomBaseModel):
    """
    Essa classe funciona como uma nota fiscal, com o valor da venda, seu horario e os produtos vendidos.
    Ela funciona como response.

    - Attributes:
        - id: int (O id da Sale Note)
        - sale_time: datetime
        - total_value: float
        - products: list[ProductSaleRequest]
    """
    id: int
    sale_time: datetime
    total_value: float
    products: list[ProductSaleRequest]