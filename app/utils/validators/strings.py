from re import match


def parse_string(value: str) -> str | None:
    """
    Parse a string value to ensure it is a valid string.

    Args:
        value (str): The string value to parse.
    Returns:
        str | None: The parsed string value, or None if the input is not a valid string.
    """
    if not isinstance(value, str):
        return None

    value = value.strip()

    if not value:
        return None

    return value


def parse_email(value: str) -> str | None:
    """
    Parse an email value to ensure it is a valid email format.

    Args:
        value (str): The email value to parse.
    Returns:
        str | None: The parsed email value, or None if the input is not a valid email format.
    """
    if not match(r"[^@]+@[^@]+\.[^@]+", value):
        return None
    return value


def parse_phone(value: str) -> str | None:
    """
    Parse a phone value to ensure it is a valid phone format.

    Args:
        value (str): The phone value to parse.
    Returns:
        str | None: The parsed phone value, or None if the input is not a valid phone format.
    """
    if not isinstance(value, str):
        return None

    value = "".join([char for char in value if char.isdigit()])

    if not value:
        return None

    if len(value) < 10 or len(value) > 15:
        return None

    return value
