"""Core generators for PyLock.

Includes password, passphrase, and username generation with various options."""
import secrets
import string
import random


# PASSWORD GENERATION
def generate_password_v2(length=12, counts=None, exclude=None, no_ambiguous=False):
    """Generate a secure password with optional constraints and exclusions."""
    if length < 8:
        raise ValueError("Minimum length is 8")

    # Define character pools
    char_sets = {
        "lower": string.ascii_lowercase,
        "upper": string.ascii_uppercase,
        "digits": string.digits,
        "symbols": "@#!~$&-*^_%"
    }

    # Remove ambiguous chars
    if no_ambiguous:
        for key in char_sets:
            char_sets[key] = ''.join(c for c in char_sets[key] if c not in "0O1l")

    # Apply character type exclusions
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

    # Fill remaining chars
    all_chars = ''.join(char_sets.values())
    for _ in range(length - len(password)):
        password.append(secrets.choice(all_chars))

    random.shuffle(password)
    
    type_count = len(char_sets)

    # Ensure password uses at least 2 character types
    if type_count < 2:
        raise ValueError("At least 2 character types required")
    return ''.join(password)


# PASSPHRASE GENERATION
def generate_passphrase(words, sep, caps=None, digits=0, wordlist=None):
    """Generate a passphrase using random words with optional formatting."""

    # Ensure wordlist is provided and valid
    if not wordlist:
        raise ValueError("Wordlist is required")

    if words < 2:
        raise ValueError("Minimum 2 words required")
    
    # Select unique words
    selected = []
    while len(selected) < words:
        w = secrets.choice(wordlist)
        if w not in selected:
            selected.append(w)

    # Apply capitalization rules
    if caps == "all":
        selected = [w.upper() for w in selected]
    elif caps == "first":
        selected = [w.capitalize() for w in selected]

    # Add digits to random words
    for _ in range(digits):
        idx = random.randint(0, len(selected) - 1)
        selected[idx] += str(random.randint(0, 9))

    return sep.join(selected)


# USERNAME GENERATION
def generate_username(vibe="clean", name=None, digits=0, symbols=0, caps="first", wordlist=None):
    """Generate a username based on vibe, name, and formatting options."""
    # validate required parameters
    if vibe != "words" and not name:
        raise ValueError("Name is required for non-words vibe")

    # Predefined username patterns for different vibes
    vibe_patterns = {
        "clean": [
            f"{name}.dev",
            f"{name}.codes",
            f"{name}.cloud",
            f"{name}.sec",
        ],
        "aesthetic": [
            f"hey.{name}",
            f"its{name}",
            f"the{name}",
            f"{name}hq",
        ],
        "tech": [
            f"{name}ops",
            f"{name}stack",
            f"{name}builds",
            f"{name}core",
            f"{name}labs",
            
        ],
        "edgy": [
            f"{name}x",
            f"{name}byte",
            f"{name}root",
        ],
        "gamer": [
            f"{name}_x",
            f"{name}_pro",
            f"{name}_kill",
            f"{name}_op",
        ],
        "random": [
            f"{name}",
            f"{name}_dev",
            f"{name}.codes",
            f"{name}x",
        ]
    }

    # Word-based usernames
    if vibe == "words":
        if not wordlist:
            raise ValueError("Wordlist is required for words vibe")

        # Filter out generic/system-like words
        bad_words = {"library","leader","base","walker","report","log","data","file","code","script","app","service","system","network","admin","user","client","server"}

        filtered = [w for w in wordlist if w not in bad_words]
        # Ensure two distinct words   
        w1 = random.choice(filtered)
        w2 = random.choice(filtered)
        while w2 == w1:
            w2 = random.choice(filtered)

        sep = random.choice(["_", ".", "-",""])
        base = f"{w1}{sep}{w2}"
    else:
        base = random.choice(vibe_patterns[vibe])
    

    # Apply capitalization rules
    if caps == "all":
        base = base.upper()
    elif caps == "first":
        base = base.capitalize()

    # Add numeric suffix if requested
    suffix = ""
    if digits > 0:
        suffix = str(random.randint(10**(digits-1), (10**digits) - 1))

    # Add symbol separator intelligently based on existing username structure
    if symbols > 0:
        symbols_list = ["_", ".", "-"]

        if base.endswith(tuple(symbols_list)):
            available = [s for s in symbols_list if not base.endswith(s)]
            sym = random.choice(available)
        elif "." in base:
            sym = random.choice(["_", "-"])
        else:
            sym = random.choice(symbols_list)

        username = f"{base}{sym}{suffix}" if suffix else f"{base}{sym}"
    else:
        username = f"{base}{suffix}"

    return username