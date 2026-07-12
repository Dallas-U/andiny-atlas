class CaseNotFoundException(Exception):
    """Raised when a requested investigation case cannot be found."""

    def __init__(self, case_id: str):

        self.case_id = case_id

        super().__init__(f"Case '{case_id}' was not found.")


class PersistenceDataException(Exception):
    """Raised when persisted investigation data cannot be read safely."""

    def __init__(self, message: str):

        super().__init__(message)


class InvalidCredentialsException(Exception):
    """Raised when user authentication fails."""

    def __init__(self):

        super().__init__("Invalid email or password.")


class UserAlreadyExistsException(Exception):
    """Raised when attempting to register an existing user."""

    def __init__(self, email: str):

        self.email = email

        super().__init__(f"A user with email '{email}' already exists.")


class UserNotFoundException(Exception):
    """Raised when a requested user cannot be found."""

    def __init__(self, email: str):

        self.email = email

        super().__init__(f"User '{email}' was not found.")


class InactiveUserException(Exception):
    """Raised when an inactive user attempts to authenticate."""

    def __init__(self):

        super().__init__("User account is inactive.")
