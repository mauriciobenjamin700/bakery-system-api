from datetime import datetime

from pytest import fixture

from app.core.constants.enums.base import MeasureEnum
from app.core.constants.enums.user import UserRoles
from app.core.security.password import hash_password
from app.core.settings import config
from app.db.configs.connection import AsyncDatabaseManager
from app.db.models import UserModel
from app.utils.validators.strings import parse_phone


@fixture
async def mock_db_session():
    test_db = AsyncDatabaseManager(config.TEST_DB_URL)
    test_db.connect()
    await test_db.create_tables()
    session = await test_db.get_session()
    yield session
    await test_db.drop_tables()
    await session.close()


@fixture
def mock_user_request():
    return {
        "name": "John Doe",
        "phone": "(89) 91111-2222",
        "email": "jhon.doe@gmail.com",
        "password": "SafePassword123@",
    }


@fixture
def mock_user_model():
    return {
        "name": "John Doe",
        "phone": "(89) 91111-2222",
        "email": "jhon.doe@gmail.com",
        "password": hash_password("SafePassword123@"),
        "role": UserRoles.USER.value,
    }


@fixture
def mock_user_response():
    return {
        "id": "1",
        "name": "John Doe",
        "phone": "89911112222",
        "email": "jhon.doe@gmail.com",
        "role": UserRoles.USER.value,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


@fixture
def mock_ingredient_model():
    return {
        "name": "Tomato",
        "measure": MeasureEnum.KG.value,
        "image_path": "https://example.com/tomato.jpg",
        "mark": "Fresh",
        "description": "Fresh and ripe tomatoes",
        "value": 3.5,
        "min_quantity": 10,
    }


@fixture
def mock_ingredient_request():
    return {
        "name": "Tomato",
        "measure": MeasureEnum.KG.value,
        "mark": "Fresh",
        "description": "Fresh and ripe tomatoes",
        "value": 3.5,
        "min_quantity": 10,
        "quantity": 20,
    }


@fixture
def mock_list_ingredient_request():
    return [
        {
            "name": "Tomato",
            "measure": MeasureEnum.KG.value,
            "mark": "Fresh",
            "description": "Fresh and ripe tomatoes",
            "value": 3.5,
            "min_quantity": 10,
            "quantity": 20,
        },
        {
            "name": "Potato",
            "measure": MeasureEnum.KG.value,
            "mark": "Fresh",
            "description": "Fresh and ripe potatoes",
            "value": 2.0,
            "min_quantity": 15,
            "quantity": 30,
        },
        {
            "name": "Rice",
            "measure": MeasureEnum.KG.value,
            "mark": "Fresh",
            "description": "Fresh and ripe potatoes",
            "value": 2.0,
            "min_quantity": 5,
            "quantity": 30,
        },
    ]


@fixture
def mock_ingredient_update():
    return {
        "name": "Tomate",
        "measure": MeasureEnum.KG.value,
        "mark": "Fresh",
        "description": "Fresh and ripe tomatoes",
        "value": 5.0,
        "min_quantity": 20,
    }


@fixture
def mock_ingredient_batch_request():
    return {
        "ingredient_id": "1",
        "quantity": 20,
        "validity": "2023-12-31",
    }


@fixture
def mock_ingredient_batch_update():
    return {
        "quantity": 30,
        "validity": "2026-01-31",
    }


@fixture
def mock_product_request_with_no_recipe():
    return {
        "name": "Test Product",
        "price_cost": 0.25,
        "price_sale": 1,
        "measure": MeasureEnum.KG.value,
        "description": "This is a test product",
        "mark": "Test Mark",
        "min_quantity": 10,
        "quantity": 20,
        "validity": "2026-12-31",
    }


@fixture
def mock_product_request_with_recipe():
    return {
        "name": "Bolo de Tomate",
        "price_cost": 10,
        "price_sale": 20,
        "measure": MeasureEnum.KG.value,
        "description": "This is a test product",
        "mark": "Test Mark",
        "min_quantity": 10,
        "quantity": 20,
        "validity": "2026-12-31",
        "recipe": [
            {
                "ingredient_id": "1",
                "quantity": 2,
            },
            {
                "ingredient_id": "2",
                "quantity": 3,
            },
        ],
    }


@fixture
def mock_product_batch_request():
    return {
        "product_id": "1",
        "quantity": 20,
        "validity": "2023-12-31",
    }


@fixture
async def mock_user_on_db(mock_db_session) -> UserModel:

    user = UserModel(
        name="On db User",
        phone=parse_phone("(89) 91111-2222"),
        email="db_user@gmail.com",
        password=hash_password("SafePassword123@"),
        role=UserRoles.USER.value,
    )

    mock_db_session.add(user)

    await mock_db_session.commit()

    return user
