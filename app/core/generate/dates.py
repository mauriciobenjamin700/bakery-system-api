import datetime


def get_now() -> datetime.datetime:
    """
    Get the current date and time in UTC.

    - Args:
        - None

    - Returns:
        - datetime: The current date and time in UTC.
    """
    now = datetime.datetime.now(datetime.timezone.utc)

    return now


def get_now_timestamp() -> int:
    """
    Get the current date and time in UTC as a timestamp.

    - Args:
        - None

    - Returns:
        - datetime: The current date and time in UTC as a timestamp.
    """
    now = get_now()

    return int(now.timestamp())


def get_expiration_timestamp(
    now: datetime.datetime, expiration_time_in_minutes: int
) -> datetime:
    """
    Get the expiration timestamp.

    - Args:
        - now: datetime: The current date and time in UTC.
        - expiration_time_in_minutes: int: The expiration time in minutes.

    - Returns:
        - datetime: The expiration timestamp.
    """
    expiration_timestamp = now + datetime.timedelta(
        minutes=expiration_time_in_minutes
    )

    return expiration_timestamp.timestamp()
