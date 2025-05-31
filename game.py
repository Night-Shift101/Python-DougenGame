from mapClass import DungeonMap as Map
import threading as th
from gameWindow import GameWindow


defaultSettings = [31, 1, .2]

map = Map(defaultSettings[0],defaultSettings[1],defaultSettings[2])
map.printMap()
main = GameWindow(map)
main.window.mainloop()