#!/usr/bin/env bash
#
# verify_deployment.sh
#
# Re-runs the manual checks used to confirm the deployed chat server
# satisfies all 6 mandatory lab requirements: persistence, history on
# join, no plaintext storage, tamper detection, signing keys, and
# signature verification (the last is implicit — a tampered message
# never passes verification, see server.py's verify_message()).
#
# Run this from inside the app directory on the host machine, e.g.:
#   ssh -p 2313 student@10.1.75.51
#   cd ~/chat_app
#   bash verify_deployment.sh
#
# Requires: curl, python3, sqlite3-capable python (standard library)

set -euo pipefail

PORT="${PORT:-5000}"
DB="${DB:-chat.db}"
KEYS_DIR="${KEYS_DIR:-keys}"

echo "=== 1. Server health ==="
curl -s "http://localhost:${PORT}/health" && echo
echo

echo "=== 2. Stored messages are ciphertext (not plaintext) ==="
python3 -c "
import sqlite3
conn = sqlite3.connect('${DB}')
rows = conn.execute('SELECT sender, ciphertext FROM messages').fetchall()
if not rows:
    print('No messages stored yet — send a few via the web client first.')
else:
    for sender, ciphertext in rows:
        print(f'{sender}: {ciphertext}')
"
echo

echo "=== 3. Signing keys registered per sender ==="
python3 -c "
import sqlite3
conn = sqlite3.connect('${DB}')
rows = conn.execute('SELECT * FROM signing_keys').fetchall()
if not rows:
    print('No signing keys yet — have a user join the chat first.')
else:
    for row in rows:
        print(row)
"
echo
echo "Private key files on disk:"
ls -la "${KEYS_DIR}/" 2>/dev/null || echo "  (keys/ directory not found yet)"
echo

echo "=== 4. Tamper detection demo ==="
echo "This will corrupt the most recent message's ciphertext, then restart"
echo "the server. Rejoin the chat afterwards to confirm it shows:"
echo "  '⚠ TAMPER DETECTED: ciphertext/authentication tag invalid'"
read -p "Run tamper demo now? [y/N] " confirm
if [[ "${confirm}" == "y" || "${confirm}" == "Y" ]]; then
    pkill -f server.py || true
    python3 demo_tamper.py
    nohup python3 server.py > server.log 2>&1 &
    echo "Server restarted. Rejoin the web client to see the tamper warning."
else
    echo "Skipped."
fi

echo
echo "=== Verification complete ==="
echo "See TESTING.md for a written log of a full verification pass."
