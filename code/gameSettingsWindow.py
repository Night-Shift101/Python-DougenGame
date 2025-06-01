import tkinter as tk


class SettingsApp:
    def __init__(self, root, gamewindow=None):
        # Ensure a reference to the main GameWindow is provided
        if gamewindow is None:
            raise ValueError("gamewindow must be provided")

        self.gamewindow = gamewindow
        self.root = root

        # Configure the settings window title and size
        self.root.title("Game Settings")
        self.root.geometry("400x175")

        # Build all widgets (labels, entries, checkbox, button)
        self._create_widgets()

    def _create_widgets(self):
        # Register validation callbacks for integer and float inputs
        val_int = (self.root.register(self._validate_int), "%P")
        val_float = (self.root.register(self._validate_float), "%P")

        # ─── Map Size Input ───────────────────────────────────────────────────
        # Label prompting for an integer map size
        tk.Label(
            self.root,
            text="Map Size (integer):",
            anchor="w"
        ).grid(
            row=0, column=0,
            sticky="w",
            padx=10, pady=(10, 5)
        )

        # Entry widget tied to a StringVar; only allows integer text
        self.map_size_var = tk.StringVar()
        self.map_size_entry = tk.Entry(
            self.root,
            textvariable=self.map_size_var,
            validate="key",
            validatecommand=val_int
        )
        # Initialize entry with the current map size from the GameWindow
        self.map_size_var.set(str(self.gamewindow.mapSize))
        self.map_size_entry.grid(
            row=0, column=1,
            padx=10, pady=(10, 5)
        )

        # ─── Connecting Hallways Chance Input ────────────────────────────────
        # Label prompting for a float value between 0.0 and 1.0
        tk.Label(
            self.root,
            text="Connecting Hallways Chance (0.0 > and < 1.0):",
            anchor="w"
        ).grid(
            row=1, column=0,
            sticky="w",
            padx=10, pady=5
        )

        # Entry widget tied to a StringVar; only allows valid float text
        self.hallway_chance_var = tk.StringVar()
        self.hallway_chance_entry = tk.Entry(
            self.root,
            textvariable=self.hallway_chance_var,
            validate="key",
            validatecommand=val_float
        )
        # Initialize entry with the current hallway chance from the GameWindow
        self.hallway_chance_var.set(str(self.gamewindow.connectionChance))
        self.hallway_chance_entry.grid(
            row=1, column=1,
            padx=10, pady=5
        )

        # ─── Hard Mode Checkbox ──────────────────────────────────────────────
        # BooleanVar to track the checkbox state
        self.hard_mode_var = tk.BooleanVar()
        # Initialize checkbox from current GameWindow hardMode flag
        self.hard_mode_var.set(self.gamewindow.hardMode)
        tk.Checkbutton(
            self.root,
            text="Hard Mode",
            variable=self.hard_mode_var
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10, pady=5,
            sticky="w"
        )

        # ─── Save Button ─────────────────────────────────────────────────────
        # When clicked, _on_save will read values and update the GameWindow
        self.save_button = tk.Button(
            self.root,
            text="Save",
            command=self._on_save
        )
        self.save_button.grid(
            row=3, column=0,
            columnspan=2,
            pady=(15, 10)
        )

        # Allow the second column (entries) to expand if the window is resized
        self.root.grid_columnconfigure(1, weight=1)

    def _validate_int(self, new_value):
        """
        Validation callback to allow only digits for integer entry.
        Accepts empty string to let the user delete.
        """
        if new_value == "":
            return True
        return new_value.isdigit()

    def _validate_float(self, new_value):
        """
        Validation callback to allow only floats between 0.0 and 1.0 inclusive.
        Accepts empty string to let the user delete.
        """
        if new_value == "":
            return True
        try:
            val = float(new_value)
        except ValueError:
            return False
        return 0.0 <= val <= 1.0

    def _on_save(self):
        """
        When the Save button is clicked, read the input values:
        - Update the GameWindow's mapSize, connectionChance, and hardMode.
        - Call updateSettings on the GameWindow to apply changes.
        - Print new settings to console for debugging.
        - Close the settings window.
        """
        # Retrieve text from entry widgets
        map_size = self.map_size_var.get()
        hallway_chance = self.hallway_chance_var.get()
        hard_mode = self.hard_mode_var.get()

        # Update the GameWindow's attributes
        self.gamewindow.mapSize = int(map_size)
        self.gamewindow.connectionChance = float(hallway_chance)
        self.gamewindow.hardMode = bool(hard_mode)

        # Trigger the GameWindow to apply and regenerate with new settings
        self.gamewindow.updateSettings()

        # Debug output to console
        print(f"Map Size: {map_size}")
        print(f"Connecting Hallways Chance: {hallway_chance}")
        print(f"Hard Mode: {hard_mode}")

        # Close the settings window
        self.root.destroy()
