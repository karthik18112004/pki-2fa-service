#!/bin/sh
python3 /app/cron/totp_cron.py >> /app/cron/last_code.txt 2>&1
