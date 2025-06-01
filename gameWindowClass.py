import tkinter as tk
from gameSettingsWindow import SettingsApp


class GameWindow:
    """
    Main window for the dungeon game. Displays:
      - A header text area (tileInfo) at the top
      - The dungeon map (label) in the center
      - Two buttons (“New Map” and “Settings”) centered at the bottom
    Handles window resizing when a new map is generated, and binds arrow keys
    for player movement.
    """

    def __init__(self, map, root, timer):
        # Reference to the dungeon map model (DungeonMap instance)
        self.map = map
        # The root Tk window for the game display
        self.window = root
        # TimerApp instance used to start/stop the game timer
        self.timer = timer

        # Holds a reference to the settings window (Toplevel) when open
        self.settingsWindow = None
        # Flag indicating whether the player has reached the Room (game over)
        self.completed = False
        # Hard mode flag: if True, walking wipes out corridors behind the player
        self.hardMode = False
        # Default map size and connection chance reflect the current map model
        self.mapSize = self.map.size
        self.connectionChance = self.map.extra_connection_chance

        # Initialize and lay out the Tk window
        self._setup_window()
        self._create_widgets()
        self._bind_events()

    def _setup_window(self):
        """Configure window title and initial geometry."""
        self.window.title("Game Window")
        # Start with 700x600 pixels; will auto-resize when regenerating map
        self.window.geometry("700x600")

    def _create_widgets(self):
        """
        Create and pack three main frames:
          1) top_frame: holds the tileInfo label (instructions/status)
          2) middle_frame: holds the map display label
          3) bottom_frame: holds the “New Map” and “Settings” buttons, centered
        """
        # ─── Top Frame: Tile Info Label ───────────────────────────────────────
        top_frame = tk.Frame(self.window)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Label showing instructions or "Game Completed!" status
        self.tileInfo = tk.Label(
            top_frame,
            text="Make your way to R as fast as possible to win!",
            font="TkFixedFont"
        )
        self.tileInfo.pack(pady=10)

        # ─── Middle Frame: Map Display ───────────────────────────────────────
        middle_frame = tk.Frame(self.window)
        # Expand in both directions to fill the available space
        middle_frame.pack(expand=True, fill=tk.BOTH)

        # Label that holds the ASCII representation of the map
        self.label = tk.Label(
            middle_frame,
            text=self.map.printMap(),
            font="TkFixedFont"
        )
        # Let this label expand to occupy middle_frame fully
        self.label.pack(expand=True)

        # ─── Bottom Frame: Centered Buttons ─────────────────────────────────
        bottom_frame = tk.Frame(self.window)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Left spacer: expands to push buttons toward the center
        left_spacer = tk.Frame(bottom_frame)
        left_spacer.pack(side=tk.LEFT, expand=True)

        # “New Map” button: regenerates the dungeon when clicked
        self.regenerate = tk.Button(
            bottom_frame,
            text="New Map",
            font="TkFixedFont",
            command=self._regenerate
        )
        self.regenerate.pack(side=tk.LEFT)

        # Small fixed-width spacer between the two buttons
        tk.Frame(bottom_frame, width=20).pack(side=tk.LEFT)

        # “Settings” button: opens the SettingsApp to change map parameters
        self.toggleSettings = tk.Button(
            bottom_frame,
            text="Settings",
            font="TkFixedFont",
            command=self.toggleSettingsWindow
        )
        self.toggleSettings.pack(side=tk.LEFT)

        # Right spacer: balances the left spacer to keep buttons centered
        right_spacer = tk.Frame(bottom_frame)
        right_spacer.pack(side=tk.LEFT, expand=True)

    def _bind_events(self):
        """
        Bind arrow keys to the player's move() method.
        Passes self (GameWindow) as context so the player can call window.updateMap().
        """
        self.window.bind("<Up>",    lambda event: self.map.player.move(self, "up"))
        self.window.bind("<Down>",  lambda event: self.map.player.move(self, "down"))
        self.window.bind("<Left>",  lambda event: self.map.player.move(self, "left"))
        self.window.bind("<Right>", lambda event: self.map.player.move(self, "right"))

    def _regenerate(self):
        """
        Called when “New Map” is clicked or settings change.
        1) Rebuild the map data (DungeonMap.regenerate())
        2) Reassign the player to the new home location
        3) Reset timer and completion flags
        4) Update the ASCII map label and tileInfo text
        5) Force a window resize to fit the new map dimensions
        """
        # Regenerate internal maze and room layout
        self.map.regenerate()
        # Place player at the new home in the new grid
        self.map.assignPlayer(self.map.player)

        # Reset timer state and completion flag
        self.timer.seconds = 0
        self.timer.timer_running = False
        self.completed = False
        # Update the timer display (e.g., show 00:00)
        self.timer.update_timer()
        # Mark that the player has not yet moved
        self.map.player.hasMoved = False

        # Refresh the map ASCII text and the instruction label
        self.label.config(text=self.map.printMap())
        self.tileInfo.config(text="Make your way to R as fast as possible to win!")

        # Force geometry recalculation and resize window to fit content
        self.window.update_idletasks()
        req_w = self.window.winfo_reqwidth()
        req_h = self.window.winfo_reqheight()
        self.window.geometry(f"{req_w}x{req_h}")

    def updateMap(self):
        """
        Refresh the map label each time the player moves.
        Checks if the current tile is a Room; if so, marks game as completed,
        stops the timer, and updates the tileInfo to “Game Completed!”.
        """
        # Update ASCII representation
        self.label.config(text=self.map.printMap())

        # Check the tile where the player now stands
        x, y = self.map.player.location
        current_tile = self.map.grid[y][x]
        if current_tile.type == "Room":
            # Player reached the target room
            self.completed = True
            self.timer.stop_timer()
            self.tileInfo.config(text="Game Completed!")

        # Ensure any pending UI changes are drawn
        self.window.update_idletasks()

    def toggleSettingsWindow(self):
        """
        Open or close the settings dialog (Toplevel).
        When opening, pass a reference to self so settings can modify mapSize, etc.
        """
        if self.settingsWindow is None or not self.settingsWindow.winfo_exists():
            # Create a new Toplevel window for settings
            self.settingsWindow = tk.Toplevel(self.window)
            self.settingsWindow.title("Game Settings")
            self.settingsWindow.geometry("300x200")
            # Instantiate SettingsApp with a reference back to this GameWindow
            SettingsApp(self.settingsWindow, gamewindow=self)
        else:
            # If settings window already exists, destroy it (close)
            self.settingsWindow.destroy()
            self.settingsWindow = None

    def updateSettings(self):
        """
        Apply new settings from the SettingsApp:
          - Resize the DungeonMap (map.size)
          - Change the hallway-connection probability
          - Enable or disable hardMode on the player
        Then regenerate the map so changes take effect immediately.
        """
        # Update map parameters from the SettingsApp variables
        self.map.size = int(self.mapSize)
        self.map.extra_connection_chance = float(self.connectionChance)
        self.map.player.hardMode = self.hardMode

        # Recreate the map with new size/chance and player placement
        self._regenerate()
