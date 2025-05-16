from datetime import datetime

from fastapi.testclient import TestClient
from pytest import fixture

from app.core.constants.enums.ingredient import IngredientMeasureEnum
from app.core.constants.enums.user import UserRoles
from app.core.security.password import hash_password
from app.core.settings import config
from app.db.configs.connection import AsyncDatabaseManager
from app.main import app


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
        "measure": IngredientMeasureEnum.KG.value,
        "image_path": "https://example.com/tomato.jpg",
        "mark": "Fresh",
        "description": "Fresh and ripe tomatoes",
        "value": 3.5,
        "min_quantity": 10,
    }
