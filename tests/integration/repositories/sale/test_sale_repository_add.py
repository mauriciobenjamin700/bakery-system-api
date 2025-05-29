import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import messages
from app.core.errors import NotFoundError
from app.core.generate.ids import code_generator
from app.db.models import SaleModel, UserModel
from app.db.repositories import SaleRepository
from app.schemas import ProductRequest, ProductResponse, SaleRequest
from app.services import ProductService


async def test_sale_repository_add_sale_success(
    mock_db_session: AsyncSession,
    mock_user_on_db: UserModel,
    mock_product_request_with_no_recipe,
):

    repository = SaleRepository(mock_db_session)

    product_service = ProductService(mock_db_session)

    product_request = ProductRequest(**mock_product_request_with_no_recipe)

    product: ProductResponse = await product_service.add(
        product_request, "test.jpg"
    )

    sale_request = SaleRequest(
        product_id=product.id, user_id=mock_user_on_db.id, quantity=5
    )

    sale_code = code_generator()

    model = await repository.map_request_to_model(sale_request, sale_code)

    sale_response = await repository.add(model)

    assert isinstance(sale_response, SaleModel)
    assert sale_response.product_id == product.id
    assert sale_response.user_id == mock_user_on_db.id
    assert sale_response.quantity == 5
    assert sale_response.id is not None
    assert sale_response.is_paid is False
    assert sale_response.quantity == sale_request.quantity
    assert sale_response.value == product.price_sale * sale_response.quantity
    assert sale_response.sale_code == sale_code
    assert sale_response.created_at is not None


async def test_sale_repository_add_sale_with_all_products_in_stock(
    mock_db_session: AsyncSession,
    mock_user_on_db: UserModel,
    mock_product_request_with_no_recipe,
):

    repository = SaleRepository(mock_db_session)

    product_service = ProductService(mock_db_session)

    product_request = ProductRequest(**mock_product_request_with_no_recipe)

    product: ProductResponse = await product_service.add(
        product_request, "test.jpg"
    )

    sale_request = SaleRequest(
        product_id=product.id,
        user_id=mock_user_on_db.id,
        quantity=product.quantity,
    )

    sale_code = code_generator()

    model = await repository.map_request_to_model(sale_request, sale_code)

    sale_response = await repository.add(model)

    assert isinstance(sale_response, SaleModel)
    assert sale_response.product_id == product.id
    assert sale_response.user_id == mock_user_on_db.id
    assert sale_response.quantity == product.quantity
    assert sale_response.id is not None
    assert sale_response.is_paid is False
    assert sale_response.value == product.price_sale * sale_response.quantity

    product_after_sale = await product_service.get_by_id(product.id)

    assert product_after_sale.quantity == 0
    assert product_after_sale.batches is None


async def test_sale_repository_add_sale_product_not_found_in_map(
    mock_db_session: AsyncSession, mock_user_on_db: UserModel
):

    repository = SaleRepository(mock_db_session)

    sale_request = SaleRequest(
        product_id="non_existent_product_id",
        user_id=mock_user_on_db.id,
        quantity=5,
    )

    sale_code = code_generator()

    with pytest.raises(NotFoundError) as e:
        await repository.map_request_to_model(sale_request, sale_code)

    assert e.value.detail == messages.ERROR_DATABASE_PRODUCT_NOT_FOUND
    assert e.value.status_code == 404


async def test_sale_repository_add_sale_product_not_found(
    mock_db_session: AsyncSession,
    mock_user_on_db: UserModel,
):

    repository = SaleRepository(mock_db_session)

    model = SaleModel(
        product_id="non_existent_product_id",
        user_id=mock_user_on_db.id,
        is_paid=False,
        quantity=5,
        value=100.0,
        sale_code=code_generator(),
    )

    with pytest.raises(NotFoundError) as e:
        await repository.add(model)

    assert e.value.detail == messages.ERROR_DATABASE_PRODUCT_NOT_FOUND
    assert e.value.status_code == 404


async def test_sale_repository_add_sale_user_not_found(
    mock_db_session: AsyncSession, mock_product_request_with_no_recipe
):

    repository = SaleRepository(mock_db_session)

    product_service = ProductService(mock_db_session)

    product_request = ProductRequest(**mock_product_request_with_no_recipe)

    product: ProductResponse = await product_service.add(
        product_request, "test.jpg"
    )

    sale_request = SaleRequest(
        product_id=product.id, user_id="non_existent_user_id", quantity=5
    )

    model = await repository.map_request_to_model(
        sale_request, code_generator()
    )

    with pytest.raises(NotFoundError) as e:
        await repository.add(model)

    assert e.value.detail == messages.ERROR_DATABASE_USER_NOT_FOUND
    assert e.value.status_code == 404


async def test_sale_repository_add_sale_with_not_enough_quantity(
    mock_db_session: AsyncSession,
    mock_user_on_db: UserModel,
    mock_product_request_with_no_recipe,
):

    repository = SaleRepository(mock_db_session)

    product_service = ProductService(mock_db_session)

    product_request = ProductRequest(**mock_product_request_with_no_recipe)

    product: ProductResponse = await product_service.add(
        product_request, "test.jpg"
    )

    sale_request = SaleRequest(
        product_id=product.id, user_id=mock_user_on_db.id, quantity=1000
    )

    model = await repository.map_request_to_model(
        sale_request, code_generator()
    )

    with pytest.raises(NotFoundError) as e:
        await repository.add(model)

    assert e.value.detail == messages.ERROR_NOT_ENOUGH_PRODUCT_IN_STOCK
    assert e.value.status_code == 404
