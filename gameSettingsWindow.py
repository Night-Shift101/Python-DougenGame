import tkinter as tk


class SettingsApp:
    def __init__(self, root, gamewindow=None):
        if gamewindow is None:
            raise ValueError("gamewindow must be provided")

        self.gamewindow = gamewindow
        self.root = root
        self.root.title("Game Settings")
        self.root.geometry("400x175")
        self._create_widgets()

    def _create_widgets(self):
        val_int = (self.root.register(self._validate_int), "%P")
        val_float = (self.root.register(self._validate_float), "%P")

        tk.Label(self.root, text="Map Size (integer):", anchor="w").grid(
            row=0, column=0, sticky="w", padx=10, pady=(10, 5)
        )
        self.map_size_var = tk.StringVar()
        self.map_size_entry = tk.Entry(
            self.root, textvariable=self.map_size_var, validate="key", validatecommand=val_int
        )
        self.map_size_var.set(str(self.gamewindow.mapSize))
        self.map_size_entry.grid(row=0, column=1, padx=10, pady=(10, 5))

        tk.Label(
            self.root,
            text="Connecting Hallways Chance (0.0 > and < 1.0):",
            anchor="w"
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.hallway_chance_var = tk.StringVar()
        self.hallway_chance_entry = tk.Entry(
            self.root,
            textvariable=self.hallway_chance_var,
            validate="key",
            validatecommand=val_float
        )
        self.hallway_chance_var.set(str(self.gamewindow.connectionChance))
        self.hallway_chance_entry.grid(row=1, column=1, padx=10, pady=5)

        self.hard_mode_var = tk.BooleanVar()
        self.hard_mode_var.set(self.gamewindow.hardMode)
        tk.Checkbutton(
            self.root,
            text="Hard Mode",
            variable=self.hard_mode_var
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.save_button = tk.Button(
            self.root,
            text="Save",
            command=self._on_save
        )
        self.save_button.grid(
            row=3, column=0, columnspan=2, pady=(15, 10)
        )

        self.root.grid_columnconfigure(1, weight=1)

    def _validate_int(self, new_value):
        if new_value == "":
            return True
        return new_value.isdigit()

    def _validate_float(self, new_value):
        if new_value == "":
            return True
        try:
            val = float(new_value)
        except ValueError:
            return False
        return 0.0 <= val <= 1.0

    def _on_save(self):
        map_size = self.map_size_var.get()
        hallway_chance = self.hallway_chance_var.get()
        hard_mode = self.hard_mode_var.get()
        self.gamewindow.mapSize = int(map_size)
        self.gamewindow.connectionChance = float(hallway_chance)
        self.gamewindow.hardMode = bool(hard_mode)
        self.gamewindow.updateSettings()
        print(f"Map Size: {map_size}")
        print(f"Connecting Hallways Chance: {hallway_chance}")
        print(f"Hard Mode: {hard_mode}")
        self.root.destroy()
