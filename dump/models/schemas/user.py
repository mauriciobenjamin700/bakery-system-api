from src.models.schemas.base import CustomBaseModel


class UserRequest(CustomBaseModel):
    """
    Essa classe serve para inserir um registro de "User" no banco de dados.

    Atributes:
        - login: str | None = None
        - password: str | None = None
        - level: int | None = 2

    """
    login: str | None = None
    password: str | None = None
    level: int | None = 2

    
class UserUpdate(CustomBaseModel):
    """
    Essa classe serve para atualizar um registro de "User" no banco de dados.

    Atributes:
        - login: str | None = None
        - password: str | None = None
        - level: int | None = None

    """
    login: str | None = None 
    password: str | None = None
    level: int | None = None

class UserLogin(CustomBaseModel):
    """
    Essa classe serve para realizar o login do usuario no sistema.

    Atributes:
        - login: str | None = None
        - password: str | None = None

    """
    login: str | None = None
    password: str | None = None
