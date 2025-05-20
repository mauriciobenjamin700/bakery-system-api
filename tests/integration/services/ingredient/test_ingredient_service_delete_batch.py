from app.core.constants.messages import MESSAGE_INGREDIENT_BATCH_DELETE_SUCCESS
from app.schemas import IngredientRequest, IngredientResponse
from app.services import IngredientService


async def test_ingredient_service_delete_success(
    mock_db_session, mock_ingredient_request
):

    request = IngredientRequest(**mock_ingredient_request)
    service = IngredientService(mock_db_session)

    response = await service.add(request, "test.png")

    message = await service.delete_batch(response.batches[0].id)

    assert message.detail == MESSAGE_INGREDIENT_BATCH_DELETE_SUCCESS
