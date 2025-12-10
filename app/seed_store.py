import os

SEED_FILE = "/data/seed.txt"

def save_seed(seed: str):
    os.makedirs(os.path.dirname(SEED_FILE), exist_ok=True)
    with open(SEED_FILE, "w") as f:
        f.write(seed)

def load_seed() -> str:
    if not os.path.exists(SEED_FILE):
        return None
    with open(SEED_FILE, "r") as f:
        return f.read().strip()
