# PKI-2FA Service

## Files
- `main.py` - Flask API with endpoints `/decrypt-seed`, `/generate-2fa`, `/verify-2fa`
- `crypto_utils.py` - RSA/OAEP decryption helper
- `seed_store.py` - seed persistence helper (writes `/data/seed.txt`)
- `totp_utils.py` - generate/verify TOTP using `pyotp`
- `cron/totp_cron.py` - cron script that writes `/cron/last_code.txt` every minute
- `cron/cronjob.sh` - cron wrapper
- `keys/` - place `student_private.pem`, `student_public.pem`, `instructor_public.pem` here
- `encrypted_seed.txt` - the instructor-provided encrypted seed (base64 single line)
- `Dockerfile` + `docker-compose.yml`

## Quick local run (Linux / WSL recommended)

1. Build & run:
```bash
docker-compose build
docker-compose up -d
