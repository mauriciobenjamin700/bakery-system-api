from datetime import date, datetime
from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Text,
    func,
    String,
    TIMESTAMP
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.constants.enums.ingredient import IngredientMeasureEnum
from app.core.constants.enums.user import UserRoles
from app.core.generate.ids import id_generator
from app.db.configs.base import Base


class UserModel(Base):
    """
    A class to represent a user model in the database. A user model is a representation of a user in the database.

    - Args:
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
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=id_generator)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(Enum(UserRoles), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())


class IngredientModel(Base):
    """
    - A class to represent an ingredient model in the database. An ingredient model is a representation of an ingredient in the database.
    - Args:
        - name: str
        - measure: str
        - image_path: str
        - description: str
        - mark: str
        - value: float
        - min_quantity: float
    - Attributes:
        - id: str
        - name: str
        - measure: str
        - image_path: str
        - description: str
        - mark: str
        - value: float
        - min_quantity: float
        - created_at: datetime
        - updated_at: datetime
    - Relationships:
        - lote_ingredient: list[LoteIngredientModel]
        - portion: list[PortionModel]
    """
    __tablename__ = "ingredient"

    id:Mapped[str] = mapped_column(String, primary_key=True, default_factory=id_generator)
    name:Mapped[str] = mapped_column(String, nullable=False)
    measure:Mapped[str] = mapped_column(Enum(IngredientMeasureEnum), nullable=False)
    image_path:Mapped[str] = mapped_column(String, nullable=True)
    mark:Mapped[str] = mapped_column(String, nullable=True)
    description:Mapped[str] = mapped_column(String, nullable=True)
    value:Mapped[float] = mapped_column(Float, nullable=False)
    min_quantity: Mapped[float] = mapped_column(Float, default=0)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now, onupdate=func.now)

    lote_ingredient = relationship("LoteIngredientModel",back_populates="ingredient", uselist=True, cascade="all, delete-orphan")
    portion = relationship("PortionModel", back_populates="ingredient", uselist=True, cascade="all, delete-orphan")


class LoteIngredientModel(Base):
    """
    - A class to represent a lote ingredient model in the database. A lote ingredient model is a representation of a lote ingredient in the database.
    - Args:
        - ingredient_id: str
        - validity: date
        - quantity: float
    - Attributes:
        - id: str
        - ingredient_id: str
        - validity: date
        - quantity: float
        - created_at: datetime
        - updated_at: datetime
    - Relationships:
        - ingredient: IngredientModel
    """
    __tablename__ = "lote_ingredient"

    id:Mapped[str] = mapped_column(String, primary_key=True, default_factory=id_generator)
    ingredient_id:Mapped[str] = mapped_column(String, ForeignKey("ingredient.id", ondelete="CASCADE"), nullable=False)
    validity:Mapped[date] = mapped_column(Date,nullable=True)
    quantity:Mapped[float] = mapped_column(Float, default=0)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now, onupdate=func.now)

    ingredient = relationship("IngredientModel", back_populates="lote_ingredient")


class PortionModel(Base):
    """
    A class to represent a portion model in the database. A portion model is a representation of a portion in the database.
    - Args:
        - ingredient_id: str
        - quantity: float
    - Attributes:
        - id: str
        - ingredient_id: str
        - quantity: float
    - Relationships:
        - ingredient: IngredientModel
    """
    __tablename__ = "portion"

    id:Mapped[str] = mapped_column(String, primary_key=True, default_factory=id_generator)
    ingredient_id:Mapped[int] = mapped_column(String, ForeignKey("ingredient.id", ondelete="CASCADE"), nullable=False)
    quantity:Mapped[float] = mapped_column(Float, nullable=False)

    ingredient = relationship("Ingredient", back_populates="portion", uselist=False)
    

class ProductModel(Base):
    """
    - A class to represent a product model in the database. A product model is a representation of a product in the database.
    - Args:
        - name: str
        - price_cost: float
        - price_sale: float
        - measure: str
        - image_path: str
        - description: str
        - mark: str
        - min_quantity: float
    - Attributes:
        - id: str
        - name: str
        - price_cost: float
        - price_sale: float
        - measure: str
        - image_path: str
        - description: str
        - mark: str
        - min_quantity: float
        - created_at: datetime
        - updated_at: datetime
    - Relationships:
        - lote_product: list[LoteProductModel]
    """
    __tablename__ = "product"

    id:Mapped[str] = mapped_column(String, primary_key=True, default_factory=id_generator)
    name:Mapped[str] = mapped_column(String,nullable=False)
    price_cost:Mapped[float] = mapped_column(Float, default=0)
    price_sale:Mapped[float] = mapped_column(Float, default=0)
    measure:Mapped[str] = mapped_column(Enum(IngredientMeasureEnum), nullable=False)
    image_path:Mapped[str] = mapped_column(String, nullable=True)
    description:Mapped[str] = mapped_column(Text, nullable=True)
    mark:Mapped[str] = mapped_column(String, nullable=True)
    min_quantity:Mapped[float] = mapped_column(Float, default=0)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now, onupdate=func.now)

    # Gerar a receita mediante as porcões
    #recipe = relationship("Recipe", back_populates="product", uselist=False, cascade="all, delete-orphan")
    lote_product = relationship("LoteProductModel", back_populates="product", uselist=True, cascade="all, delete-orphan")


class LoteProductModel(Base):
    """
    - A class to represent a lote product model in the database. A lote product model is a representation of a lote product in the database.
    - Args:
        - product_id: str
        - validity: date
        - quantity: float
    - Attributes
        - id: str
        - product_id: str
        - validity: date
        - quantity: float
        - created_at: datetime
        - updated_at: datetime
    - Relationships:
        - product: ProductModel
    """
    __tablename__ = "lote_product"

    id:Mapped[str] = mapped_column(String, primary_key=True, default_factory=id_generator)
    product_id:Mapped[str] = mapped_column(String, ForeignKey("product.id"), nullable=False)
    validity:Mapped[date] = mapped_column(Date, nullable=True)
    quantity:Mapped[float] = mapped_column(Float, default=0)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now, onupdate=func.now)

    product = relationship("ProductModel", back_populates="lote_product", uselist=False)
