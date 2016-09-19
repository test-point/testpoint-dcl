class DclBackendException(Exception):
    pass


class DclBackendValidationError(DclBackendException):
    pass


class DclBackendPushException(DclBackendException):
    """
    Raised when the source data is valid, but changes cannot be saved and we can't
    do anything with it; worth logging and showing error message to the user
    """

    pass
