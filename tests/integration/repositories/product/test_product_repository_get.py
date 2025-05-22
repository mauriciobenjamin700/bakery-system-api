import pytest

from app.core.constants import messages
from app.core.errors import ConflictError
from app.db.models import ProductModel
from app.db.repositories import ProductRepository
from app.schemas import ProductRequest


@pytest.mark.parametrize("get_all", [False, True])
async def test_product_repository_get_success(
    mock_db_session, mock_product_request_with_no_recipe, get_all
):

    repository = ProductRepository(db_session=mock_db_session)
    request = ProductRequest(**mock_product_request_with_no_recipe)
    product, _, _ = repository.map_product_request_to_model(
        request, "image.jpg"
    )

    on_db = await repository.add(product)

    if not get_all:

        find = await repository.get(product_id=on_db.id)
        assert isinstance(find, ProductModel)
        assert find == on_db

    else:

        find = await repository.get()
        assert isinstance(find, list)
        assert len(find) == 1
        assert find[0] == on_db


@pytest.mark.parametrize("get_all", [False, True])
async def test_product_repository_get_not_found(
    mock_db_session, mock_product_request_with_no_recipe, get_all
):
    repository = ProductRepository(db_session=mock_db_session)
    request = ProductRequest(**mock_product_request_with_no_recipe)
    product, _, _ = repository.map_product_request_to_model(
        request, "image.jpg"
    )

    if not get_all:

        await repository.add(product)

        find = await repository.get("123")
        assert find is None

    else:

        find = await repository.get()
        assert find is None
