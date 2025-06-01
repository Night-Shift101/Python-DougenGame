from mapClass import DungeonMap as Map
from playerClass import PlayerClass as Player

from gameWindow import GameWindow


defaultSettings = [51, 1, .2]

map = Map(defaultSettings[0],defaultSettings[1],defaultSettings[2])
player = Player(map)
main = GameWindow(map)
main.window.mainloop()