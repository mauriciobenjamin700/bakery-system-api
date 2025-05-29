import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UserModel
from app.schemas import (
    IngredientRequest,
    ProductRequest,
    SaleNoteRequest,
    SaleRequest,
)
from app.schemas.product import ProductResponse
from app.schemas.sale import SaleNoteResponse, SaleResponse
from app.services import IngredientService, ProductService, SaleService


async def test_sale_service_add_sale_request(
    mock_db_session: AsyncSession,
    mock_user_on_db: UserModel,
    mock_product_request_with_no_recipe,
):

    product_service = ProductService(mock_db_session)
    sale_service = SaleService(mock_db_session)

    product_request = ProductRequest(**mock_product_request_with_no_recipe)

    product: ProductResponse = await product_service.add(
        product_request, "test.jpg"
    )

    sale_request = SaleRequest(
        product_id=product.id, user_id=mock_user_on_db.id, quantity=5
    )

    sale_response = await sale_service.add(sale_request)

    assert isinstance(sale_response, SaleResponse)
    assert sale_response.product_id == product.id
    assert sale_response.user_id == mock_user_on_db.id
    assert sale_response.quantity == 5
    assert sale_response.id is not None
    assert sale_response.is_paid is False
    assert sale_response.value == product.price_sale * sale_response.quantity


async def test_sale_service_add_sale_note_request(
    mock_db_session: AsyncSession,
    mock_user_on_db: UserModel,
    mock_product_request_with_no_recipe,
    mock_product_request_with_recipe,
    mock_list_ingredient_request,
):
    product_service = ProductService(mock_db_session)
    sale_service = SaleService(mock_db_session)
    ingredient_service = IngredientService(mock_db_session)

    ingredients = []

    for mock in mock_list_ingredient_request:

        ingredient_request = IngredientRequest(**mock)
        ingredient_response = await ingredient_service.add(
            ingredient_request, "test.jpg"
        )
        ingredients.append(ingredient_response)

    product_request_no_recipe = ProductRequest(
        **mock_product_request_with_no_recipe
    )
    product_no_recipe: ProductResponse = await product_service.add(
        product_request_no_recipe, "test.jpg"
    )

    product_request_with_recipe = ProductRequest(
        **mock_product_request_with_recipe
    )

    for idx, portion in enumerate(product_request_with_recipe.recipe):
        portion.ingredient_id = ingredients[idx].id

    product_with_recipe: ProductResponse = await product_service.add(
        product_request_with_recipe, "test.jpg"
    )

    sale_request = SaleNoteRequest(
        sales=[
            SaleRequest(
                product_id=product_no_recipe.id,
                user_id=mock_user_on_db.id,
                quantity=2,
            ),
            SaleRequest(
                product_id=product_with_recipe.id,
                user_id=mock_user_on_db.id,
                quantity=3,
            ),
        ]
    )

    sale_response = await sale_service.add(sale_request)

    assert isinstance(sale_response, SaleNoteResponse)
    assert len(sale_response.products) == 2
    assert sale_response.seller.id == mock_user_on_db.id
    assert len(sale_response.notes) == 2
    assert sale_response.total_value == (
        (product_no_recipe.price_sale * 2)
        + (product_with_recipe.price_sale * 3)
    )
