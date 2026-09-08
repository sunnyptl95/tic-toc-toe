"""
Tic Tac Toe — Online Multiplayer Backend
Deploy this on Render as a Web Service.

Start command: uvicorn server:app --host 0.0.0.0 --port $PORT
"""

import asyncio
import random
import string
import os
from urllib.request import urlopen
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Optional Render self-ping.
# Set PUBLIC_URL to your deployed Render URL.
# Example: https://your-game-backend.onrender.com
SELF_PING_INTERVAL = int(os.getenv("SELF_PING_INTERVAL", "600"))  # 10 minutes
PUBLIC_URL = os.getenv("PUBLIC_URL", "").rstrip("/")


async def self_ping():
    """Periodically ping the public health endpoint while the server is running.

    This helps keep an already-running instance active, but cannot wake a
    completely spun-down Render instance by itself.
    """
    if not PUBLIC_URL:
        print("[self-ping] PUBLIC_URL not set; self-ping disabled.")
        return

    url = PUBLIC_URL + "/"
    while True:
        try:
            await asyncio.to_thread(urlopen, url, timeout=10)
            print(f"[self-ping] OK -> {url}")
        except Exception as exc:
            print(f"[self-ping] failed: {exc}")
        await asyncio.sleep(SELF_PING_INTERVAL)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(self_ping())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# room_code -> {"players": [WebSocket, ...], "board": [...], "turn": "X"}
rooms = {}


def generate_code():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=5))


@app.get("/")
def health():
    return {
        "status": "ok",
        "rooms_active": len(rooms),
        "self_ping": bool(PUBLIC_URL),
    }


@app.get("/new-room")
def new_room():
    code = generate_code()
    while code in rooms:
        code = generate_code()
    return {"room_code": code}


@app.websocket("/ws/{room_code}")
async def ws_endpoint(websocket: WebSocket, room_code: str):
    await websocket.accept()

    room = rooms.setdefault(room_code, {"players": [], "board": [None] * 9, "turn": "X"})

    if len(room["players"]) >= 2:
        await websocket.send_json({"type": "error", "message": "Room is full"})
        await websocket.close()
        return

    symbol = "X" if len(room["players"]) == 0 else "O"
    room["players"].append(websocket)

    await websocket.send_json({
        "type": "joined",
        "symbol": symbol,
        "board": room["board"],
        "turn": room["turn"],
    })

    if len(room["players"]) == 2:
        for p in room["players"]:
            await p.send_json({"type": "start", "board": room["board"], "turn": room["turn"]})

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") == "move":
                idx = data.get("index")
                if (
                    idx is not None
                    and 0 <= idx < 9
                    and room["board"][idx] is None
                    and room["turn"] == symbol
                ):
                    room["board"][idx] = symbol
                    room["turn"] = "O" if symbol == "X" else "X"
                    for p in room["players"]:
                        await p.send_json({
                            "type": "update",
                            "board": room["board"],
                            "turn": room["turn"],
                            "lastMove": idx,
                            "player": symbol,
                        })

            elif data.get("type") == "reset":
                room["board"] = [None] * 9
                room["turn"] = "X"
                for p in room["players"]:
                    await p.send_json({
                        "type": "reset",
                        "board": room["board"],
                        "turn": room["turn"],
                    })

    except WebSocketDisconnect:
        if websocket in room["players"]:
            room["players"].remove(websocket)
        for p in room["players"]:
            await p.send_json({"type": "opponent-left"})
        if not room["players"]:
            rooms.pop(room_code, None)
