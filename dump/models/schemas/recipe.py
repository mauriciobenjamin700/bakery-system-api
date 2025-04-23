from src.models.schemas.base import CustomBaseModel

class RecipeRequest(CustomBaseModel):
    """
    Essa classe serve para interagir com um objeto do tipo "Recipe" no banco.

    - Attributes:
        - id_product: int (O id do produto)
    """
    id_product: int | None = None
class RecipeResponse(CustomBaseModel):
    """
    Essa classe serve para retornar um registro de "Recipe" no banco.
    
    - Attributes:
        - id: int (O id da receita)
        - id_product: int (O id do produto)
    """
    id: int
    id_product: int
