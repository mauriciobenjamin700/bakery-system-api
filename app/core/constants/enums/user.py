from enum import Enum


class UserRoles(str, Enum):
    """
    A class to represent the user roles in the application. A user role is a representation of the role of a user in the application.

    - Attributes:
        - USER: str = "user"
        - ADMIN: str = "admin"
    """

    USER = "user"
    ADMIN = "admin"

    def __str__(self) -> str:
        """
        Method to get the string representation of the enum.
        Returns:
            str: The string representation of the enum.
        """
        return str(self.value)

    def get(self) -> str:
        """
        Method to get the value of the enum.

        Returns:
            str: The value of the enum.
        """
        return self.value
