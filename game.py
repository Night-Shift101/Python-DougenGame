from mapClass import DungeonMap as Map
from playerClass import PlayerClass as Player
import tkinter as tk
from gameWindow import GameWindow
from timerWindow import TimerApp



defaultSettings = [51, 1, .1]
parent = tk.Tk()
child = tk.Toplevel(parent)
map = Map(defaultSettings[0],defaultSettings[1],defaultSettings[2])
player = Player(map)
timer = TimerApp(child)
Game = GameWindow(map, parent, timer)

parent.mainloop()