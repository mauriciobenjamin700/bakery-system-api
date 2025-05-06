from enum import Enum


class BaseEnum(str, Enum):
    """
    A base class for all Enums in the application. This class provides a common interface for all Enums in the application.

    - Attributes:
        - __str__: str
        - get: str
    """

    def values(self):
        """
        Returns the values of the Enum as a list.

        - Returns:
            - list: A list of the values of the Enum.
        """
        return [item.value for item in self.__class__]

    def keys(self):
        """
        Returns the keys of the Enum as a list.

        - Returns:
            - list: A list of the keys of the Enum.
        """
        return [item.name for item in self.__class__]


class MeasureEnum(BaseEnum):
    """
    Enum for product measures.

    - Attributes:
        - KG: str = "kg"
        - L: str = "l"
        - UNITY: str = "un"
    """

    KG = "kg"
    L = "l"
    UNITY = "u"
