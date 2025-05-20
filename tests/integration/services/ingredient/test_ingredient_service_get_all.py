import pytest

from app.core.constants.messages import (
    ERROR_DATABASE_INGREDIENT_NOT_FOUND,
    ERROR_DATABASE_INGREDIENTS_NOT_FOUND,
)
from app.core.errors import NotFoundError
from app.schemas import IngredientRequest, IngredientResponse
from app.services import IngredientService


async def test_ingredient_service_get_all_success(
    mock_db_session, mock_ingredient_request
):

    request = IngredientRequest(**mock_ingredient_request)
    service = IngredientService(mock_db_session)

    on_db = await service.add(request, "test.png")

    response = await service.get_all()

    assert isinstance(response, list)
    assert len(response) == 1
    response = response[0]
    assert isinstance(response, IngredientResponse)
    assert response == on_db


async def test_ingredient_service_get_all_not_found(mock_db_session):

    service = IngredientService(mock_db_session)

    with pytest.raises(NotFoundError) as e:
        await service.get_all()

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_DATABASE_INGREDIENTS_NOT_FOUND
