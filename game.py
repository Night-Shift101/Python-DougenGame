from mapClass import DungeonMap as Map
from gameWindow import GameWindow


defaultSettings = [31, 1, .2]

map = Map(defaultSettings[0],defaultSettings[1],defaultSettings[2])
main = GameWindow(map)
main.window.mainloop()