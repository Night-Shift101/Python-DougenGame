class tile:
    """
    Base class for all types of tiles in the dungeon.
    Each tile has:
      - name: a human-readable identifier (e.g., "Empty", "Home")
      - type: a string indicating its role (same as name here)
      - position: a tuple (x, y) representing its coordinates on the grid
    """
    def __init__(self, name: str, type: str, position: tuple):
        self.name = name
        self.type = type
        self.position = position


class Empty(tile):
    """
    Represents an unoccupied or wall tile in the dungeon.
    These tiles are not traversable (except when in hard mode behavior).
    """
    def __init__(self, position: tuple):
        super().__init__(name="Empty", type="Empty", position=position)


class Home(tile):
    """
    The starting tile for the player.
    Placed at the center of the dungeon grid when it is generated.
    """
    def __init__(self, position: tuple):
        super().__init__(name="Home", type="Home", position=position)


class Hallway(tile):
    """
    A corridor tile carved out by the maze-generation algorithm.
    These tiles form the paths the player can walk along.
    """
    def __init__(self, position: tuple):
        super().__init__(name="Hallway", type="Hallway", position=position)


class Room(tile):
    """
    The goal tile in the dungeon. 
    One dead-end in the maze is converted into a Room based on probability.
    When the player reaches this tile, the game is completed.
    """
    def __init__(self, position: tuple):
        super().__init__(name="Room", type="Room", position=position)
