import base64
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization, hashes
import subprocess

def sign_message(message: str, private_key) -> bytes:
    return private_key.sign(
        message.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )

def load_private_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def get_latest_commit_hash() -> str:
    return subprocess.check_output(
        ["git", "log", "-1", "--format=%H"]
    ).decode("utf-8").strip()

def main():
    commit_hash = get_latest_commit_hash()
    private_key = load_private_key("keys/student_private.pem")
    instructor_key = load_public_key("keys/instructor_public.pem")
    signature = sign_message(commit_hash, private_key)
    encrypted_signature = encrypt_with_public_key(signature, instructor_key)
    encoded_signature = base64.b64encode(encrypted_signature).decode("utf-8")
    print("Commit Hash:", commit_hash)
    print("Encrypted Commit Signature:", encoded_signature)

if __name__ == "__main__":
    main()
