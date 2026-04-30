from pylock.core.analyzer import analyze_password
from pylock.core.validator import validate_password
from pylock.infra.wordlist import load_common_passwords


def handle_check(args):
    """Analyze password strength and apply strict validation rules if enabled."""    
    common_passwords = load_common_passwords()

    result = analyze_password(args.password, common_passwords)

    # Apply strict validation rules if enabled
    if args.strict:
        validation_errors = validate_password(
            password=args.password,
            min_length=12,
            require_symbols=True,
            require_numbers=True,
            no_repeats=True
        )
        result["validation"] = validation_errors

    return result