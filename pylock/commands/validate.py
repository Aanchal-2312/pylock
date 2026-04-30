from pylock.core.validator import validate_password
from pylock.core.config import load_config


def handle_validate(args):
    """Handle password validation based on user input and config settings."""
    config = load_config()

    # if user enables basic mode → override strict config
    if args.basic:
        return validate_password(
            password=args.password,
            min_length=8,
            require_symbols=False,
            require_numbers=False,
            no_repeats=False
        )

    # Otherwise use configured validation rules
    return validate_password(
        password=args.password,
        min_length=config["min_length"],
        require_symbols=config["require_symbols"],
        require_numbers=config["require_numbers"],
        no_repeats=config["no_repeats"]
    )