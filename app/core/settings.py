from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    A class to represent the settings of the application.

    Attributes:
        DB_URL (str): The database URL.
        DB_USER (str): The database user.
        DB_PASSWORD (str): The database password.
        DB_NAME (str): The database name.
        TEST_DB_URL (str): The test database URL.
    """

    DB_URL: str = Field(
        title="URL do banco de dados",
        description="URL do banco de dados",
        default="postgresql://user:password@localhost:5432/database",
    )
    DB_USER: str = Field(
        title="Usuário do banco de dados",
        description="Usuário do banco de dados",
        default="user",
    )
    DB_PASSWORD: str = Field(
        title="Senha do banco de dados",
        description="Senha do banco de dados",
        default="password",
    )
    DB_NAME: str = Field(
        title="Nome do banco de dados",
        description="Nome do banco de dados",
        default="database",
    )
    TEST_DB_URL: str = Field(
        title="URL do banco de dados de teste",
        description="URL do banco de dados de teste",
        default="sqlite+aiosqlite:///:memory:",
    )
    TOKEN_ALGORITHM: str = Field(
        title="Algoritmo de criptografia do token",
        description="Algoritmo de criptografia do token",
        default="HS256",
    )
    TOKEN_EXPIRES_IN_MINUTES: int = Field(
        title="Tempo de expiração do token",
        description="Tempo de expiração do token",
        default=60,
    )
    TOKEN_SECRET_KEY: str = Field(
        title="Chave secreta do token",
        description="Chave secreta do token",
        default="your_secret_key",
    )

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


config = Settings()
