import tkinter as tk

class GameWindow:
    def __init__(self, map):
        self.window = tk.Tk()
        self.window.title("My Tkinter Window")
        self.window.geometry("700x600")
        self.map = map
        self.label = tk.Label(self.window, text=self.map.printMap(), font='TkFixedFont')
        self.label.pack()
        self.regenerate = tk.Button(self.window, command=self._regenerate, text="New Map", font='TkFixedFont' )
        self.regenerate.pack()
        self.window.bind("<Up>",  lambda x: self.map.player.move(self,"up"))
        self.window.bind("<Down>", lambda x: self.map.player.move(self,"down"))
        self.window.bind("<Left>", lambda x: self.map.player.move(self,"left"))
        self.window.bind("<Right>", lambda x: self.map.player.move(self, "right"))
    def _regenerate(self):
        self.map.regenerate()
        self.map.assignPlayer(self.map.player)
        self.label.destroy()
        self.regenerate.destroy()
        self.label = tk.Label(self.window, text=self.map.printMap(), font='TkFixedFont')
        self.label.pack()
        self.regenerate = tk.Button(self.window, command=self._regenerate, text="New Map", font='TkFixedFont' )
        self.regenerate.pack()
    def updateMap(self):
        self.label.config(text=self.map.printMap())
        self.window.update_idletasks()
        