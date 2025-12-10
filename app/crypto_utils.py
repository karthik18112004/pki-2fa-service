import base64
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization, hashes


def decrypt_seed(encrypted_seed_b64: str) -> str:
    encrypted_seed = base64.b64decode(encrypted_seed_b64)

    with open("keys/student_private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=None
        )

    seed = private_key.decrypt(
        encrypted_seed,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return seed.decode()
