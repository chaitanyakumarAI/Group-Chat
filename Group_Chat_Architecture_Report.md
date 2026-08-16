# Real-Time Group Chat Application Architecture Report

## General Information
- **Course:** Computer System Design (CSD)
- **Assignment:** Assignment 4 — Real-Time Group Chat Application using WebSockets
- **Host SSH Machine:** `student@10.1.75.51` (Port `2237`)
- **Internal Server Port:** `5000`
- **Official Public Testing URL:** **`http://10.1.75.51:5237/`**
- **GitHub Repository:** [https://github.com/chaitanyakumarAI/Group-Chat](https://github.com/chaitanyakumarAI/Group-Chat)

---

## 👨‍💻 Group Team Members & Individual Technical Contributions

| Role / Designation | Student Member Name | Roll Number | SSH Command | Key Technical Contribution |
|---|---|---|---|---|
| **Group Head (Host Server)** | **Ranga Chandra Naga Venkata Chaitanya Kumar** | **12341740** | `ssh -p 2237 student@10.1.75.51` | Backend Architecture, Flask-SocketIO Core, AES-256-GCM Encryption & Ed25519 Signature Pipeline, SSH Daemon. |
| **Member 2** | **Bhukya Raju** | **12340520** | `ssh -p 2238 student@10.1.75.51` | Front-End UI Design, Cyberpunk Aurora Glassmorphism Theme, Socket.IO Client Event Listeners, Dynamic Avatar Generator. |
| **Member 3** | **V.G.N. Harshitha** | **12342310** | `ssh -p 2239 student@10.1.75.51` | Database Schema Architecture (`chat.db`), SQLite Message Persistence Engine, Reconnection State Management & History Pre-loading. |
| **Member 4** | **Maloth Madhu** | **12341370** | `ssh -p 2240 student@10.1.75.51` | Multi-Client Integration & Testing across SSH Machines (`10.1.75.51:5237`), Graceful Disconnection Handling, SQLite Inspection Scripts. |

### Detailed Task Responsibilities:
- **Ranga Chandra Naga Venkata Chaitanya Kumar (12341740)**: Designed the core Flask-SocketIO architecture, implemented server-side room management, integrated AES-256-GCM symmetric encryption and per-user Ed25519 digital signature signing/verification, and managed SSH server deployment on `student@10.1.75.51:2237`.
- **Bhukya Raju (12340520)**: Developed the single-page responsive UI using HTML5, CSS3, and JavaScript, designed the Cyberpunk Aurora dark-mode glassmorphic theme with glowing ambient mesh blobs, and created dynamic user avatar color generators.
- **V.G.N. Harshitha (12342310)**: Architected the SQLite database layer (`chat.db`) with tables for messages and user public keys, implemented message history pre-loading on user join, and ensured data integrity during server restarts.
- **Maloth Madhu (12341370)**: Executed end-to-end integration testing across 4 lab client SSH machines, verified port forwarding (`5000` -> `5237`), implemented edge-case socket disconnection handling, and documented SQLite database inspection queries.

---

## 🖼️ Application Screenshots & Visual Proof Placeholders

> 📸 **Screenshot 1 Placeholder:** Real-Time Chat Interface on `http://10.1.75.51:5237/` showing multi-user chat, dynamic avatars, and live typing indicator  
> `[ Paste Screenshot Here ]`

> 📸 **Screenshot 2 Placeholder:** User Join Modal & Unique Username Validation Screen  
> `[ Paste Screenshot Here ]`

> 📸 **Screenshot 3 Placeholder:** Terminal output of SQLite database inspection showing stored AES-256-GCM encrypted messages & Ed25519 signatures  
> `[ Paste Screenshot Here ]`

> 📸 **Screenshot 4 Placeholder:** SSH Host Background Daemon Process Running (`nohup python3 server.py`) on `student@10.1.75.51:2237`  
> `[ Paste Screenshot Here ]`

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
