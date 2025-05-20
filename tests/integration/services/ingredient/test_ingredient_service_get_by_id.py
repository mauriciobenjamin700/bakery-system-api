import pytest

from app.core.constants.messages import ERROR_DATABASE_INGREDIENT_NOT_FOUND
from app.core.errors import NotFoundError
from app.schemas import IngredientRequest, IngredientResponse
from app.services import IngredientService


async def test_ingredient_service_get_by_id_success(
    mock_db_session, mock_ingredient_request
):

    request = IngredientRequest(**mock_ingredient_request)
    service = IngredientService(mock_db_session)

    on_db = await service.add(request, "test.png")

    response = await service.get_by_id(on_db.id)

    assert isinstance(response, IngredientResponse)
    assert response == on_db


async def test_ingredient_service_get_by_id_not_found(
    mock_db_session, mock_ingredient_request
):

    request = IngredientRequest(**mock_ingredient_request)
    service = IngredientService(mock_db_session)

    await service.add(request, "test.png")

    with pytest.raises(NotFoundError) as e:
        await service.get_by_id("non_existent_id")

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_DATABASE_INGREDIENT_NOT_FOUND
