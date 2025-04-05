from src.models.schemas.base import CustomBaseModel

class PortionRequest(CustomBaseModel):
    """
    Essa classe serve para inserir um registro de "Portion" no banco de dados.

    - Attributes:
        - id_ingredient: int
        - id_recipe: int
        - quantity: float
    """
    id_ingredient: int | None = None
    id_recipe: int | None = None
    quantity: float | None = None

class PortionResponse(CustomBaseModel):
    """
    Essa classe serve para retornar um registro de "Portion" do banco de dados.
    
    - Attributes:
        - id:int (O id da portion)
        - id_ingredient:int
        - id_recipe:int
        - quantity:float
        - ingredient_name:str
    """
    id:int
    id_ingredient:int
    id_recipe:int
    quantity:float
    ingredient_name:str