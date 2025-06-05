# app/core/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field # Re-adicionado Field, caso seja usado para validação ou metadados

class Settings(BaseSettings):
    """
    A class to represent the settings of the application.

    Attributes:
        DB_URL (str): The database URL.
        DB_USER (str): The database user.
        DB_PASSWORD (str): The database password.
        DB_NAME (str): The database name.
        DB_HOST (str): The database host. # Adicionado
        DB_PORT (str): The database port. # Adicionado
        TEST_DB_URL (str): The test database URL.
        TOKEN_ALGORITHM (str): The token encryption algorithm.
        TOKEN_EXPIRES_IN_MINUTES (int): The token expiration time in minutes.
        TOKEN_SECRET_KEY (str): The token secret key.
    """

    # Estas variáveis devem ser carregadas do .env
    DB_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str # Adicionado para ser carregado do .env
    DB_PORT: str # Adicionado para ser carregado do .env

    # Valores padrão para as outras variáveis
    TEST_DB_URL: str = Field(default="sqlite+aiosqlite:///:memory:")
    TOKEN_ALGORITHM: str = Field(default="HS256")
    TOKEN_EXPIRES_IN_MINUTES: int = Field(default=60)
    TOKEN_SECRET_KEY: str = Field(default="your_secret_key")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

# A instância 'config' deve ser criada APENAS no final do ficheiro.
# Isto garante que a classe Settings e todas as suas dependências estejam totalmente definidas
# antes de 'config' ser instanciado e potencialmente importado por outros módulos.
config = Settings()
