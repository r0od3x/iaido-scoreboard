# Iaido Scoreboard

A full-screen scoreboard for **iaido competitions**, built with Python and Tkinter.
It is designed to be driven entirely from the keyboard by a table official and shown on a
TV or projector: the screen is split into a **red** half and a **white** half, each with the
competitor's name and their own timer.

## Features

- **Solo match** — one red vs one white competitor
- **Team match** — N vs N series (3v3 by default) with automatic round progression
  and a final series result (winner or draw)
- Independent timers for each side, pause / resume
- Animated full-screen round-winner and series-winner announcements with the judges' score (3-0 / 2-1)
- **Undo** the last round decision
- Configurable team size, font, labels, animation duration and credit text

## Keyboard controls

| Key | Action |
|---|---|
| `2` | Select score **2 - 1** |
| `3` | Select score **3 - 0** |
| `R` | Award the selected score to **Red** |
| `W` | Award the selected score to **White** |
| `4` | Start / pause the **red** timer |
| `5` | Start / pause the **white** timer |
| `Z` | Undo the last round |
| `Esc` | Close an announcement / return to the home screen |
| `Q` | Quit (outside text fields) |

Workflow for a round: press `2` or `3` to choose the decision, then `R` or `W` for the winner.

## Running

Requirements: **Python 3.8+** (Tkinter is included with the standard Windows/macOS installers).

```bash
python iaido.py
```

## Configuration

Copy `config.example.json` to `config.json` next to `iaido.py` (or next to `iaido.exe`) and edit it.
Every key is optional.

| Key | Description | Default |
|---|---|---|
| `team_size` | Players per team in team mode | `3` |
| `font_family` | Font used everywhere | `Arial` |
| `round_overlay_ms` | How long a round-winner announcement stays up (ms) | `3000` |
| `red_label` / `white_label` | Names used when a name field is left empty | `Red` / `White` |
| `credit_text` | Small credit line on the home screen | `Made by Ghalbi Mohamed Reda` |

## Building a Windows executable

```bash
pip install pyinstaller
pyinstaller iaido.spec          # output: dist/iaido.exe (uses myicon.ico)
```

Build outputs are not committed; attach `dist/iaido.exe` to a GitHub Release to distribute it.
