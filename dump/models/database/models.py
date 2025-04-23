from datetime import date,datetime

from src.models.database.base import Base
from sqlalchemy import String, Integer, ForeignKey, Date, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column

class User(Base):
    """
    # Tabela de Usuários no Banco de Dados
    
    Atributes:
        - login: str
        - password: str
        - level: int
    """
    __tablename__ = "user"

    login:Mapped[str] = mapped_column(String,primary_key=True,unique=True)
    password:Mapped[str] = mapped_column(String,nullable=False)
    level:Mapped[int] = mapped_column(Integer,nullable=False)


class Ingredient(Base):
    """
    - Attributes:
        - id: int
        - name: str
        - measure: int
        - image_path: str
        - mark: str
        - description: str
    """
    __tablename__ = "ingredient"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String, nullable=False)
    measure:Mapped[int] = mapped_column(Integer, nullable=False)
    image_path:Mapped[str] = mapped_column(String, nullable=True)
    mark:Mapped[str] = mapped_column(String, nullable=True)
    description:Mapped[str] = mapped_column(String, nullable=True)
    value:Mapped[float] = mapped_column(Float, nullable=False)
    min_quantity: Mapped[float] = mapped_column(Float, default=0)

    lote_ingredient = relationship("LoteIngredient",back_populates="ingredient", uselist=True, cascade="all, delete-orphan")
    portion = relationship("Portion", back_populates="ingredient", uselist=True, cascade="all, delete-orphan")


class LoteIngredient(Base):
    """
    - Attributes:
        - id: int
        - id_ingredient: int
        - validity: date
        - quantity: float
        - register_date: datetime   
    """
    __tablename__ = "lote_ingredient"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_ingredient:Mapped[int] = mapped_column(Integer, ForeignKey("ingredient.id", ondelete="CASCADE"), nullable=False)
    validity:Mapped[date] = mapped_column(Date,nullable=True)
    quantity:Mapped[float] = mapped_column(Float, default=0)
    register_date:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    ingredient = relationship("Ingredient", back_populates="lote_ingredient")

class Product(Base):
    """
    - Attributes:
        - id: int
        - name: str
        - price_cost: float
        - price_sale: float
        - measure: int
        - image_path: str
        - description: str
        - mark: str
    """
    __tablename__ = "product"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String,nullable=False)
    price_cost:Mapped[float] = mapped_column(Float, default=0)
    price_sale:Mapped[float] = mapped_column(Float, default=0)
    measure:Mapped[int] = mapped_column(Integer, nullable=False)
    image_path:Mapped[str] = mapped_column(String, nullable=True)
    description:Mapped[str] = mapped_column(String, nullable=True)
    mark:Mapped[str] = mapped_column(String, nullable=True)
    min_quantity:Mapped[float] = mapped_column(Float, default=0)

    recipe = relationship("Recipe", back_populates="product", uselist=False, cascade="all, delete-orphan")
    lote_product = relationship("LoteProduct", back_populates="product", uselist=True, cascade="all, delete-orphan")


class LoteProduct(Base):
    """
    - Attributes
        - id: int
        - register_date: datetime
        - product_id: int
        - quantity: float
        - validity: date
        - min_quantity: float
    """
    __tablename__ = "lote_product"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id:Mapped[int] = mapped_column(Integer, ForeignKey("product.id"), nullable=False)
    validity:Mapped[date] = mapped_column(Date, nullable=True)
    quantity:Mapped[float] = mapped_column(Float, default=0)
    register_date:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    product = relationship("Product", back_populates="lote_product", uselist=False)


class Recipe(Base):
    """
    - Attributes:
        - id: int
        - id_product: int
    """
    __tablename__ = "recipe"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_product:Mapped[int] = mapped_column(Integer,ForeignKey("product.id"), nullable=False)

    portion = relationship("Portion", back_populates="recipe", uselist=True, cascade="all, delete-orphan")
    product = relationship("Product", back_populates="recipe", uselist=False)


class Portion(Base):
    """
    - Aattributes:
        - id: int
        - id_ingredient: int
        - id_recipe: int
        - quantity
    """
    __tablename__ = "portion"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_ingredient:Mapped[int] = mapped_column(Integer, ForeignKey("ingredient.id", ondelete="CASCADE"), nullable=False)
    id_recipe:Mapped[int] = mapped_column(Integer, ForeignKey("recipe.id", ondelete="CASCADE"), nullable=False)
    quantity:Mapped[float] = mapped_column(Float, nullable=False)
    ingredient_name:Mapped[str] = mapped_column(String, nullable=False)

    ingredient = relationship("Ingredient", back_populates="portion", uselist=False)
    recipe = relationship("Recipe", back_populates="portion",uselist=False)



class SaleNote(Base):
    """
    - Attributes:
        - id: int
        - total_value: float
        - sale_time: datetime
    """
    __tablename__ = "sale_note"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    total_value:Mapped[Float] = mapped_column(Float, nullable=False)
    sale_time:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    product_sale = relationship("ProductSale", back_populates="sale_note", uselist=True, cascade="all, delete-orphan")

class ProductSale(Base):
    """
    - Attributes:
        - id: int
        - id_sale_note: int
        - id_product: int
        - product_name: str
        - quantity: float
        - unit_cost: float
    """
    __tablename__ = "product_sale"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_sale_note:Mapped[int] = mapped_column(Integer, ForeignKey("sale_note.id"), nullable=False)
    id_product:Mapped[int] = mapped_column(Integer, nullable=False)
    product_name:Mapped[str] = mapped_column(String, nullable=False)
    quantity:Mapped[float] = mapped_column(Float, nullable=False)
    unit_cost:Mapped[float] = mapped_column(Float, nullable=False)

    sale_note = relationship("SaleNote", back_populates="product_sale", uselist=False)

def create_entities(engine) -> bool:
    """
    Cria no banco todas as entidades necessárias para o sistema
    """
    try:
        Base.metadata.create_all(engine)
        return True
    except Exception as e:
        print(f"Erro ao criar entidades: {e}")
        return False