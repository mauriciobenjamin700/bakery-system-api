from uuid import uuid4


def id_generator():
    """
    A function that generates a unique identifier.

    Returns:
        str: A unique identifier.
    """
    return str(uuid4())
