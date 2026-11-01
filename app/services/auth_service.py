"""Business rules for accounts. No Flask request objects and no SQL here."""
from werkzeug.security import check_password_hash, generate_password_hash

from ..repositories import user_repository

MIN_PASSWORD_LENGTH = 8


class AuthError(Exception):
    """Raised with a user-facing message when a rule is broken."""


def register(email, password):
    email = (email or "").strip().lower()
    if not email or "@" not in email:
        raise AuthError("Enter a valid email address.")
    if len(password or "") < MIN_PASSWORD_LENGTH:
        raise AuthError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.")
    if user_repository.find_by_email(email):
        raise AuthError("An account with that email already exists.")
    return user_repository.create(email, generate_password_hash(password))


def authenticate(email, password):
    user = user_repository.find_by_email((email or "").strip().lower())
    if user is None or not check_password_hash(user["password_hash"], password or ""):
        raise AuthError("Incorrect email or password.")
    return user
