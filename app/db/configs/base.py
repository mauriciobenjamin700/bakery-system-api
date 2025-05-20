from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class to be inherited by all models. This class provides a method to convert the model to a dictionary.

    - Methods:
        - to_dict: Method to convert the model to a dictionary.
    """

    def __repr__(self) -> str:
        cls = self.__class__
        column_attrs = inspect(cls).mapper.column_attrs
        columns = {attr.key: getattr(self, attr.key) for attr in column_attrs}
        columns_str = ", ".join(
            f"{key}={value!r}" for key, value in columns.items()
        )
        return f"{cls.__name__}({columns_str})"

    def to_dict(
        self, exclude: list = [], include: dict = {}, remove_none: bool = False
    ) -> dict:
        """
        Method to convert the model to a dictionary.

        - Args:
            - exclude: list : A list of fields to exclude from the dictionary.
            - include: dict : A dictionary of fields to include in the dictionary.
            - remove_none: bool : A flag to remove None values from the dictionary.
        - Returns:
            - dict : A dictionary representation of the model.
        """
        column_attrs = inspect(self.__class__).mapper.column_attrs
        data = {attr.key: getattr(self, attr.key) for attr in column_attrs}
        data = {k: v for k, v in data.items()}

        result = {}

        for key, value in data.items():
            if key not in exclude:
                result[key] = value
            if remove_none and value is None:
                pass
            else:
                result[key] = value

        result.update(include)

        return result
