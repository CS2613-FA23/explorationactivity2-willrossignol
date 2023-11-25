import re


def check_email(email: str):
    pattern = (
        # Prefix
        "[A-Za-z0-9]+([\._-][A-Za-z0-9]+)*"
        # @ Character
        "@"
        # Suffix
        "[A-Za-z0-9-]+[.][A-Za-z0-9-]{2,}"
    )
    found = re.fullmatch(pattern, email)
    return bool(found)


def check_password(password: str):
    safe = False

    pattern = (
        # Start of string
        "^"
        # At least one number
        "(?=.*[0-9]+.*)"
        # At least one lowercase letter
        "(?=.*[a-z]+.*)"
        # At least one uppercase letter
        "(?=.*[A-Z]+.*)"
        # At least one special character
        "(?=.*[!@#$%&_=,/<>?;':^*()+.\"{}\[\]\\\\-]+.*)"
        # No whitespace characters
        "(?!.*\s+.*)"
        # At least 8 characters
        ".{8,}"
        # End of string
        "$"
    )

    password_check = re.match(pattern, password)
    if password_check:
        safe = True

    return safe
