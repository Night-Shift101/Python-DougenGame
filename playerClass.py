from roomClass import Empty


class PlayerClass:
    """
    Represents the player within the dungeon map. Handles movement, tracking
    of whether the player has moved (to start the timer), and enforces hard
    mode behavior by clearing previous positions.
    """

    def __init__(self, map):
        # Reference to the DungeonMap instance
        self.map = map
        # Player's current (x, y) location; assigned via assignPlayer
        self.location = None
        # Place the player on the map at the 'home' position
        self.map.assignPlayer(self)
        # Tracks whether the player has already made their first move
        self.hasMoved = False
        # If True, the tile the player leaves becomes an Empty tile
        self.hardMode = False
        # Debug print of initial location
        print(self.location)

    def move(self, window, direction: str):
        """
        Attempt to move the player in one of four cardinal directions:
        'up', 'down', 'left', or 'right'. If the game is completed, no move
        is allowed. On the first move, starts the game timer. If hardMode is
        enabled, the previous tile becomes Empty once the player moves.
        """
        # If the dungeon is already completed, do not allow more movement
        if window.completed:
            print("Game completed. No further moves allowed.")
            return

        # Start the timer on the first move
        if not self.hasMoved:
            self.hasMoved = True
            window.timer.start_timer()

        # Ensure the player has a valid starting location
        if self.location is None:
            print("Player has no location assigned.")
            return

        # Determine the new coordinates based on the requested direction
        x, y = self.location
        if direction == "up":
            new_location = (x, y - 1)
        elif direction == "down":
            new_location = (x, y + 1)
        elif direction == "left":
            new_location = (x - 1, y)
        elif direction == "right":
            new_location = (x + 1, y)
        else:
            # If the direction string is not valid, inform the user
            print("Invalid direction. Use 'up', 'down', 'left', or 'right'.")
            return

        # Check if the new location is within bounds and not an Empty tile
        if self.map.canMove(new_location):
            # If hard mode is active, convert the tile being left into Empty
            if self.hardMode:
                old_x, old_y = x, y
                self.map.grid[old_y][old_x] = Empty([old_x, old_y])
            # Update the player's location
            self.location = new_location
            print(f"Moved to {self.location}")
        else:
            # Movement is invalid (either out of bounds or into an Empty tile)
            print("Move out of bounds.")

        # After movement (or failed movement), update the map display
        window.updateMap()
