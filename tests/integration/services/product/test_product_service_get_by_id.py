import pytest

from app.core.errors import NotFoundError
from app.core.constants import messages
from app.schemas import ProductRequest
from app.services import ProductService


async def test_product_service_get_by_id(
    mock_db_session, mock_product_request_with_no_recipe
):
    request = ProductRequest(**mock_product_request_with_no_recipe)
    service = ProductService(mock_db_session)

    on_db = await service.add(request, "test.png")

    response = await service.get_by_id(on_db.id)
   
    assert on_db == response


async def test_product_service_get_by_id_not_found(
    mock_db_session, mock_product_request_with_no_recipe
):
    request = ProductRequest(**mock_product_request_with_no_recipe)
    service = ProductService(mock_db_session)

    on_db = await service.add(request, "test.png")

    with pytest.raises(NotFoundError) as e:

        await service.get_by_id("1")

    assert e.value.status_code == 404
    assert e.value.detail == messages.ERROR_DATABASE_PRODUCT_NOT_FOUND