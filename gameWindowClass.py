import tkinter as tk
from gameSettingsWindow import SettingsApp


class GameWindow:
    def __init__(self, map, root, timer):
        self.window = root
        self.map = map
        self.timer = timer

        self.settingsWindow = None
        self.completed = False
        self.hardMode = False
        self.mapSize = self.map.size
        self.connectionChance = self.map.extra_connection_chance
        self._setup_window()
        self._create_widgets()
        self._bind_events()

    def _setup_window(self):
        self.window.title("Game Window")
        self.window.geometry("700x600")

    def _create_widgets(self):
        top_frame = tk.Frame(self.window)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        self.tileInfo = tk.Label(
            top_frame,
            text="Make your way to R as fast as possible to win!",
            font="TkFixedFont"
        )
        self.tileInfo.pack(pady=10)  

        middle_frame = tk.Frame(self.window)
        middle_frame.pack(expand=True, fill=tk.BOTH)

        self.label = tk.Label(
            middle_frame,
            text=self.map.printMap(),
            font="TkFixedFont"
        )
        self.label.pack(expand=True)

        bottom_frame = tk.Frame(self.window)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        left_spacer = tk.Frame(bottom_frame)
        left_spacer.pack(side=tk.LEFT, expand=True)

        self.regenerate = tk.Button(
            bottom_frame,
            text="New Map",
            font="TkFixedFont",
            command=self._regenerate
        )
        self.regenerate.pack(side=tk.LEFT)

        tk.Frame(bottom_frame, width=20).pack(side=tk.LEFT)

        self.toggleSettings = tk.Button(
            bottom_frame,
            text="Settings",
            font="TkFixedFont",
            command=self.toggleSettingsWindow
        )
        self.toggleSettings.pack(side=tk.LEFT)

        right_spacer = tk.Frame(bottom_frame)
        right_spacer.pack(side=tk.LEFT, expand=True)

    def _bind_events(self):
        self.window.bind("<Up>",    lambda event: self.map.player.move(self, "up"))
        self.window.bind("<Down>",  lambda event: self.map.player.move(self, "down"))
        self.window.bind("<Left>",  lambda event: self.map.player.move(self, "left"))
        self.window.bind("<Right>", lambda event: self.map.player.move(self, "right"))

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
        req_w = self.window.winfo_reqwidth()
        req_h = self.window.winfo_reqheight()
        self.window.geometry(f"{req_w}x{req_h}")

    def updateMap(self):
        self.label.config(text=self.map.printMap())

        x, y = self.map.player.location
        current_tile = self.map.grid[y][x]
        if current_tile.type == "Room":
            self.completed = True
            self.timer.stop_timer()
            self.tileInfo.config(text="Game Completed!")

        self.window.update_idletasks()

    def toggleSettingsWindow(self):
        if self.settingsWindow is None or not self.settingsWindow.winfo_exists():
            self.settingsWindow = tk.Toplevel(self.window)
            self.settingsWindow.title("Game Settings")
            self.settingsWindow.geometry("300x200")
            SettingsApp(self.settingsWindow, gamewindow=self)
        else:
            self.settingsWindow.destroy()
            self.settingsWindow = None
    def updateSettings(self):
        self.map.size = int(self.mapSize)
        self.map.extra_connection_chance = float(self.connectionChance)
        self.map.player.hardMode = self.hardMode
        self._regenerate()
