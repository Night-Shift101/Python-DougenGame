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
    def _regenerate(self):
        self.map.regenerate()
        self.label.destroy()
        self.regenerate.destroy()
        self.label = tk.Label(self.window, text=self.map.printMap(), font='TkFixedFont')
        self.label.pack()
        self.regenerate = tk.Button(self.window, command=self._regenerate, text="New Map", font='TkFixedFont' )
        self.regenerate.pack()

        