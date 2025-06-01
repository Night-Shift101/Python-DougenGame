import tkinter as tk
from mapClass import DungeonMap as Map
from playerClass import PlayerClass as Player
from timerWindow import TimerApp
from gameSettingsWindow import SettingsApp
from gameWindowClass import GameWindow


def main():
    # ─── Default Settings ────────────────────────────────────────────────────
    # [map_size, room_chance, extra_connection_chance]
    default_settings = [31, 1.0, 0.1]

    # ─── Initialize Root Window ──────────────────────────────────────────────
    # This is the main game window.
    root = tk.Tk()

    # ─── Initialize Timer Window ─────────────────────────────────────────────
    # We use a separate Toplevel window for displaying the timer.
    timer_window = tk.Toplevel(root)

    # ─── Create Dungeon Map ──────────────────────────────────────────────────
    # Instantiate the map using default settings:
    #   size = 31, room_chance = 1.0, extra_connection_chance = 0.1
    dungeon_map = Map(
        size=default_settings[0],
        room_chance=default_settings[1],
        extra_connection_chance=default_settings[2]
    )

    # ─── Create Player ────────────────────────────────────────────────────────
    # The PlayerClass constructor will assign the player to the map's home tile.
    player = Player(dungeon_map)

    # ─── Create Timer App ─────────────────────────────────────────────────────
    # TimerApp manages game timing; it takes the timer_window as its parent.
    timer_app = TimerApp(timer_window)

    # ─── Create Game Window ──────────────────────────────────────────────────
    # Combine the dungeon_map, root window, and timer_app into our main game UI.
    game_window = GameWindow(dungeon_map, root, timer_app)

    # ─── Start Tkinter Main Loop ──────────────────────────────────────────────
    # This call blocks and keeps the GUI responsive until the user closes the window.
    root.mainloop()


if __name__ == "__main__":
    main()
