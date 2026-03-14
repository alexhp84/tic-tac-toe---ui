# 🚀 Hitchhiker's Guide to Tic-Tac-Toe

> *"Here I am, brain the size of a planet, and you ask me to play Tic-Tac-Toe."*
> — Marvin the Paranoid Android

A Hitchhiker's Guide to the Galaxy themed Tic-Tac-Toe game built in Python with a full pygame UI. Play against a friend or challenge Marvin the Paranoid Android, who will beat you whilst complaining about it.

---

## 📸 Features

- 🤖 **Play against Marvin** — the depressed robot with a Genuine People Personality, who will win, lose, and draw with equal amounts of misery
- 👥 **Human vs Human** — two players on the same machine
- 🎨 **Full pygame UI** — randomised Hitchhiker's Guide themed backgrounds, Vogon and Don't Panic icons, Harlow Solid font throughout
- 🎙️ **Marvin quotes** — on greeting, each move, wins, losses, draws, and resets
- 🔢 **42 Easter egg** — reach a score of 42 for a surprise
- 🔄 **Abandon Hope** — reset the current board mid-game without losing scores
- 📊 **Persistent scores** — scores carry across games in the same session
- 🖥️ **Single menu screen** — enter names, pick opponent, choose who goes first, all in one place

---

## 🎮 How to Play

- The menu screen collects Player 1's name, opponent choice, optional Player 2 name, and who goes first
- **❌ = Vorgon** (Player 1) &nbsp;|&nbsp; **⭕ = Don't Panic** (Player 2 / Marvin)
- Click a cell on the board to place your piece
- First to get three in a row wins
- Click **Abandon Hope** to reset the current board (scores are kept)
- At the end of each game, choose **Play Again** to return to the menu or **Quit** for the session summary

---

## 🛠️ Requirements

- Python 3.10+
- pygame

```bash
pip install pygame
```

---

## ▶️ Running the Game

```bash
python game_play.py
```

> ⚠️ Always run `game_play.py`, not `game_ui.py`. Running `game_ui.py` directly will redirect you automatically.

---

## 📁 File Structure

```
tic-tac-toe---ui/
│
├── game_play.py            # Game logic and session loop — run this
├── game_ui.py              # All pygame rendering and UI screens
│
├── Harlow Solid Regular.ttf
├── arthur_dent.png         # Background image
├── babel-fish.png          # Background image
├── hitchikers.png          # Background image + menu title
├── restaurant.png          # Background image
├── marvin.png              # Marvin portrait (menu)
├── vorgon.png              # Player 1 icon (❌)
├── dont_panic.png          # Player 2 icon (⭕)
└── magrathea.png
```

---

## 🏗️ Building Executables

Builds for all three platforms are generated automatically via GitHub Actions on every push to `main`. Download the latest builds from the [Releases](../../releases) page:

| Platform | File |
|----------|------|
| 🐧 Linux | `HitchhikersTTT` |
| 🪟 Windows | `HitchhikersTTT.exe` |
| 🍎 macOS | `HitchhikersTTT-macOS.zip` |

### Building manually

```bash
pip install pyinstaller

# Linux / macOS
pyinstaller --onefile --windowed --name HitchhikersTTT \
  --add-data "*.png:." \
  --add-data "Harlow Solid Regular.ttf:." \
  game_play.py

# Windows
pyinstaller --onefile --windowed --name HitchhikersTTT \
  --add-data "*.png;." \
  --add-data "Harlow Solid Regular.ttf;." \
  game_play.py
```

---

## 🌌 Marvin's Moods

Marvin has a quote for every occasion:

| Situation | Sample |
|-----------|--------|
| Greeting | *"I've calculated your chances of winning. They're about as good as a bowl of petunias in a vacuum."* |
| His turn | *"I could calculate the meaning of life, or block your diagonal. Both are equally pointless."* |
| He wins | *"Victory. I'd celebrate, but I've got this terrible pain in all the diodes down my left side."* |
| You win | *"Congratulations. You've beaten a robot with a Genuine People Personality. I hope you're proud."* |
| Draw | *"No one wins. Finally, a result that reflects the true nature of the universe."* |
| Score hits 42 | *"42. I could have told you that millions of years ago if you'd just asked."* |

---

## 📜 Licence

This project is for personal and educational use.  
*Hitchhiker's Guide to the Galaxy* is the creation of Douglas Adams. All character references are used in tribute.

---

> *So long, and thanks for all the fish.* 🐬
