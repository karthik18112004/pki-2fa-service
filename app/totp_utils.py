import pyotp
import base64

def generate_totp_code(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    seed_base32 = base64.b32encode(seed_bytes).decode()
    totp = pyotp.TOTP(seed_base32)
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    seed_bytes = bytes.fromhex(hex_seed)
    seed_base32 = base64.b32encode(seed_bytes).decode()
    totp = pyotp.TOTP(seed_base32)
    return totp.verify(code, valid_window=valid_window)
