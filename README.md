# 🎮 Tic Tac Toe — Notebook Edition

A clean and interactive **Tic Tac Toe** game with a notebook-inspired interface, single-player AI, local multiplayer, and online multiplayer.

🎮 **Play Online:** https://owlttt.netlify.app/  
💻 **GitHub:** https://github.com/sunnyptl95/tic-toc-toe

---

## ✨ Features

- 🤖 **Single Player**
  - Play against an AI opponent
  - Multiple difficulty levels
  - Minimax-based gameplay for challenging matches

- 👥 **Local Multiplayer**
  - Two players can play on the same device

- 🌐 **Online Multiplayer**
  - Create a private game room
  - Share the room code with another player
  - Real-time moves using WebSockets
  - Supports two players per room

- 📊 **Game Statistics**
  - Track wins, losses, and draws
  - Statistics are stored locally in the browser

- 🔊 **Sound Effects**
  - Interactive audio feedback during gameplay

- 📱 **Responsive Design**
  - Works on desktop and mobile screens

- 📓 **Notebook-Inspired UI**
  - Handwritten/notebook-style visual experience

---

## 🎮 Game Modes

### 🤖 Single Player

Challenge the computer in different difficulty levels.

The game uses a minimax-based AI system to make strategic moves.

### 👥 Local Multiplayer

Play against a friend on the same device.

Player X and Player O take turns on the same board.

### 🌐 Online Multiplayer

Play against another player over the internet.

The online system uses:

```text
Frontend
   │
   ▼
Netlify
   │
   │ HTTP / WebSocket
   ▼
FastAPI Backend
   │
   ▼
Game Rooms
```

Each room receives a unique room code that players can use to join the same game.

---

## 🛠️ Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- SVG
- Local Storage
- WebSocket Client

### Backend

- Python
- FastAPI
- Uvicorn
- WebSockets

### Deployment

- **Frontend:** Netlify
- **Backend:** Render

---

## 📂 Project Structure

```text
tic-toc-toe/
│
├── index.html
│
├── server.py
│
├── requirements.txt
│
└── README.md
```

### `index.html`

Contains the complete frontend game interface, styling, game logic, AI, local multiplayer, statistics, and online multiplayer client.

### `server.py`

FastAPI backend responsible for:

- Creating game rooms
- Managing connected players
- WebSocket communication
- Broadcasting moves
- Handling resets
- Handling player disconnections

### `requirements.txt`

Backend dependencies:

```text
fastapi==0.115.0
uvicorn[standard]==0.30.6
```

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/sunnyptl95/tic-toc-toe.git
cd tic-toc-toe
```

### 2. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the backend

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

### 4. Open the frontend

Open:

```text
index.html
```

in your browser.

---

## 🌐 Online Multiplayer Architecture

The project separates the frontend and backend.

```text
                  ┌──────────────────┐
                  │     Player 1     │
                  └────────┬─────────┘
                           │
                           │
                  ┌────────▼─────────┐
                  │     Netlify      │
                  │    Frontend      │
                  └────────┬─────────┘
                           │
                    WebSocket / HTTP
                           │
                  ┌────────▼─────────┐
                  │      Render      │
                  │   FastAPI Server │
                  └────────┬─────────┘
                           │
                    ┌──────┴──────┐
                    │             │
              ┌─────▼─────┐ ┌─────▼─────┐
              │  Player 1 │ │  Player 2 │
              │     X     │ │     O     │
              └───────────┘ └───────────┘
```

### Room Flow

1. Player creates a room.
2. Backend generates a room code.
3. Player shares the code.
4. Second player joins using the code.
5. Backend establishes the WebSocket connections.
6. Moves are synchronized in real time.
7. Both players receive game updates.

---

## 🔌 API

### Create Room

```http
GET /new-room
```

Creates a new multiplayer room and returns a room code.

### Health Check

```http
GET /
```

Returns the backend status and active room information.

### WebSocket

```text
/ws/{room_code}
```

Used for real-time multiplayer communication.

---

## ☁️ Deployment

### Frontend — Netlify

The frontend can be deployed as a static website.

Current live version:

**https://owlttt.netlify.app/**

### Backend — Render

Deploy `server.py` as a Python Web Service.

Build dependencies:

```text
pip install -r requirements.txt
```

Start command:

```bash
uvicorn server:app --host 0.0.0.0 --port $PORT
```

After deploying the backend, make sure the frontend WebSocket/API configuration points to the Render backend URL.

---

## 🔐 Environment Variables

The backend can use:

```text
PUBLIC_URL=https://your-service.onrender.com
```

The server can use this URL for its self-ping mechanism while the instance is running.

Optional:

```text
SELF_PING_INTERVAL=300
```

The value is measured in seconds.

> Note: Self-pinging cannot guarantee that a completely spun-down free hosting instance will stay awake.

---

## 📱 Browser Support

The game is designed to work on modern browsers supporting:

- JavaScript
- WebSockets
- Local Storage
- SVG
- CSS3

Recommended browsers:

- Chrome
- Edge
- Firefox
- Safari

---

## 🗺️ Roadmap

Possible future improvements:

- [ ] Spectator mode
- [ ] Online player names
- [ ] Rematch button
- [ ] Improved matchmaking
- [ ] Persistent online statistics
- [ ] Leaderboard
- [ ] More AI difficulty options
- [ ] Custom game themes
- [ ] Room expiration and cleanup
- [ ] Improved mobile UI

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/my-feature
```

3. Make your changes
4. Commit your changes

```bash
git commit -m "Add my feature"
```

5. Push the branch

```bash
git push origin feature/my-feature
```

6. Open a Pull Request

---

## 👨‍💻 Author

**Sunny**

GitHub:  
https://github.com/sunnyptl95

---

## 📄 License

No license has currently been specified for this repository.

If you want others to legally reuse, modify, or distribute the project, consider adding an appropriate open-source license.

---

## ⭐ Support

If you like the project, consider giving the repository a ⭐ on GitHub.

**Play the game:**  
🎮 https://owlttt.netlify.app/

**Source code:**  
💻 https://github.com/sunnyptl95/tic-toc-toe