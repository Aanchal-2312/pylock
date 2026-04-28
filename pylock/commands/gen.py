import secrets
import random
from pylock.core.generator import generate_password_v2, generate_passphrase, generate_username
from pylock.services.wordlist import load_words, load_username_words


# Password generation
def handle_password(args):
    exclude = []

    if args.nd:
        exclude.append("digits")
    if args.ns:
        exclude.append("symbols")

    counts = {}

    if args.uppercase is not None:
        counts["upper"] = args.uppercase
    if args.lowercase is not None:
        counts["lower"] = args.lowercase
    if args.digits is not None:
        counts["digits"] = args.digits
    if args.symbols is not None:
        counts["symbols"] = args.symbols

    results = []

    for _ in range(args.number):
        pwd = generate_password_v2(
            length=args.length,
            counts=counts if counts else None,
            exclude=exclude,
            no_ambiguous=args.na
        )
        results.append(pwd)

    return results



# Passphrase generation
def handle_passphrase(args):
    words = load_words()

    phrases =[]

    for _ in range(args.number):
        phrase = generate_passphrase(
            words=args.words,
            sep=args.sep,
            caps=args.caps,
            digits=args.digits,
            wordlist=words
        )
        phrases.append(phrase)

    return phrases


# Username generation
def handle_username(args):
    usernames = []

    words = None
    if args.vibe == "words":
        words = load_username_words()

    while len(usernames) < args.number:
        u = generate_username(
            vibe=args.vibe,
            name=args.name,
            digits=args.digits,
            symbols=args.symbols,
            caps=args.caps,
            wordlist=words
        )

        if u not in usernames:
            usernames.append(u)

    return usernames