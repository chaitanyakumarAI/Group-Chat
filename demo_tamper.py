"""
Demo Tamper Script for Assignment 4 Verification
Tampers with 1 byte of AES-GCM ciphertext in chat.db to demonstrate Tamper Detection.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chat.db")

def tamper_message():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} does not exist. Run the server first and send a message.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, sender, ciphertext FROM messages ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()

    if not row:
        print("No messages found in chat.db to tamper with.")
        conn.close()
        return

    msg_id, sender, ciphertext = row
    # Corrupt last character of base64 ciphertext
    corrupted_char = 'Z' if ciphertext[-1] != 'Z' else 'A'
    tampered_ciphertext = ciphertext[:-1] + corrupted_char

    cursor.execute("UPDATE messages SET ciphertext = ? WHERE id = ?", (tampered_ciphertext, msg_id))
    conn.commit()
    conn.close()

    print("=" * 60)
    print(f"SUCCESSFULLY TAMPERED WITH MESSAGE ID: {msg_id} (Sender: {sender})")
    print(f"Original Ciphertext : {ciphertext}")
    print(f"Tampered Ciphertext : {tampered_ciphertext}")
    print("When you refresh the chat or load history, server will flag:")
    print("[TAMPER DETECTED: ciphertext/authentication tag invalid]")
    print("=" * 60)

if __name__ == "__main__":
    tamper_message()