from app.seed_store import load_seed
from app.totp_utils import generate_totp_code
import datetime

seed = load_seed()
if seed:
    code = generate_totp_code(seed)
    print(f"{datetime.datetime.utcnow().isoformat()} - {code}")
