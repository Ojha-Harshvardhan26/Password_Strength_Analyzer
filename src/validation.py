"""Input validation. Messages are static and never contain password characters."""

from src.config import MAX_PASSWORD_LENGTH
from src.models import ValidationResult

EMPTY_MESSAGE = "Please enter a password."
TOO_LONG_MESSAGE = f"Password is too long (maximum {MAX_PASSWORD_LENGTH} characters)."
INVALID_TYPE_MESSAGE = "Invalid input."
WHITESPACE_NOTICE = "Spaces at the start or end are counted as characters."


def validate_password(password: object) -> ValidationResult:
    """Check that the input is a non-empty string within the length limit."""
    if not isinstance(password, str):
        return ValidationResult(False, INVALID_TYPE_MESSAGE)
    if len(password) == 0:
        return ValidationResult(False, EMPTY_MESSAGE)
    if len(password) > MAX_PASSWORD_LENGTH:
        return ValidationResult(False, TOO_LONG_MESSAGE)
    notices = ()
    if password[0].isspace() or password[-1].isspace():
        notices = (WHITESPACE_NOTICE,)
    return ValidationResult(True, None, notices)
