import random
from typing import List, Tuple
from roomClass import tile, Hallway, Empty, Home, Room 


class DungeonMap:
    """
    Represents a dungeon map with corridors (hallways), rooms, and a starting 'home' position.
    Internally, the map is generated as a maze with dead-end rooms based on specified probabilities.
    """

    def __init__(
        self,
        size: int,
        room_chance: float = 0.4,
        extra_connection_chance: float = 0.05
    ):
        # Validate inputs
        if size < 5:
            raise ValueError("Size must be at least 5 to create a dungeon map.")
        if not (0.0 <= room_chance <= 1.0):
            raise ValueError("Room chance must be between 0 and 1.")
        if not (0.0 <= extra_connection_chance <= 1.0):
            raise ValueError("Extra connection chance must be between 0 and 1.")

        # Ensure size is odd so the maze algorithm works correctly
        if size % 2 == 0:
            size -= 1

        # Placeholder for player; assigned later
        self.player = None

        # Dimensions of the grid
        self.size = size
        # grid will store integer codes for cell types during generation:
        #   0 = unvisited/wall, 1 = home, 2 = corridor, 3 = potential room
        self.grid: List[List[int]] = [[0] * size for _ in range(size)]

        # Define 'home' at the center of the grid
        self.home = (size // 2, size // 2)
        # Mark the home cell with integer code 1
        self.grid[self.home[0]][self.home[1]] = 1

        # Probabilities for placing rooms at dead-ends and adding extra corridor connections
        self.room_chance = room_chance
        self.extra_connection_chance = extra_connection_chance

        # Generate the maze and mark potential room locations
        self.generate()
        # Convert the integer grid into tile objects (Empty, Home, Hallway, Room)
        self.grid = self.buildRooms()

    def generate(self) -> List[List[int]]:
        """
        Carve out a maze using a depth-first search (DFS) approach, starting from 'home'.
        Walls are represented by 0, corridors by 2, and dead-end cells flagged for rooms by 3.
        """
        # Possible directions: two steps away in each cardinal direction
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        # Use a stack for DFS; start from the home cell
        stack: List[Tuple[int, int]] = [self.home]

        while stack:
            x, y = stack[-1]
            neighbors: List[Tuple[int, int]] = []

            # Check each direction for unvisited cells (value 0)
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if self._inBounds(nx, ny) and self.grid[nx][ny] == 0:
                    neighbors.append((nx, ny))

            if neighbors:
                # Choose a random neighbor to carve into
                nx, ny = random.choice(neighbors)
                # Carve through the wall one step between current and neighbor
                wall_x, wall_y = (x + nx) // 2, (y + ny) // 2
                self.grid[wall_x][wall_y] = 2  # Mark corridor
                self.grid[nx][ny] = 2         # Mark corridor
                # Push the neighbor onto the stack to continue carving
                stack.append((nx, ny))
            else:
                # No unvisited neighbors: backtrack
                stack.pop()

        # After the maze is complete, identify dead-end cells
        dead_ends: List[Tuple[int, int]] = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 2:
                    # Count adjacent passages or home to see if this cell is a dead-end
                    count_adjacent_passages = 0
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        ni, nj = i + dx, j + dy
                        if self._inBounds(ni, nj) and self.grid[ni][nj] in (1, 2):
                            count_adjacent_passages += 1
                    # Dead-end if exactly one adjacent corridor or home
                    if count_adjacent_passages == 1:
                        dead_ends.append((i, j))

        # Randomly convert some dead-ends into rooms based on room_chance
        for (i, j) in dead_ends:
            if random.random() < self.room_chance:
                self.grid[i][j] = 3  # Mark as potential room

        # Optionally add extra corridor connections to reduce linearity
        self._addExtraConnections()
        return self.grid

    def _addExtraConnections(self):
        """
        Iterate through interior cells and carve extra connections (corridors) between existing passages
        with probability extra_connection_chance, to create loops in the maze.
        """
        # Avoid boundary cells (start from 1 to size-2)
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                if self.grid[i][j] != 0:
                    continue  # Only consider unvisited/wall cells

                # Check vertical alignment: if north & south are passages/home/rooms
                north = self.grid[i - 1][j]
                south = self.grid[i + 1][j]
                if north in (1, 2, 3) and south in (1, 2, 3):
                    left = self.grid[i][j - 1]
                    right = self.grid[i][j + 1]
                    # If left & right are walls and random chance succeeds, carve corridor
                    if left == 0 and right == 0 and random.random() < self.extra_connection_chance:
                        self.grid[i][j] = 2
                    continue

                # Check horizontal alignment: if west & east are passages/home/rooms
                west = self.grid[i][j - 1]
                east = self.grid[i][j + 1]
                if west in (1, 2, 3) and east in (1, 2, 3):
                    up = self.grid[i - 1][j]
                    down = self.grid[i + 1][j]
                    # If up & down are walls and random chance succeeds, carve corridor
                    if up == 0 and down == 0 and random.random() < self.extra_connection_chance:
                        self.grid[i][j] = 2

    def _inBounds(self, x: int, y: int) -> bool:
        """
        Check if coordinates (x, y) lie within the grid boundaries.
        """
        return 0 <= x < self.size and 0 <= y < self.size

    def buildRooms(self) -> List[List[tile]]:
        """
        Convert the integer-coded grid into a grid of tile objects:
          - 0 => Empty
          - 1 => Home
          - 2 => Hallway
          - 3 => Potential Room candidate (only one chosen as actual Room)
        A single room is chosen at random from the candidates.
        """
        # Initialize an empty tile grid
        tile_grid: List[List[tile]] = [[None] * self.size for _ in range(self.size)]
        # Collect all cells marked as potential rooms (value 3)
        possibleRooms: List[Tuple[int, int]] = []

        # First pass: assign Empty, Home, or Hallway tiles; record potential rooms
        for i in range(self.size):
            for j in range(self.size):
                val = self.grid[i][j]
                if val == 0:
                    tile_grid[i][j] = Empty([i, j])
                elif val == 1:
                    tile_grid[i][j] = Home([i, j])
                elif val == 2:
                    tile_grid[i][j] = Hallway([i, j])
                elif val == 3:
                    # Temporarily skip assigning Room until we pick one
                    possibleRooms.append((i, j))

        # Select one dead-end cell from the candidates to become the actual Room
        finalRoom = random.choice(possibleRooms)
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == finalRoom:
                    tile_grid[i][j] = Room([i, j])
                elif tile_grid[i][j] is None:
                    # Any remaining None cells are converted to Empty
                    tile_grid[i][j] = Empty([i, j])

        return tile_grid

    def printMap(self, dev: bool = False):
        """
        Produce a string representation of the map with ASCII borders.
        Symbols:
          - 'H ' for Home
          - '. ' for Hallway
          - 'R ' for Room
          - '  ' for Empty
          - '█ ' for the player location
        """
        # Mapping of tile classes to their ASCII symbols
        cell_repr = {
            Empty: '  ',
            Home: 'H ',
            Hallway: '. ',
            Room: 'R '
        }

        # Build top border
        textmap = '┌' + '─' * (2 * self.size) + '┐' + "\n"

        # For each row, append '│', then each cell symbol, then '│'
        for y, row in enumerate(self.grid):
            line = ''
            for x, cell in enumerate(row):
                # If player's coordinates match this cell, draw the player symbol
                if (x, y) == self.player.location:
                    line += '█ '
                else:
                    # Match the cell object to its symbol
                    for cls, symbol in cell_repr.items():
                        if isinstance(cell, cls):
                            line += symbol
                            break
            textmap += f'│{line}│\n'

        # Build bottom border
        textmap += '└' + '─' * (2 * self.size) + '┘' + '\n'
        return textmap

    def regenerate(self):
        """
        Reset the integer grid and regenerate the maze and rooms from scratch.
        """
        # Reset grid to all walls/unvisited
        self.grid: List[List[int]] = [[0] * self.size for _ in range(self.size)]
        # Reset home position at center
        self.home = (self.size // 2, self.size // 2)
        self.grid[self.home[0]][self.home[1]] = 1

        # Re-run generation and rebuild room tiles
        self.generate()
        self.grid = self.buildRooms()

    def assignPlayer(self, player):
        """
        Place the player on the map at the home coordinates.
        """
        self.player = player
        self.player.location = self.home

    def canMove(self, new_location: Tuple[int, int]) -> bool:
        """
        Check if the player can move to new_location.
        Returns False if out of bounds or if the cell is Empty (i.e., not a hallway/home/room).
        """
        x, y = new_location
        if not self._inBounds(y, x):
            return False
        cell = self.grid[y][x]
        return not isinstance(cell, Empty)
