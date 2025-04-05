from pydantic import Field


from app.schemas.settings.base import BaseSchema


class Message(BaseSchema):
    detail: str = Field(
        title="Detalhes da mensagem",
        examples=["Mensagem enviada com sucesso"],
        description="Mensagem contendo detalhes sobre a requisição realizada"
    )
