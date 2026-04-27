import secrets
import string
import random

def generate_password_v2(length=12, counts=None, exclude=None, no_ambiguous=False):
    if length < 8:
        raise ValueError("Minimum length is 8")

    import string

    char_sets = {
        "lower": string.ascii_lowercase,
        "upper": string.ascii_uppercase,
        "digits": string.digits,
        "symbols": "@#!~$&-*^_%"
    }

    # remove ambiguous chars
    if no_ambiguous:
        for key in char_sets:
            char_sets[key] = ''.join(c for c in char_sets[key] if c not in "0O1l")

    # apply exclusions
    if exclude:
        for key in exclude:
            char_sets.pop(key, None)

    if not char_sets:
        raise ValueError("No character sets available")

    password = []

    # COUNT MODE
    if counts:
        total = sum(counts.values())
        if total > length:
            raise ValueError("Counts exceed length")

        for key, count in counts.items():
            if key in char_sets:
                for _ in range(count):
                    password.append(secrets.choice(char_sets[key]))

    # remaining chars
    all_chars = ''.join(char_sets.values())
    for _ in range(length - len(password)):
        password.append(secrets.choice(all_chars))

    random.shuffle(password)
    
    type_count = len(char_sets)

    if type_count < 2:
        raise ValueError("At least 2 character types required")
    return ''.join(password)
