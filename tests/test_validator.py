from pylock.core.validator import validate_password


def test_valid_password():
    errors = validate_password(
        "A$StrongPass123!",
        min_length=12,
        require_symbols=True,
        require_numbers=True,
        no_repeats=True
    )
    assert errors == []


def test_short_password():
    errors = validate_password("short", min_length=10)
    assert "Minimum length required: 10" in errors


def test_missing_symbol():
    errors = validate_password("Password123", require_symbols=True)
    assert "Must include at least one symbol" in errors


def test_missing_number():
    errors = validate_password("Password!", require_numbers=True)
    assert "Must include at least one number" in errors


def test_repeated_characters():
    errors = validate_password("aaaBBB111", no_repeats=True)
    assert "No repeated characters allowed" in errors