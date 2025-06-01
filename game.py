from mapClass import DungeonMap as Map
from playerClass import PlayerClass as Player
import tkinter as tk
from gameWindowClass import GameWindow
from timerWindow import TimerApp
from gameSettingsWindow import SettingsApp


defaultSettings = [31, 1, .1]
parent = tk.Tk()
timerChild = tk.Toplevel(parent)

map = Map(defaultSettings[0],defaultSettings[1],defaultSettings[2])
player = Player(map)
timer = TimerApp(timerChild)
Game = GameWindow(map, parent, timer)

parent.mainloop()