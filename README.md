# 🚀 Cosmic Drill

A simple 2D space shooter built with **Python and pygame-ce**.

Control your spaceship, dodge incoming enemies, shoot them down, and survive as long as possible while earning points.

This project was developed as a hands-on exercise to improve my Python programming, game logic, and problem-solving skills.

## 🎮 Features

- Spaceship movement with screen boundaries
- Enemy spawning and movement
- Shooting and bullet collision detection
- Health system (3 HP)
- Score tracking
- Game Over screen and restart functionality
- Frame-rate independent movement using delta time (`dt`)

## 🕹️ Controls

| Key | Action |
|---|---|
| A / D | Move left / right |
| SPACE | Start game / Shoot |
| R | Restart after Game Over |

## 🛠️ Tech Stack

- Python 3.13
- pygame-ce
- uv — dependency management
- Git & GitHub

## 🚀 Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/VanilVibecoder/cosmic-drill.git
cd cosmic-drill
```

**2. Install dependencies**

Make sure [uv](https://docs.astral.sh/uv/) is installed.

```bash
uv sync
```

**3. Run the game**

```bash
uv run python main.py
```

## 📚 What I Learned

- Building and managing a game loop
- Handling keyboard input and events
- Working with coordinates and rectangles
- Implementing collision detection
- Managing multiple game objects using lists and dictionaries
- Using delta time for consistent movement
- Implementing game states and restart logic

## 📌 Project Status

**Playable MVP — Completed**

A small educational project focused on learning Python through practical development.