"""Password validation utilities.

Validates passwords against configurable security rules."""
import re


def validate_password(password, min_length=8, require_symbols=False, require_numbers=False, no_repeats=False):
    """Validate password against security requirements and return a list of errors."""
    errors = []

    # min length
    if len(password) < min_length:
        errors.append(f"Minimum length required: {min_length}")

    # symbols
    if require_symbols and not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", password):
        errors.append("Must include at least one symbol")

    # numbers
    if require_numbers and not re.search(r"[0-9]", password):
        errors.append("Must include at least one number")

    # no repeats
    if no_repeats and re.search(r"(.)\1{2,}", password):
        errors.append("No repeated characters allowed")

    return errors