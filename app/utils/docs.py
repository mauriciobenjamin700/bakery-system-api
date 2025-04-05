from fastapi import Response
from json import (
    dumps,
    loads
)
from typing import Literal


def generate_response(status_code: Literal[200,400,401,404,409,500], detail: str ) -> Response:
    """
    Generate a response object for FastAPI.
    """
    content = dumps({"detail": detail})
    response =  Response(status_code=status_code, content=content, media_type="application/json")
    return response


def generate_responses_documentation(responses_list: list[Response]) -> dict:
    """
    Gera uma estrutura de respostas para FastAPI a partir de uma lista de objetos Response.

    :param responses_list: Lista de objetos Response.
    :return: Dicionário formatado para o parâmetro `responses` do FastAPI.
    """
    responses = {}
    for response in responses_list:
        status_code = response.status_code
        content = response.body if response.body else {"detail": "Success"}
        if status_code not in responses:
            responses[status_code] = {
                "description": "Erro" if status_code >= 400 else "Sucesso",
                "content": {
                    "application/json": {
                        "examples": {}
                    }
                }
            }


        dict_content = loads(content.decode("utf-8"))
        detail = dict_content.get("detail", "Success")
        example_key = detail.lower().replace(" ", "_")
        responses[status_code]["content"]["application/json"]["examples"][example_key] = {
            "summary": detail,
            "value": dict_content
        }

    return responses
