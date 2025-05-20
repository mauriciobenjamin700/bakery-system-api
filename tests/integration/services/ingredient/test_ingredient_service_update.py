import pytest

from app.core.constants.messages import ERROR_DATABASE_INGREDIENT_NOT_FOUND
from app.core.errors import NotFoundError
from app.schemas import IngredientRequest, IngredientResponse, IngredientUpdate
from app.services import IngredientService


async def test_ingredient_service_update_success(
    mock_db_session, mock_ingredient_request, mock_ingredient_update
):

    request = IngredientRequest(**mock_ingredient_request)
    service = IngredientService(mock_db_session)

    on_db = await service.add(request, "test.png")

    update = IngredientUpdate(**mock_ingredient_update)

    response = await service.update(on_db.id, update)

    assert isinstance(response, IngredientResponse)
    assert response != on_db
    assert response.id == on_db.id
    assert response.name == update.name
    assert response.measure == update.measure
    assert response.mark == update.mark
    assert response.description == update.description
    assert response.value == update.value
    assert response.min_quantity == update.min_quantity


async def test_ingredient_service_update_not_found(
    mock_db_session, mock_ingredient_request
):

    request = IngredientRequest(**mock_ingredient_request)
    service = IngredientService(mock_db_session)

    await service.add(request, "test.png")

    with pytest.raises(NotFoundError) as e:
        await service.get_by_id("non_existent_id")

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_DATABASE_INGREDIENT_NOT_FOUND
