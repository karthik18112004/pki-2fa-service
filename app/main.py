from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .crypto_utils import decrypt_seed
from .seed_store import save_seed, load_seed
from .totp_utils import generate_totp_code, verify_totp_code
from cryptography.hazmat.primitives import serialization

app = FastAPI()

class SeedPayload(BaseModel):
    encrypted_seed: str

class CodePayload(BaseModel):
    code: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/decrypt-seed")
def decrypt_seed_api(payload: SeedPayload):
    try:
        with open("keys/student_private.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        seed = decrypt_seed(payload.encrypted_seed, private_key)
        save_seed(seed)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate-2fa")
def generate_2fa():
    seed = load_seed()
    if not seed:
        raise HTTPException(status_code=400, detail="Seed not found")
    code = generate_totp_code(seed)
    return {"code": code, "valid_for": 30}

@app.post("/verify-2fa")
def verify_api(payload: CodePayload):
    seed = load_seed()
    if not seed:
        raise HTTPException(status_code=500, detail="Seed not found")
    valid = verify_totp_code(seed, payload.code)
    return {"valid": valid}
