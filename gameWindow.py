import tkinter as tk

class GameWindow:
    def __init__(self, map, root, timer):
        self.window = root
        self.timer = timer
        self.window.title("Game Window")
        
        self.window.geometry("700x600")
        self.map = map
        self.completed = False
        self.label = tk.Label(self.window, text=self.map.printMap(), font='TkFixedFont')
        self.label.pack()
        self.tileInfo = tk.Label(self.window, text="Make your way to R as fast as possible to win!", font='TkFixedFont')
        self.regenerate = tk.Button(self.window, command=self._regenerate, text="New Map", font='TkFixedFont' )
        self.regenerate.pack()
        self.tileInfo.pack()
        self.window.bind("<Up>",  lambda x: self.map.player.move(self,"up"))
        self.window.bind("<Down>", lambda x: self.map.player.move(self,"down"))
        self.window.bind("<Left>", lambda x: self.map.player.move(self,"left"))
        self.window.bind("<Right>", lambda x: self.map.player.move(self, "right"))
    def _regenerate(self):
        self.map.regenerate()
        self.map.assignPlayer(self.map.player)
        self.timer.seconds = 0
        self.timer.timer_running = False
        self.completed = False
        self.timer.update_timer()
        self.map.player.hasMoved = False
        self.label.config(text=self.map.printMap())
        self.tileInfo.config(text="Make your way to R as fast as possible to win!")
        self.window.update_idletasks()
    def updateMap(self):
        self.label.config(text=self.map.printMap())
        tile = self.map.grid[self.map.player.location[1]][self.map.player.location[0]]
        if tile.type == "Room":
            self.completed = True
            self.timer.stop_timer()
            self.tileInfo.config(text="Game Completed!")
        
        self.window.update_idletasks()
        