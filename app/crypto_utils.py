import base64
import requests
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_rsa_keypair(key_size: int = 4096):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("keys/student_private.pem", "wb") as f:
        f.write(private_pem)
    with open("keys/student_public.pem", "wb") as f:
        f.write(public_pem)

    return private_key, public_key

def request_seed(student_id: str, github_repo_url: str, api_url: str):
    with open("keys/student_public.pem", "r") as f:
        public_key_pem = f.read()
    public_key_single_line = public_key_pem.replace("\n", "\\n")
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_single_line
    }
    resp = requests.post(api_url, json=payload, timeout=10)
    data = resp.json()
    if data.get("status") == "success" and "encrypted_seed" in data:
        with open("encrypted_seed.txt", "w") as f:
            f.write(data["encrypted_seed"])
        print("Encrypted seed saved to encrypted_seed.txt")
    else:
        raise Exception(f"Failed to request seed: {data}")

def decrypt_seed(encrypted_seed_b64: str, private_key):
    encrypted_seed = base64.b64decode(encrypted_seed_b64)
    seed_bytes = private_key.decrypt(
        encrypted_seed,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    seed_hex = seed_bytes.decode()
    if len(seed_hex) != 64 or not all(c in "0123456789abcdef" for c in seed_hex):
        raise ValueError("Invalid seed format")
    return seed_hex
