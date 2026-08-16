"""
Persistent and Secure Group Chat — Backend Server
Flask + Flask-SocketIO (WebSockets) + SQLite + AES-GCM + Ed25519 signatures

Extends real-time chat with:
  1. Persistence     -> messages stored in SQLite (chat.db)
  2. Confidentiality -> AES-256-GCM encryption before storage
  3. Integrity       -> AES-GCM authentication tag detects tampering
  4. Authenticity    -> Ed25519 signature per sender, verified on read
"""

import os
import base64
import logging
import sqlite3
import threading
from datetime import datetime

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature, InvalidTag

# ─── App Configuration ───
app = Flask(__name__)
app.config["SECRET_KEY"] = "groupchat_secret_key_2024"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    logger=False,
    engineio_logger=False,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

ROOM = "general"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chat.db")
KEY_FILE = os.path.join(BASE_DIR, "secret.key")
KEYS_DIR = os.path.join(BASE_DIR, "keys")
os.makedirs(KEYS_DIR, exist_ok=True)

# ─── In-Memory State ───
connected_users: dict[str, dict] = {}       # sid -> {"username": str}
signing_keys: dict[str, Ed25519PrivateKey] = {}  # username -> loaded private key
db_lock = threading.Lock()


def get_user_list() -> list[str]:
    return [u["username"] for u in connected_users.values()]


def now() -> str:
    return datetime.now().strftime("%H:%M:%S")


# ─── Database Setup (Persistence) ───
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id TEXT NOT NULL,
        sender TEXT NOT NULL,
        ciphertext TEXT NOT NULL,   -- base64 AES-GCM ciphertext (+ auth tag)
        nonce TEXT NOT NULL,        -- base64 12-byte nonce
        signature TEXT NOT NULL,    -- base64 Ed25519 signature over plaintext
        timestamp TEXT NOT NULL
    )
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS signing_keys (
        username TEXT PRIMARY KEY,
        public_key TEXT NOT NULL    -- base64 raw Ed25519 public key
    )
""")
conn.commit()


# ─── Symmetric Key (Confidentiality) ───
# A single AES-256 key protects the room. It is generated once and persisted
# to disk so that history stored before a restart can still be decrypted.
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        AES_KEY = f.read()
else:
    AES_KEY = AESGCM.generate_key(bit_length=256)
    with open(KEY_FILE, "wb") as f:
        f.write(AES_KEY)

aesgcm = AESGCM(AES_KEY)


def encrypt_message(plaintext: str) -> tuple[str, str]:
    """Return (ciphertext_b64, nonce_b64). AES-GCM tag is embedded in ciphertext."""
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(ciphertext).decode(), base64.b64encode(nonce).decode()


def decrypt_message(ciphertext_b64: str, nonce_b64: str) -> str:
    """Raises cryptography.exceptions.InvalidTag if data was tampered with."""
    ciphertext = base64.b64decode(ciphertext_b64)
    nonce = base64.b64decode(nonce_b64)
    return aesgcm.decrypt(nonce, ciphertext, None).decode()


# ─── Per-User Signing Keys (Authenticity) ───
def get_or_create_keypair(username: str) -> Ed25519PrivateKey:
    """Load an existing Ed25519 keypair for this username, or generate a new one.
    Private key persists to keys/<username>.pem so identity survives reconnects.
    Public key is stored in the DB so anyone can verify this sender's signatures.
    """
    path = os.path.join(KEYS_DIR, f"{username}.pem")

    if os.path.exists(path):
        with open(path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
    else:
        private_key = Ed25519PrivateKey.generate()
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        with open(path, "wb") as f:
            f.write(pem)

    public_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    public_b64 = base64.b64encode(public_bytes).decode()

    with db_lock:
        conn.execute(
            "INSERT OR REPLACE INTO signing_keys(username, public_key) VALUES (?, ?)",
            (username, public_b64),
        )
        conn.commit()

    return private_key


def sign_message(username: str, plaintext: str) -> str:
    signature = signing_keys[username].sign(plaintext.encode())
    return base64.b64encode(signature).decode()


def verify_message(username: str, plaintext: str, signature_b64: str) -> bool:
    cursor = conn.execute(
        "SELECT public_key FROM signing_keys WHERE username = ?", (username,)
    )
    row = cursor.fetchone()
    if not row:
        return False
    public_key = Ed25519PublicKey.from_public_bytes(base64.b64decode(row[0]))
    try:
        public_key.verify(base64.b64decode(signature_b64), plaintext.encode())
        return True
    except InvalidSignature:
        return False


# ─── Persistence Helpers ───
def save_message(room_id: str, sender: str, ciphertext: str, nonce: str, signature: str):
    with db_lock:
        conn.execute(
            """INSERT INTO messages(room_id, sender, ciphertext, nonce, signature, timestamp)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (room_id, sender, ciphertext, nonce, signature, datetime.now().isoformat()),
        )
        conn.commit()


def get_history(room_id: str) -> list[dict]:
    """Retrieve -> Decrypt -> Verify for every stored message.
    Detects both ciphertext tampering (AES-GCM tag) and signature forgery.
    """
    cursor = conn.execute(
        """SELECT sender, ciphertext, nonce, signature, timestamp
           FROM messages WHERE room_id = ? ORDER BY id""",
        (room_id,),
    )
    rows = cursor.fetchall()

    history = []
    for sender, ciphertext, nonce, signature, timestamp in rows:
        tampered = False
        try:
            text = decrypt_message(ciphertext, nonce)
        except InvalidTag:
            text = "[TAMPER DETECTED: ciphertext/authentication tag invalid]"
            tampered = True

        signature_valid = False if tampered else verify_message(sender, text, signature)

        history.append({
            "username": sender,
            "text": text,
            "timestamp": datetime.fromisoformat(timestamp).strftime("%H:%M:%S"),
            "tampered": tampered,
            "signature_valid": signature_valid,
        })
    return history


# ─── HTTP Routes ───
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return {
        "status": "ok",
        "connected_users": len(connected_users),
        "users": get_user_list(),
        "stored_messages": conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0],
    }


# ─── SocketIO Events ────
@socketio.on("connect")
def on_connect():
    log.info(f"New connection: {request.sid}")


@socketio.on("join")
def on_join(data: dict):
    sid = request.sid
    username = str(data.get("username", "")).strip()

    if not username:
        emit("error", {"message": "Username cannot be empty."})
        return
    if len(username) > 20:
        emit("error", {"message": "Username must be 20 characters or fewer."})
        return
    if username in get_user_list():
        emit("error", {"message": f'Username "{username}" is already taken.'})
        return

    connected_users[sid] = {"username": username}
    join_room(ROOM)

    # Load (or create) this sender's signing identity
    signing_keys[username] = get_or_create_keypair(username)

    log.info(f"JOIN  | {username} ({sid})")

    emit("joined", {
        "username": username,
        "users": get_user_list(),
        "timestamp": now(),
    })

    # Persistence requirement: send decrypted + verified chat history on join
    emit("history", {"messages": get_history(ROOM)})

    emit("user_joined", {
        "username": username,
        "users": get_user_list(),
        "timestamp": now(),
    }, to=ROOM, include_self=False)


@socketio.on("message")
def on_message(data: dict):
    sid = request.sid
    user = connected_users.get(sid)
    if not user:
        emit("error", {"message": "You must join the chat first."})
        return

    text = str(data.get("text", "")).strip()
    if not text:
        return
    if len(text) > 500:
        emit("error", {"message": "Message too long (max 500 chars)."})
        return

    username = user["username"]

    # Encrypt -> Sign -> Store  (persistence + confidentiality + integrity + authenticity)
    ciphertext, nonce = encrypt_message(text)
    signature = sign_message(username, text)
    save_message(ROOM, username, ciphertext, nonce, signature)

    log.info(f"MSG   | {username}: {text[:60]}")

    # Broadcast the plaintext in real time (sender is trusted at send-time;
    # anyone re-reading history later gets the decrypt+verify treatment above)
    emit("message", {
        "username": username,
        "text": text,
        "timestamp": now(),
        "sid": sid,
        "signature_valid": True,
        "tampered": False,
    }, to=ROOM)


@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    user = connected_users.pop(sid, None)
    if user:
        username = user["username"]
        log.info(f"LEAVE | {username} ({sid})")
        emit("user_left", {
            "username": username,
            "users": get_user_list(),
            "timestamp": now(),
        }, to=ROOM)
    else:
        log.info(f"DISCONNECT (unauthenticated): {sid}")


@socketio.on("typing")
def on_typing(data: dict):
    sid = request.sid
    user = connected_users.get(sid)
    if user:
        emit("typing", {
            "username": user["username"],
            "is_typing": data.get("is_typing", False),
        }, to=ROOM, include_self=False)


# ─── Entry Point ───
if __name__ == "__main__":
    print("=" * 55)
    print("  Secure Persistent Group Chat Server")
    print(f"  Database : {DB_PATH}")
    print(f"  AES key  : {KEY_FILE}")
    print(f"  Sign keys: {KEYS_DIR}/")
    print("  Running on http://0.0.0.0:5000")
    print("=" * 55)
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, allow_unsafe_werkzeug=True)
