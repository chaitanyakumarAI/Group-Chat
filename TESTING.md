# Deployment & Verification Log

Deployed and verified on the allotted lab host `stu29_sys1` (SSH port 2313),
exposed at `http://10.1.75.51:5313`.

## 1. Server health
```
curl http://localhost:5000/health
{"connected_users":0,"status":"ok","stored_messages":0,"users":[]}
```

## 2. Persistence
Sent messages "Hi" and "Hello" via the web client, restarted the server
(`pkill -f server.py` then relaunched), rejoined — both messages reloaded
correctly from `chat.db` via the `history` event.

## 3. Confidentiality (no plaintext in DB)
```
python3 -c "import sqlite3; c=sqlite3.connect('chat.db'); \
print(c.execute('SELECT sender, ciphertext FROM messages').fetchall())"
[('Madhu', 'rshOMy2gmmzlh6xbUfKyXd+OAg=='), ('Madhu', 'XhXNHaG4U7y+dLztEaEHMf7DXTn0')]
```
Only AES-256-GCM ciphertext is stored — never plaintext.

## 4. Tamper detection
Ran `demo_tamper.py` to corrupt a stored ciphertext, restarted the server,
rejoined — the corrupted message correctly rendered as:
`⚠ TAMPER DETECTED: ciphertext/authentication tag invalid`

## 5. Signing keys
```
python3 -c "import sqlite3; c=sqlite3.connect('chat.db'); \
print(c.execute('SELECT * FROM signing_keys').fetchall())"
[('Madhu', '7VP0qmt9dnelFIEk74ey7zqy1AT/jG23A3nK+E0m1OQ=')]
```
Each sender's Ed25519 keypair is generated on first join and persisted under `keys/`
(e.g. `keys/Madhu.pem`); every message is verified against it on load.

All six mandatory requirements confirmed working end-to-end.
