# import secrets
from pylock.core.generator import generate_password_v2
# from pylock.services.wordlist import load_words


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



# def handle_passphrase(args):
#     words = load_words()

#     if args.words < 2:
#         raise ValueError("Minimum 2 words required")

#     chosen = [secrets.choice(words) for _ in range(args.words)]

#     if args.caps:
#         chosen = [w.capitalize() for w in chosen]

#     separator = args.sep if args.sep else "-"

#     return separator.join(chosen)