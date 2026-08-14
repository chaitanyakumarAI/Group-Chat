"""
Real-Time Group Chat Application - Backend Server
Flask + Flask-SocketIO (WebSockets)
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import logging

# ─── App Configuration ───────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = "groupchat_secret_key_2024"

# Allow all origins for LAN testing across lab machines
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    logger=False,
    engineio_logger=False,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ─── In-Memory State ─────────────────────────────────────────────────────────
# {sid: {"username": str, "joined_at": str}}
connected_users: dict[str, dict] = {}

ROOM = "general"  # single chat room for all users


def get_user_list() -> list[str]:
    return [u["username"] for u in connected_users.values()]


def now() -> str:
    return datetime.now().strftime("%H:%M:%S")


# ─── HTTP Routes ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    """Serve the chat client."""
    return render_template("index.html")


@app.route("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "connected_users": len(connected_users),
        "users": get_user_list(),
    }


# ─── SocketIO Events ─────────────────────────────────────────────────────────
@socketio.on("connect")
def on_connect():
    sid = request.sid
    log.info(f"New connection: {sid}")
    # Don't add to users yet — wait for 'join' event with username


@socketio.on("join")
def on_join(data: dict):
    """Client sends username to join the chat room."""
    sid = request.sid
    username = str(data.get("username", "")).strip()

    # ── Validate username ──
    if not username:
        emit("error", {"message": "Username cannot be empty."})
        return

    if len(username) > 20:
        emit("error", {"message": "Username must be 20 characters or fewer."})
        return

    # ── Check for duplicate names ──
    existing = get_user_list()
    if username in existing:
        emit("error", {"message": f'Username "{username}" is already taken.'})
        return

    # ── Register user ──
    connected_users[sid] = {"username": username, "joined_at": now()}
    join_room(ROOM)

    log.info(f"JOIN  | {username} ({sid})")

    # Acknowledge to the joining client
    emit("joined", {
        "username": username,
        "users": get_user_list(),
        "timestamp": now(),
    })

    # Notify everyone else in the room
    emit("user_joined", {
        "username": username,
        "users": get_user_list(),
        "timestamp": now(),
    }, to=ROOM, include_self=False)


@socketio.on("message")
def on_message(data: dict):
    """Broadcast a chat message to the whole room."""
    sid = request.sid
    user = connected_users.get(sid)

    if not user:
        emit("error", {"message": "You must join the chat first."})
        return

    text = str(data.get("text", "")).strip()
    if not text:
        return  # silently ignore blank messages

    if len(text) > 500:
        emit("error", {"message": "Message too long (max 500 chars)."})
        return

    payload = {
        "username": user["username"],
        "text": text,
        "timestamp": now(),
        "sid": sid,  # let client know its own messages
    }

    log.info(f"MSG   | {user['username']}: {text[:60]}")
    emit("message", payload, to=ROOM)


@socketio.on("disconnect")
def on_disconnect():
    """Handle client disconnection gracefully."""
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
    """Broadcast typing indicator (non-persistent)."""
    sid = request.sid
    user = connected_users.get(sid)
    if user:
        emit("typing", {
            "username": user["username"],
            "is_typing": data.get("is_typing", False),
        }, to=ROOM, include_self=False)


# ─── Entry Point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  Real-Time Group Chat Server")
    print("  Running on http://0.0.0.0:5000")
    print("  Share your LAN IP with teammates!")
    print("=" * 55)
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, allow_unsafe_werkzeug=True)
