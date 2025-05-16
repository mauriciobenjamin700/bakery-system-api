import datetime


def parse_date_to_string(
    value: datetime.datetime | datetime.date | str | int,
) -> str | None:
    """
    Parse a date value to ensure it is a valid date format.

    Args:
        value (datetime.date): The date value to parse.
    Returns:
        str | None: The parsed date value in string format, or None if the input is not a valid date.
    """
    if isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%d %H:%M")

    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d %H:%M")

    if isinstance(value, str):
        try:
            value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            return None
        return value.strftime("%Y-%m-%d %H:%M")

    if isinstance(value, int):
        try:
            value = datetime.datetime.fromtimestamp(value)
        except ValueError:
            return None
        return value.strftime("%Y-%m-%d %H:%M")

    return None
