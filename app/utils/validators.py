import re

# Format de téléphone tolérant
PHONE_REGEX = re.compile(r"^\+?[0-9][0-9\s().-]{6,20}$")

# Mini regex email (MVP) - le backend revalide de toute façon
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))

def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))