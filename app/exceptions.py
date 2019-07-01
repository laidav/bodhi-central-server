from .modules.ErrorCodes import ErrorCodes


class ValidationError(ValueError):
    pass


class PostNotFoundError(Exception):
    def __init__(self):
        self.error = ErrorCodes.POST_NOT_FOUND


class SubjectNotFoundError(Exception):
    def __init__(self):
        self.error = ErrorCodes.SUBJECT_NOT_FOUND


class PracticeNotFoundError(Exception):
    def __init__(self):
        self.error = ErrorCodes.PRACTICE_NOT_FOUND


class UsernameAlreadyExistsError(Exception):
    def __init__(self):
        self.error = ErrorCodes.USERNAME_ALREADY_EXISTS


class EmailAlreadyExistsError(Exception):
    def __init__(self):
        self.error = ErrorCodes.EMAIL_ALREADY_EXISTS


class ConfirmPasswordError(Exception):
    def __init__(self):
        self.error = ErrorCodes.CONFIRM_PASSWORD


class UserNotFoundError(Exception):
    def __init__(self):
        self.error = ErrorCodes.USER_NOT_FOUND
