from pylock.core.analyzer import analyze_password


COMMON = ["password", "123456", "qwerty"]


def test_analyze_weak_password():
    result = analyze_password("password123", COMMON)

    assert result["score"] in ["Very Weak", "Weak"]
    assert "Password is too common" in result["weaknesses"] or any("pattern" in w for w in result["weaknesses"])


def test_analyze_strong_password():
    result = analyze_password("A$StrongPass123!", COMMON)

    assert result["score"] in ["Strong", "Very Strong"]
    assert result["entropy"] > 50


def test_entropy_non_zero():
    result = analyze_password("abc123", COMMON)
    assert result["entropy"] > 0


def test_repeated_characters_detection():
    result = analyze_password("aaaBBB111", COMMON)
    assert "Repeated characters detected" in result["weaknesses"]