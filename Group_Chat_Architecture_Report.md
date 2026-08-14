# Laboratory Tutorial: Real-Time Group Chat Application

## Group Details & Submission Summary
- **Target Audience / TAs Review**: Multi-User Laboratory WebSocket Testing
- **Group Allotted SSH Servers**:
  - **Student 1 (Host Machine)**: `ssh -p 2237 student@10.1.75.51`
  - **Student 2 Client**: `ssh -p 2238 student@10.1.75.51`
  - **Student 3 Client**: `ssh -p 2239 student@10.1.75.51`
  - **Student 4 Client**: `ssh -p 2240 student@10.1.75.51`
- **Group Head Submission**: Complete Source Code & Technical Architecture Documentation
- **Group Registration Form**: [Submitted / Verified via Link](https://forms.gle/VHHzfSLmPhZQZ9rLA)
- **Backend Technology Stack**: Python 3, Flask, Flask-SocketIO (WebSockets / Engine.IO)
- **Frontend Technology Stack**: HTML5, CSS3 (Glassmorphic Modern UI), Modern JavaScript (Socket.IO v4 Client API)
- **Client Testing URL (TAs & All Students)**: **`http://10.1.75.51:5000`**

---

## 1. System Architecture & Component Diagram

```
                       +-----------------------------------+
                       |    Student 1 SSH Server (Host)    |
                       |    (ssh -p 2237 student@10.1.75.51)|
                       |  (Flask + Flask-SocketIO Core)   |
                       |         Public IP / Port:         |
                       |      http://10.1.75.51:5000      |
                       +-----------------+-----------------+
                                         |
             +---------------------------+---------------------------+
             |                           |                           |
             v                           v                           v
  +--------------------+      +--------------------+      +--------------------+
  |   Student 2 SSH    |      |   Student 3 SSH    |      |   Student 4 SSH    |
  | (-p 2238 Client)   |      | (-p 2239 Client)   |      | (-p 2240 Client)   |
  | (Browser Session)  |      | (Browser Session)  |      | (Browser Session)  |
  +--------------------+      +--------------------+      +--------------------+
                                         |
                                         v
                              +--------------------+
                              |  TA / Evaluator    |
                              | (Browser Session)  |
                              +--------------------+
```

### Architecture Highlights:
1. **Full-Duplex Communication**: Utilizes native WebSockets (with automatic long-polling fallback) via Flask-SocketIO for persistent, bi-directional communication between the central host SSH server (`10.1.75.51:2237`) and all 4 concurrent student SSH clients.
2. **Centralized Broadcast Engine**: A single backend server instance maintains active connection session identifiers (`sid`) in an in-memory dictionary (`connected_users`), managing state and room memberships.
3. **Event-Driven Pipeline**:
   - `join`: Registers username, validates duplicate names, and broadcasts `user_joined` event to all active room members.
   - `message`: Receives text payload from a client and immediately relays (`emit`) it to all clients connected to the `"general"` room.
   - `disconnect`: Detects connection drops automatically (close tab, network drop, process kill) and triggers `user_left` broadcast.
   - `typing`: Broadcasts transient typing state to present real-time interaction feedback.

---

## 2. Minimum Requirements & Verification Matrix

| Requirement | Implementation Detail | Status |
| :--- | :--- | :---: |
| **Real-time Message Broadcasting** | Handled via `socketio.emit('message', data, to='general')`. All connected clients receive incoming text instantly without page refreshes. | ✅ Complete |
| **User Join / Leave Notifications** | Server emits `user_joined` and `user_left` events on socket connect/disconnect. UI renders system notification pills. | ✅ Complete |
| **Unique Username Identification** | Server checks existing user list upon `join` event; rejects duplicates and alerts client via `error` socket event. | ✅ Complete |
| **Graceful Handling of Client Disconnections** | Clean socket cleanup via `@socketio.on('disconnect')` removing `sid` entry and updating online member count dynamically. | ✅ Complete |
| **4 Simultaneous Clients Support** | Tested across SSH instances (ports 2237, 2238, 2239, 2240) communicating via host `http://10.1.75.51:5000`. | ✅ Complete |

---

## 3. SSH Server Deployment Commands

### Step 1: Deploy to Student 1 Host SSH (`port 2237`)
Run from your computer:
```bash
scp -P 2237 -r E:\CSD\chat_app student@10.1.75.51:~/chat_app
```

### Step 2: SSH into Host Machine & Run Backend
```bash
ssh -p 2237 student@10.1.75.51
cd ~/chat_app
pip install -r requirements.txt
nohup python3 server.py > server.log 2>&1 &
```

### Step 3: Access Chat App for All 4 Students & TAs
Open any web browser and go to:
```text
http://10.1.75.51:5000
```
*(All 4 students on ports 2237, 2238, 2239, and 2240 connect to this URL to chat together in real time).*
