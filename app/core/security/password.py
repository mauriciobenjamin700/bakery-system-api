import bcrypt


def hash_password(password: str) -> str:
    """
    Generates a hashed password.

    - Args:
        - password: str: The password to be hashed.
    - Returns:
        - str: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a hashed password.

    - Args:
        - plain_password: str: The plain password.
        - hashed_password: str: The hashed password.

    - Returns:
        - bool: True if the plain password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
