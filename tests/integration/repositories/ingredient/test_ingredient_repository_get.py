import pytest

from app.db.models import IngredientModel, UserModel
from app.db.repositories import IngredientRepository


@pytest.mark.parametrize(
    ["field", "all_results", "result_type"],
    [
        ("name", True, list),
        ("id", False, UserModel),
        ("name", False, UserModel),
    ],
)
async def test_ingredient_repository_get(
    mock_db_session, mock_ingredient_model, field, all_results, result_type
):

    # Arrange

    repository = IngredientRepository(mock_db_session)

    model = IngredientModel(**mock_ingredient_model)

    on_db = await repository.add(model)

    if field == "name":
        result = await repository.get(name=on_db.name, all_results=all_results)
    elif field == "id":
        result = await repository.get(id=on_db.id, all_results=all_results)

    assert result is not None
