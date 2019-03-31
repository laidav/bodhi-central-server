from .modules.ErrorCodes import ErrorCodes


class ValidationError(ValueError):
    pass


class PostNotFoundError(Exception):
    def __init__(self):
        self.error = ErrorCodes.POST_NOT_FOUND
