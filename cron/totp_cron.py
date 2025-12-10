# cron/totp_cron.py
from datetime import datetime, timezone
import os
from seed_store import load_seed
from totp_utils import generate_totp

OUT_FILE = "/cron/last_code.txt"

def main():
    seed = load_seed()
    if not seed:
        # no seed yet; do nothing
        return 1
    code = generate_totp(seed)
    ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w") as f:
        f.write(f"{ts} {code}\n")
    return 0

if __name__ == "__main__":
    exit(main())
