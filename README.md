# Real-Time Group Chat Application (Flask + WebSockets)

A real-time, multi-client Group Chat Application built using **Flask** and **Flask-SocketIO (WebSockets)**, supporting simultaneous communication across multiple laboratory machines and remote SSH servers.

![UI Theme](https://img.shields.io/badge/UI-Cyberpunk_Glassmorphism-6366f1)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![WebSockets](https://img.shields.io/badge/WebSockets-Flask--SocketIO-emerald)

---

## 🌟 Key Features
- **Real-Time Message Broadcasting**: Instant bi-directional communication powered by WebSockets.
- **User Join/Leave System Notifications**: Live notification pills when users connect or disconnect.
- **Unique Username Validation**: Prevents duplicate usernames across active sessions.
- **Graceful Disconnection Handling**: Automatic cleanup when clients close tabs or drop network.
- **Aurora Glassmorphism UI**: Dark-mode Cyberpunk aesthetic with ambient glow blobs and dynamic avatar gradients.
- **Live User Sidebar & Typing Indicator**: Real-time participant counter and typing state.

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
python server.py
```
Open `http://localhost:5000` in your browser.

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


