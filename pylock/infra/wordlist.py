"""Wordlist loading functions for gen and analyze commands."""

def load_words():
    try:
        with open(f"pylock/infra/wordlists/wordlist.txt", "r") as f:
            return [w.strip() for w in f if w.strip()]
    except FileNotFoundError:
        raise ValueError("wordlist.txt not found")
    

def load_username_words():
    try:
        with open(f"pylock/infra/wordlists/username_words.txt", "r") as f:
            return [w.strip() for w in f if w.strip()]
    except FileNotFoundError:
        raise ValueError("username_words.txt not found")
    

def load_common_passwords():
    try:
        with open(f"pylock/infra/wordlists/common_passwords.txt", "r") as f:
            return [w.strip().lower() for w in f if w.strip()]
    except FileNotFoundError:
        return []