def load_words():
    try:
        with open("wordlist.txt", "r") as f:
            return [w.strip() for w in f if w.strip()]
    except FileNotFoundError:
        raise ValueError("wordlist.txt not found")
    

def load_username_words():
    try:
        with open(f"pylock/services/wordlists/username_words.txt", "r") as f:
            return [w.strip() for w in f if w.strip()]
    except FileNotFoundError:
        raise ValueError("username_words.txt not found")
    