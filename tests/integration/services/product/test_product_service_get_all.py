import pytest

from app.core.errors import NotFoundError
from app.core.constants import messages
from app.schemas import ProductRequest
from app.services import ProductService


async def test_product_service_get_all(
    mock_db_session, mock_product_request_with_no_recipe
):
    request = ProductRequest(**mock_product_request_with_no_recipe)
    service = ProductService(mock_db_session)

    on_db = await service.add(request, "test.png")

    response = await service.get_all()
   
    assert isinstance(response, list)
    assert len(response) == 1
    response = response[0]
    assert on_db == response


async def test_product_service_get_all_not_found(
    mock_db_session, mock_product_request_with_no_recipe
):
    request = ProductRequest(**mock_product_request_with_no_recipe)
    service = ProductService(mock_db_session)

    with pytest.raises(NotFoundError) as e:

        await service.get_all()

    assert e.value.status_code == 404
    assert e.value.detail == messages.ERROR_DATABASE_PRODUCTS_NOT_FOUND