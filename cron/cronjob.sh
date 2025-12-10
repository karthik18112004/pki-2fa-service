#!/bin/sh

while true; do
  if [ -f /data/seed.txt ]; then
    SEED=$(cat /data/seed.txt)
    CODE=$(python3 - <<EOF
import pyotp, sys
seed = sys.argv[1]
print(pyotp.TOTP(seed).now())
EOF
"$SEED")
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $CODE" > /cron/last_code.txt
  fi
  sleep 60
done
