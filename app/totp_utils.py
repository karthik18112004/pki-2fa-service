import pyotp


def generate_totp(seed: str) -> str:
    totp = pyotp.TOTP(seed)
    return totp.now()


def verify_totp(seed: str, code: str) -> bool:
    totp = pyotp.TOTP(seed)
    return totp.verify(code)
