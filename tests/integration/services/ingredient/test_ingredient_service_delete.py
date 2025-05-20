from app.core.constants.messages import MESSAGE_INGREDIENT_DELETE_SUCCESS
from app.schemas import IngredientRequest
from app.services import IngredientService


async def test_ingredient_service_add_success(
    mock_db_session, mock_ingredient_request
):

    request = IngredientRequest(**mock_ingredient_request)
    service = IngredientService(mock_db_session)

    on_db = await service.add(request, "test.png")

    result = await service.delete(on_db.id)

    assert result.detail == MESSAGE_INGREDIENT_DELETE_SUCCESS
