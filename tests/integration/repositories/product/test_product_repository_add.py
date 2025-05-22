import pytest

from app.core.constants import messages
from app.core.errors import ConflictError
from app.db.models import ProductModel
from app.db.repositories import ProductRepository
from app.schemas import ProductRequest


async def test_product_repository_add_success(
    mock_db_session, mock_product_request_with_no_recipe
):

    repository = ProductRepository(db_session=mock_db_session)
    request = ProductRequest(**mock_product_request_with_no_recipe)
    product, _, _ = repository.map_product_request_to_model(
        request, "image.jpg"
    )

    on_db = await repository.add(product)

    assert isinstance(on_db, ProductModel)
    assert on_db.id is not None
    assert on_db.name == request.name
    assert on_db.price_cost == request.price_cost
    assert on_db.price_sale == request.price_sale
    assert on_db.measure == request.measure
    assert on_db.image_path == "image.jpg"
    assert on_db.description == request.description
    assert on_db.mark == request.mark
    assert on_db.min_quantity == request.min_quantity
    assert on_db.created_at is not None
    assert on_db.updated_at is not None


async def test_product_repository_add_fail_conflict(
    mock_db_session, mock_product_request_with_no_recipe
):

    repository = ProductRepository(db_session=mock_db_session)
    request = ProductRequest(**mock_product_request_with_no_recipe)
    product, _, _ = repository.map_product_request_to_model(
        request, "image.jpg"
    )

    await repository.add(product)

    with pytest.raises(ConflictError) as e:
        await repository.add(product)

    assert e.value.status_code == 409
    assert e.value.detail == messages.ERROR_DATABASE_PRODUCT_ALREADY_EXISTS
