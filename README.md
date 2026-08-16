# Persistent and Secure Group Chat Application (Flask + WebSockets)

A real-time, multi-client Group Chat Application built using **Flask** and **Flask-SocketIO (WebSockets)**, extended with **persistence, encryption, integrity, and authenticity** — messages are stored in SQLite, encrypted with AES-256-GCM, and signed per-sender with Ed25519.

![UI Theme](https://img.shields.io/badge/UI-Cyberpunk_Glassmorphism-6366f1)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![WebSockets](https://img.shields.io/badge/WebSockets-Flask--SocketIO-emerald)
![Security](https://img.shields.io/badge/Crypto-AES--GCM_%2B_Ed25519-red)

---

## 🌟 Key Features

**Real-time chat**
- Instant bi-directional communication powered by WebSockets.
- User join/leave notifications, unique username validation, typing indicator, live user sidebar.
- Aurora glassmorphism UI with dark-mode cyberpunk aesthetic.

**Persistence, Encryption, Integrity & Authenticity**
- **Persistence** — every message is stored in a local SQLite database (`chat.db`); new users receive full chat history on join.
- **Confidentiality** — messages are encrypted with **AES-256-GCM** before being written to disk. The database never contains plaintext.
- **Integrity** — AES-GCM's built-in authentication tag detects any tampering with stored ciphertext. Corrupted messages are flagged as `⚠ TAMPER DETECTED` instead of being silently shown or crashing the app.
- **Authenticity** — each username is bound to its own **Ed25519** signing keypair (generated on first join, persisted under `keys/`). Every message is signed by its sender and re-verified whenever history is loaded.

---

## 🚀 Allotted SSH Server & Deployment Details

- **Student 1 (Host Server)**: `ssh -p 2237 student@10.1.75.51`
- **Student 2 Client**: `ssh -p 2238 student@10.1.75.51`
- **Student 3 Client**: `ssh -p 2239 student@10.1.75.51`
- **Student 4 Client**: `ssh -p 2240 student@10.1.75.51`
- **Live Client Testing URL**: **`http://10.1.75.51:5000`**

---

## 🛠️ Quick Start

### 1. Local Run
```bash
git clone https://github.com/chaitanyakumarAI/Group-Chat.git
cd Group-Chat
pip install -r requirements.txt
python3 server.py
```
Open `http://localhost:5000` in your browser. On first run, `chat.db`, `secret.key`, and a `keys/` folder are created automatically — no manual setup needed.

### 2. Deploy on Remote SSH Server
```bash
# Copy files to server
scp -P 2237 -r . student@10.1.75.51:~/chat_app

# Connect and run
ssh -p 2237 student@10.1.75.51
cd ~/chat_app
pip install -r requirements.txt
nohup python3 server.py > server.log 2>&1 &
```

---

## 🔍 Verifying It Works

```bash
# Health check
curl http://localhost:5000/health

# Confirm messages are stored as ciphertext, not plaintext
python3 -c "import sqlite3; c=sqlite3.connect('chat.db'); print(c.execute('SELECT sender, ciphertext FROM messages').fetchall())"

# Confirm each sender has a signing keypair
python3 -c "import sqlite3; c=sqlite3.connect('chat.db'); print(c.execute('SELECT * FROM signing_keys').fetchall())"
```

To confirm persistence: send a message, stop the server (`Ctrl+C`), restart it, and rejoin — earlier messages reappear via the `history` event.

---

## 🧪 Demonstrating Tamper Detection

```bash
# 1. Send a message in the browser, then stop the server
# 2. Corrupt the most recent stored message:
python3 demo_tamper.py
# 3. Restart the server and rejoin — the tampered message now shows:
#    "⚠ TAMPER DETECTED: ciphertext/authentication tag invalid"
```

---

## 📁 Project Structure

```
Group-Chat/
├── server.py            # Flask-SocketIO server: persistence, encryption, signing
├── demo_tamper.py        # Corrupts a stored ciphertext to demo tamper detection
├── templates/index.html  # Chat UI (real-time + history rendering)
├── requirements.txt
├── .gitignore             # Excludes chat.db, secret.key, keys/ (never commit secrets)
├── chat.db*               # Auto-generated SQLite database (not committed)
├── secret.key*            # Auto-generated AES-256 key (not committed)
└── keys/*                 # Auto-generated per-user Ed25519 private keys (not committed)

* generated automatically on first run, excluded from git
```