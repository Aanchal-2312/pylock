from pylock.core.hasher import hash_password, verify_password


def test_bcrypt_hash_and_verify():
    pwd = "mypassword"
    hashed = hash_password(pwd, "bcrypt")

    assert verify_password(pwd, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_argon2_hash_and_verify():
    pwd = "mypassword"
    hashed = hash_password(pwd, "argon2")

    assert verify_password(pwd, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_invalid_hash_format():
    try:
        verify_password("test", "invalid_hash")
        assert False
    except ValueError:
        assert True