"""Password analysis utilities.
Includes entropy calculation, pattern detection, crack time estimation, and improvement suggestions."""
import math
import re



def calculate_entropy(password):
    """Estimate Password entropy based on character variety and length."""
    pool = 0

    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", password):
        pool += 32

    if pool == 0:
        return 0

    return len(password) * math.log2(pool)


def check_patterns(password, common_passwords):
    """Detect common patterns and weaknesses in the password."""
    weaknesses = []
    pwd = password.lower()
    
    if pwd in common_passwords:
        weaknesses.append("Password is too common")

    for common in common_passwords:
        if common in pwd and len(common) > 3:
            weaknesses.append(f"Contains common pattern: '{common}'")

    if re.search(r"(.)\1{2,}", password):
        weaknesses.append("Repeated characters detected")

    return list(set(weaknesses))  


def estimate_crack_time(entropy, weaknesses):
    """Estimate time required to brute-force the password."""
    if weaknesses:
        return "Instant (dictionary attack)"

    guesses = 2 ** entropy
    guesses_per_sec = 1e9

    seconds = guesses / guesses_per_sec

    if seconds < 60:
        return "Seconds"
    elif seconds < 3600:
        return "Minutes"
    elif seconds < 86400:
        return "Hours"
    elif seconds < 31536000:
        return "Days"
    elif seconds < 1e9:
        return "Years"
    else:
        return "Centuries"


def score_password(entropy, weaknesses):
    """Classify password strength based on entropy and weaknesses."""
    if weaknesses:
        if entropy < 40:
            return "Very Weak"
        elif entropy < 60:
            return "Weak"
        else:
            return "Moderate"

    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Moderate"
    elif entropy < 80:
        return "Strong"
    else:
        return "Very Strong"


def suggest_improvements(password):
    """Generate actionable suggestions to strengthen the password."""
    suggestions = []

    if len(password) < 12:
        suggestions.append("Increase length to at least 12")

    if not re.search(r"[A-Z]", password):
        suggestions.append("Add uppercase letters")

    if not re.search(r"[a-z]", password):
        suggestions.append("Add lowercase letters")

    if not re.search(r"[0-9]", password):
        suggestions.append("Add digits")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", password):
        suggestions.append("Add symbols")

    return suggestions


def analyze_password(password, common_passwords):
    """Perform full password analysis and return structured results."""
    entropy = calculate_entropy(password)
    weaknesses = check_patterns(password, common_passwords)

    penalty = 0
    if weaknesses:
        penalty += 30

    entropy = max(0, entropy - penalty)

    suggestions = suggest_improvements(password)
    score = score_password(entropy, weaknesses)
    crack_time = estimate_crack_time(entropy, weaknesses)

    return {
        "entropy": round(entropy, 2),
        "score": score,
        "crack_time": crack_time,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
    }