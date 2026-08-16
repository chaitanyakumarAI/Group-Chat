"""
Tamper-Detection Demo Helper
-----------------------------
Run this AFTER stopping the server and sending at least one chat message.
It flips a byte inside the stored ciphertext of the most recent message,
directly in the SQLite database — simulating an attacker (or a disk error)
modifying stored data.

Usage:
    1. python3 server.py            # send a message from the browser, then Ctrl+C
    2. python3 demo_tamper.py       # corrupts the last message's ciphertext
    3. python3 server.py            # restart, rejoin -> history shows
                                     #   "⚠ TAMPER DETECTED"
"""

import sqlite3
import base64
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chat.db")

conn = sqlite3.connect(DB_PATH)
row = conn.execute(
    "SELECT id, sender, ciphertext FROM messages ORDER BY id DESC LIMIT 1"
).fetchone()

if not row:
    print("No messages found. Send a chat message first, then re-run this script.")
else:
    msg_id, sender, ciphertext_b64 = row
    raw = bytearray(base64.b64decode(ciphertext_b64))
    raw[0] ^= 0xFF  # flip every bit in the first byte -> corrupts the AES-GCM tag/data
    tampered_b64 = base64.b64encode(bytes(raw)).decode()

    conn.execute("UPDATE messages SET ciphertext = ? WHERE id = ?", (tampered_b64, msg_id))
    conn.commit()

    print(f"Tampered with message id={msg_id} from '{sender}'.")
    print("Restart the server and rejoin the chat to see the tamper warning in history.")

conn.close()