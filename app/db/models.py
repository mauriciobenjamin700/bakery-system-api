from datetime import date, datetime

from sqlalchemy import (
    TIMESTAMP,
    Date,
    Enum,
    Float,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants.enums.ingredient import IngredientMeasureEnum
from app.core.constants.enums.user import UserRoles
from app.core.generate.ids import id_generator
from app.db.configs.base import Base


class UserModel(Base):
    """
    A class to represent a user model in the database. A user model is a representation of a user in the database.

    - Attributes:
        - name: str
        - phone: str
        - email: str
        - password: str
        - role: str

    - Attributes:
        - id: str PK,
        - name: str NOT NULL,
        - phone: str UNIQUE NOT NULL,
        - email: str UNIQUE NOT NULL,
        - password: str NOT NULL
        - role: str NOT NULL # ["user", "admin"]
        - created_at: datetime NOT NULL DEFAULT now()
        - updated_at: datetime NOT NULL DEFAULT now() ON UPDATE now()

        __tablename__: str = 'users'
    """

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=id_generator
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(Enum(UserRoles), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        default=datetime.now,
        onupdate=func.now(),
    )


class IngredientModel(Base):
    """
    - A class to represent an ingredient model in the database. An ingredient model is a representation of an ingredient in the database.

    Attributes:
        id (str): The unique identifier for the ingredient.
        name (str): The name of the ingredient.
        measure (str): The unit of measure for the ingredient.
        image_path (str | None): The path to the ingredient image.
        mark (str | None): The brand or mark of the ingredient.
        description (str | None): A description of the ingredient.
        value (float): The value of the ingredient.
        min_quantity (float): The minimum quantity of the ingredient.
        created_at (datetime): The date and time when the ingredient was created.
        updated_at (datetime): The date and time when the ingredient was last updated.
        ingredients_batch (list[IngredientBatchModel]): A list of ingredient batches associated with the ingredient.
    """

    __tablename__ = "ingredients"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=id_generator
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    measure: Mapped[str] = mapped_column(
        Enum(IngredientMeasureEnum), nullable=False
    )
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    mark: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    min_quantity: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        default=datetime.now,
        onupdate=datetime.now,
    )

    ingredients_batch = relationship(
        "IngredientBatchModel",
        back_populates="ingredient",
        uselist=True,
        cascade="all, delete-orphan",
    )
    portions = relationship(
        "PortionModel",
        back_populates="ingredient",
        uselist=True,
        cascade="all, delete-orphan",
    )


class IngredientBatchModel(Base):
    """
    - A class to represent an ingredient batch model in the database. An ingredient batch model is a representation of an ingredient batch in the database.

    Attributes:
        id (str): The unique identifier for the ingredient batch.
        ingredient_id (str): The unique identifier for the ingredient.
        validity (date): The date when the ingredient batch is valid until.
        quantity (float): The quantity of the ingredient batch.
        created_at (datetime): The date and time when the ingredient batch was created.
        updated_at (datetime): The date and time when the ingredient batch was last updated.
        ingredient (IngredientModel): The ingredient associated with the ingredient batch.
    """

    __tablename__ = "ingredients_batch"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=id_generator
    )
    ingredient_id: Mapped[str] = mapped_column(
        String, ForeignKey("ingredients.id"), nullable=False
    )
    validity: Mapped[date] = mapped_column(TIMESTAMP, nullable=True)
    quantity: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        default=datetime.now,
        onupdate=func.now(),
    )

    ingredient = relationship(
        "IngredientModel", back_populates="ingredients_batch"
    )


class ProductModel(Base):
    """
    A class to represent a product model in the database. A product model is a representation of a product in the database.

    Attributes:
        id (str): The unique identifier for the product.
        name (str): The name of the product.
        price_cost (float): The cost price of the product.
        price_sale (float): The sale price of the product.
        measure (str): The unit of measure for the product.
        image_path (str): The path to the product image.
        description (str): A description of the product.
        mark (str): The brand or mark of the product.
        min_quantity (float): The minimum quantity of the product.
        created_at (datetime): The date and time when the product was created.
        updated_at (datetime): The date and time when the product was last updated.

    """

    __tablename__ = "products"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=id_generator
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    price_cost: Mapped[float] = mapped_column(Float, default=0)
    price_sale: Mapped[float] = mapped_column(Float, nullable=False)
    measure: Mapped[str] = mapped_column(
        Enum(IngredientMeasureEnum), nullable=False
    )
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    mark: Mapped[str] = mapped_column(String, nullable=True)
    min_quantity: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        default=datetime.now,
        onupdate=func.now(),
    )

    products_batch = relationship(
        "ProductBatchModel",
        back_populates="product",
        uselist=True,
        cascade="all, delete-orphan",
    )
    portions = relationship(
        "PortionModel",
        back_populates="product",
        uselist=True,
        cascade="all, delete-orphan",
    )


class PortionModel(Base):
    """
    A class to represent a portion model in the database. A portion model is a representation of a portion used in a recipe to make a product.

    Attributes:
        id (str): The unique identifier for the portion.
        ingredient_id (str): The unique identifier for the ingredient.
        quantity (float): The quantity of the ingredient in the portion.
        product_id (str): The unique identifier for the product.
        ingredient (IngredientModel): The ingredient associated with the portion.
        product (ProductModel): The product associated with the portion.
    """

    __tablename__ = "portions"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=id_generator
    )
    ingredient_id: Mapped[int] = mapped_column(
        String, ForeignKey("ingredients.id"), nullable=False
    )
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    product_id: Mapped[int] = mapped_column(
        String, ForeignKey("products.id"), nullable=False
    )

    ingredient = relationship(
        "IngredientModel", back_populates="portions", uselist=False
    )
    product = relationship(
        "ProductModel", back_populates="portions", uselist=False
    )


class ProductBatchModel(Base):
    """
    A class to represent a product batch model in the database. A product batch model is a representation of a product batch in the database.

    Attributes:
        id (str): The unique identifier for the product batch.
        product_id (str): The unique identifier for the product.
        validity (date): The date when the product batch is valid until.
        quantity (float): The quantity of the product batch.
        created_at (datetime): The date and time when the product batch was created.
        updated_at (datetime): The date and time when the product batch was last updated.
        product (ProductModel): The product associated with the product batch.
    """

    __tablename__ = "products_batch"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=id_generator
    )
    product_id: Mapped[str] = mapped_column(
        String, ForeignKey("products.id"), nullable=False
    )
    validity: Mapped[date] = mapped_column(Date, nullable=True)
    quantity: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        default=datetime.now,
        onupdate=func.now(),
    )
    product = relationship(
        "ProductModel", back_populates="products_batch", uselist=False
    )
