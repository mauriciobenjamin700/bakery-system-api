from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str = Field(
        title="URL do banco de dados",
        description="URL do banco de dados",
        default="postgresql://user:password@localhost:5432/database"
    )
    DB_USER: str = Field(
        title="Usuário do banco de dados",
        description="Usuário do banco de dados",
        default="user"
    )
    DB_PASSWORD: str = Field(
        title="Senha do banco de dados",
        description="Senha do banco de dados",
        default="password"
    )
    DB_NAME: str = Field(
        title="Nome do banco de dados",
        description="Nome do banco de dados",
        default="database"
    )
    TEST_DB_URL: str = Field(
        title="URL do banco de dados de teste",
        description="URL do banco de dados de teste",
        default="sqlite+aiosqlite:///:memory:"
    )


    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


config = Settings()
