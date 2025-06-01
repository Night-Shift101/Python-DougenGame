# Dungeon Maze Game

## Overview

This is a simple maze-based dungeon game built with Python and Tkinter. The goal is to navigate from the starting tile (“Home”) to a hidden “Room” tile as quickly as possible. A timer tracks your elapsed time, and you can customize the maze through a settings dialog.

## How to Play

**Start:** When you launch the game, an ASCII‐style map is generated, with your player positioned at the center (“Home”).

**Movement:** Use the arrow keys (↑, ↓, ←, →) to move one tile at a time:

Corridors (.) and Home (H) are traversable.

Walls or empty spaces are blocked.

**Objective:** Reach the single “Room” tile (R). Once you step onto R, the game is completed and the timer stops.

**Timer:** The timer (displayed in a separate window) starts on your first move and counts up in MM:SS format.

## Settings

Click the Settings button to open the settings window. There are three options:

### Map Size (integer)

Determines the width/height of the square grid (must be an odd integer ≥ 5).

Larger maps create bigger mazes.

### Connecting Hallways Chance (0.0 – 1.0):

Controls the probability of adding extra corridor connections (“loops”) in the maze.

A value of 0.0 yields a perfect maze (no loops). Higher values add more loops.

### Hard Mode (checkbox):

When enabled, every time you move, the tile you just left turns into an Empty tile (you cannot backtrack).

When disabled, corridors remain intact after you pass through.

After adjusting any of these values, click Save:

The new settings are applied immediately, the maze regenerates, and you’re placed back at Home.

The timer resets to 00:00.

# Requirements

- Python 3.x
- Tkinter (usually included with Python on most platforms)

# Installation & Run

Ensure Python 3 and Tkinter are installed on your system.

Clone or copy all the .py files into a single folder.

From a terminal, cd into that folder.

Run:
`python3 main.py`


The game window and timer window will appear. Use the arrow keys to explore the maze and try to find the R tile as quickly as possible!

# Credits
All code written by Gavin Fox

AI (Copilot and ChatGPT) were used for this file and comments throughout

