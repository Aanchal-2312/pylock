from pylock.core.generator import (
    generate_password_v2,
    generate_passphrase,
    generate_username
)


# 🔐 PASSWORD TESTS

def test_password_length():
    pwd = generate_password_v2(length=16)
    assert len(pwd) == 16


def test_password_min_length_error():
    try:
        generate_password_v2(length=5)
        assert False
    except ValueError:
        assert True


def test_password_no_ambiguous():
    pwd = generate_password_v2(length=50, no_ambiguous=True)
    ambiguous = set("0O1l")
    assert not any(c in ambiguous for c in pwd)


def test_password_exclude_digits():
    pwd = generate_password_v2(length=20, exclude=["digits"])
    assert not any(c.isdigit() for c in pwd)


# 🔐 PASSPHRASE TESTS

def test_passphrase_word_count():
    wl = ["alpha", "beta", "gamma", "delta", "omega"]
    phrase = generate_passphrase(words=4, sep="-", wordlist=wl)
    assert len(phrase.split("-")) == 4


def test_passphrase_caps_all():
    wl = ["alpha", "beta", "gamma"]
    phrase = generate_passphrase(words=3, sep="-", caps="all", wordlist=wl)
    assert phrase.upper() == phrase


def test_passphrase_requires_wordlist():
    try:
        generate_passphrase(words=3, sep="-")
        assert False
    except ValueError:
        assert True


# 👤 USERNAME TESTS

def test_username_words_mode():
    wl = ["alpha", "beta", "gamma"]
    username = generate_username(vibe="words", wordlist=wl)
    assert isinstance(username, str)
    assert len(username) > 0


def test_username_requires_name():
    try:
        generate_username(vibe="tech")
        assert False
    except ValueError:
        assert True


def test_username_caps_all():
    username = generate_username(vibe="tech", name="test", caps="all")
    assert username.upper() == username


def test_username_digits_added():
    username = generate_username(vibe="tech", name="test", digits=2)
    assert any(c.isdigit() for c in username)


def test_username_symbols_added():
    username = generate_username(vibe="tech", name="test", symbols=1)
    assert any(c in "_.-" for c in username)