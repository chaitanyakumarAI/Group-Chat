# Real-Time Group Chat Application (Flask + WebSockets + Security)

A real-time, multi-client Group Chat Application built using **Flask**, **Flask-SocketIO (WebSockets)**, and **SQLite**, with end-to-end security enhancements (AES-256-GCM confidentiality and Ed25519 digital signatures).

![UI Theme](https://img.shields.io/badge/UI-Cyberpunk_Glassmorphism-6366f1)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![WebSockets](https://img.shields.io/badge/WebSockets-Flask--SocketIO-emerald)
![Security](https://img.shields.io/badge/Security-AES--256--GCM%20%7C%20Ed25519-purple)

## 🌐 Live Deployment

This app is currently deployed and verified on the allotted lab host:

- **Host**: `stu29_sys1` (`ssh -p 2313 student@10.1.75.51`)
- **Live URL**: `http://10.1.75.51:5313`
- **Full verification log**: see [`TESTING.md`](./TESTING.md) for step-by-step
  confirmation of persistence, encryption, tamper detection, and signature
  verification against this deployment.

---

## 🌟 Key Features
- **Real-Time Message Broadcasting**: Instant bi-directional communication powered by WebSockets.
- **User Join/Leave System Notifications**: Live notification pills when users connect or disconnect.
- **Unique Username Validation**: Prevents duplicate usernames across active sessions.
- **SQLite Message Persistence**: Chat history saved to `chat.db` and auto-loaded upon joining.
- **Confidentiality & Authenticity**: AES-256-GCM message encryption + Ed25519 cryptographic signatures per sender.
- **Aurora Glassmorphism UI**: Dark-mode Cyberpunk aesthetic with ambient glow blobs and dynamic avatar gradients.

---

## 🚀 Allotted SSH Server & Deployment Details

- **Student 1 (Host Server)**: `ssh -p 2313 student@10.1.75.51`
- **Student 2 Client**: `ssh -p 2314 student@10.1.75.51`
- **Student 3 Client**: `ssh -p 2315 student@10.1.75.51`
- **Student 4 Client**: `ssh -p 2316 student@10.1.75.51`
- **Live Client Testing URL**: **`http://10.1.75.51:5313/`** *(Mapped from SSH Port 2313)*
  
---

## 🛠️ Quick Start

### Deploy on Remote SSH Server
```bash
# Clone repository
cd ~
git clone https://github.com/chaitanyakumarAI/Group-Chat.git ~/chat_app
cd ~/chat_app

# Install dependencies
pip install -r requirements.txt

# Start background server process
nohup python3 server.py > server.log 2>&1 &
```

---

## 🔍 Inspecting Database & Signatures on SSH Server
```bash
sqlite3 ~/chat_app/chat.db "SELECT id, sender, ciphertext, signature, timestamp FROM messages;"
```

---

## 📄 Submission Documentation
The repository contains the complete Architecture & Technical Implementation Report:
- [`Group_Chat_Architecture_Report.md`](./Group_Chat_Architecture_Report.md)
- [`Group_Chat_Architecture_Report.pdf`](./Group_Chat_Architecture_Report.pdf)
