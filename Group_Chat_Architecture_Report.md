# Real-Time Group Chat Application Architecture Report

## General Information
- **Course Assignment:** Real-Time Group Chat Application using WebSockets
- **Host Machine:** `student@10.1.75.51` (SSH Port: `2237`)
- **Internal Backend Port:** `5000`
- **Official Testing Public URL:** **`http://10.1.75.51:5237/`**
- **GitHub Repository:** [https://github.com/chaitanyakumarAI/Group-Chat](https://github.com/chaitanyakumarAI/Group-Chat)

---

## 1. Executive Summary & Port Mapping
This project implements a multi-user, real-time Group Chat Application using **Flask**, **Flask-SocketIO**, and **SQLite** persistence, enhanced with **AES-256-GCM encryption** and **Ed25519 digital signatures**.

### ⚠️ Network & Port Forwarding Note
- The Flask-SocketIO backend listens internally on port `5000` (`0.0.0.0:5000`).
- The laboratory NAT router forwards SSH port `2237` traffic to public HTTP port **`5237`**.
- Therefore, all TAs and clients access the live application at:
  👉 **`http://10.1.75.51:5237/`**

---

## 2. Group Allocation & SSH Server Details
| Team Member | SSH Connection Command | Access Method |
|---|---|---|
| **Member 1 (Group Head / Host)** | `ssh -p 2237 student@10.1.75.51` | Hosts backend server |
| **Member 2** | `ssh -p 2238 student@10.1.75.51` | Accesses `http://10.1.75.51:5237/` |
| **Member 3** | `ssh -p 2239 student@10.1.75.51` | Accesses `http://10.1.75.51:5237/` |
| **Member 4** | `ssh -p 2240 student@10.1.75.51` | Accesses `http://10.1.75.51:5237/` |

---

## 3. Core Features & Verification Matrix
- **Real-Time Communication**: Bi-directional WebSocket broadcasting.
- **Join/Leave Notifications**: Live arrival and departure notification pills.
- **User Identification**: Unique username enforcement with dynamic avatars.
- **Graceful Disconnection**: Socket cleanup on browser disconnect.
- **SQLite Message Persistence**: Messages saved in `chat.db` and auto-loaded on reconnect.
- **AES-256-GCM Encryption**: Payloads encrypted before storage in SQLite.
- **Ed25519 Digital Signatures**: Cryptographic verification per message sender.

---

## 4. SQLite Database Inspection Command
To verify stored encrypted messages and signatures on the host SSH server:
```bash
sqlite3 ~/chat_app/chat.db "SELECT id, sender, ciphertext, signature, timestamp FROM messages;"
```

To verify stored user public keys:
```bash
sqlite3 ~/chat_app/chat.db "SELECT username, public_key FROM signing_keys;"
```
