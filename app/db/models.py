from datetime import datetime
from sqlalchemy import (
    Enum,
    func,
    String,
    TIMESTAMP
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

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
