from uuid import uuid4


def id_generator() -> str:
    """
    A function that generates a unique identifier.

    Returns:
        str: A unique identifier.
    """
    return str(uuid4())


def code_generator() -> str:
    """
    A function that generates a unique code.

    Returns:
        str: A unique code.
    """
    return str(uuid4())
