# Real-Time Group Chat Application Architecture Report

## General Information
- **Course:** Computer System Design (CSD)
- **Assignment:** Assignment 4 — Real-Time Group Chat Application using WebSockets
- **Host SSH Machine:** `student@10.1.75.51` (Port `2237`)
- **Internal Server Port:** `5000`
- **Official Public Testing URL:** **`http://10.1.75.51:5237/`**
- **GitHub Repository:** [https://github.com/chaitanyakumarAI/Group-Chat](https://github.com/chaitanyakumarAI/Group-Chat)

---

## 👨‍💻 Group Team Members & Server Allotment

| Role / Designation | Student Member Name | Roll Number | SSH Connection Command | Mapped Public Access URL |
|---|---|---|---|---|
| **Group Head (Host Server)** | **Ranga Chandra Naga Venkata Chaitanya Kumar** | **12341740** | `ssh -p 2237 student@10.1.75.51` | `http://10.1.75.51:5237/` |
| **Member 2** | **Bhukya Raju** | **12340520** | `ssh -p 2238 student@10.1.75.51` | `http://10.1.75.51:5237/` |
| **Member 3** | **V.G.N. Harshitha** | **12342310** | `ssh -p 2239 student@10.1.75.51` | `http://10.1.75.51:5237/` |
| **Member 4** | **Maloth Madhu** | **12341370** | `ssh -p 2240 student@10.1.75.51` | `http://10.1.75.51:5237/` |

---

## 1. Executive Summary & Port Mapping
This project implements a multi-user, real-time Group Chat Application for **Computer System Design (CSD) Assignment 4**. Built using **Flask**, **Flask-SocketIO**, and **SQLite** persistence, it incorporates **AES-256-GCM encryption** and **Ed25519 digital signatures** for security and authenticity.

### ⚠️ Laboratory Network & Port Forwarding Details
- The Flask backend process binds internally to port `5000` (`0.0.0.0:5000`).
- The laboratory network router forwards SSH port `2237` traffic to public HTTP port **`5237`**.
- Therefore, all TAs and team members access the live application at:
  👉 **`http://10.1.75.51:5237/`**

---

## 2. Core Features & Requirement Verification Matrix
- **Real-Time Communication**: Bi-directional WebSocket event broadcasting via Flask-SocketIO.
- **Join/Leave Notifications**: System pills indicating when users join or leave the chat room.
- **User Identification**: Unique username enforcement with dynamic gradient avatar generation.
- **Graceful Disconnection Cleanup**: Connection tracking and cleanup when browser tabs close.
- **SQLite Persistence**: Chat history saved to `chat.db` and auto-rendered on reconnect.
- **Confidentiality (AES-256-GCM)**: Payload encrypted with room key prior to database insertion.
- **Authenticity (Ed25519)**: Cryptographic digital signature generated per sender and verified on read.

---

## 3. Database Inspection Commands (SSH Server Host)
To inspect stored encrypted messages and signatures in SQLite:
```bash
sqlite3 ~/chat_app/chat.db "SELECT id, sender, ciphertext, signature, timestamp FROM messages;"
```

To verify stored user public keys:
```bash
sqlite3 ~/chat_app/chat.db "SELECT username, public_key FROM signing_keys;"
```
