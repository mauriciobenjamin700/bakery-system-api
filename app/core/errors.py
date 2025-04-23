class BadRequestError(Exception):
    """
    A class that represents a bad request error.

    - Attributes:
        - status_code: The status code of the error.
        - detail: The error message.
    """

    def __init__(self, detail: str):
        """
        The constructor for the BadRequestError class.

        - Args:
            - detail: The error message.
        """
        self.status_code = 400
        self.detail = detail
        super().__init__(detail)


class ConflictError(Exception):
    """
    A class that represents a conflict error.

    - Attributes:
        - status_code: The status code of the error.
        - detail: The error message.
    """

    def __init__(self, detail: str):
        """
        The constructor for the ConflictError class.

        - Args:
            - detail: The error message.
        """
        self.status_code = 409
        self.detail = detail
        super().__init__(detail)


class NotFoundError(Exception):
    """
    A class that represents a not found error.

    - Attributes:
        - status_code: The status code of the error.
        - detail: The error message.
    """

    def __init__(self, detail: str):
        """
        The constructor for the NotFoundError class.

        - Args:
            - detail: The error message.
        """
        self.status_code = 404
        self.detail = detail
        super().__init__(detail)


class UnauthorizedError(Exception):
    """
    A class that represents an unauthorized error.

    - Attributes:
        - status_code: The status code of the error.
        - detail: The error message.
    """

    def __init__(self, detail: str):
        """
        The constructor for the UnauthorizedError class.

        - Args:
            - detail: The error message.
        """
        self.status_code = 401
        self.detail = detail
        super().__init__(detail)


class UnprocessableEntityError(Exception):
    """
    A class that represents an unprocessable entity error.

    - Attributes:
        - status_code: The status code of the error.
        - detail: The error message.
    """

    def __init__(self, detail: str):
        """
        The constructor for the UnprocessableEntityError class.

        - Args:
            - detail: The error message.
        """
        self.status_code = 422
        self.detail = detail
        super().__init__(detail)


class ValidationError(Exception):
    """
    A class that represents a validation error.

    - Attributes:
        - status_code: The status code of the error.
        - field: The field that caused the error.
        - detail: The error message.
    """

    def __init__(self, field: str, detail: str):
        """
        The constructor for the ValidationError class.

        - Args:
            - field: The field that caused the error.
            - detail: The error message.
        """
        self.status_code = 422
        self.field = field
        self.detail = detail
        super().__init__(f"{field}: {detail}")
