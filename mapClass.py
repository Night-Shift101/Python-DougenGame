import random
from typing import List, Tuple
from roomClass import tile, Hallway, Empty, Home, Room 
class DungeonMap:
    def __init__(self,
                 size: int,
                 room_chance: float = 0.4,
                 extra_connection_chance: float = 0.05):
        if size < 5:
            raise ValueError("Size must be at least 5 to create a dungeon map.")
        if not (0.0 <= room_chance <= 1.0):
            raise ValueError("Room chance must be between 0 and 1.")
        if not (0.0 <= extra_connection_chance <= 1.0):
            raise ValueError("Extra connection chance must be between 0 and 1.")

        if size % 2 == 0:
            size -= 1

        self.size = size
        self.grid: List[List[int]] = [[0] * size for _ in range(size)]

        self.home = (size // 2, size // 2)
        self.grid[self.home[0]][self.home[1]] = 1

        self.room_chance = room_chance
        self.extra_connection_chance = extra_connection_chance

        self.generate()
        self.grid = self.buildRooms()

    def generate(self) -> List[List[int]]:
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        stack: List[Tuple[int, int]] = [self.home]

        while stack:
            x, y = stack[-1]
            neighbors: List[Tuple[int, int]] = []

            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if self._inBounds(nx, ny) and self.grid[nx][ny] == 0:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                wall_x, wall_y = (x + nx) // 2, (y + ny) // 2

                self.grid[wall_x][wall_y] = 2
                self.grid[nx][ny] = 2
                stack.append((nx, ny))
            else:
                stack.pop()

        dead_ends: List[Tuple[int, int]] = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 2:
                    count_adjacent_passages = 0
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        ni, nj = i + dx, j + dy
                        if self._inBounds(ni, nj) and self.grid[ni][nj] in (1, 2):
                            count_adjacent_passages += 1
                    if count_adjacent_passages == 1:
                        dead_ends.append((i, j))

        for (i, j) in dead_ends:
            if random.random() < self.room_chance:
                self.grid[i][j] = 3

        self._addExtraConnections()
        return self.grid

    def _addExtraConnections(self):
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                if self.grid[i][j] != 0:
                    continue

                north = self.grid[i - 1][j]
                south = self.grid[i + 1][j]
                if north in (1, 2, 3) and south in (1, 2, 3):
                    left = self.grid[i][j - 1]
                    right = self.grid[i][j + 1]
                    if left == 0 and right == 0 and random.random() < self.extra_connection_chance:
                        self.grid[i][j] = 2
                    continue

                west = self.grid[i][j - 1]
                east = self.grid[i][j + 1]
                if west in (1, 2, 3) and east in (1, 2, 3):
                    up = self.grid[i - 1][j]
                    down = self.grid[i + 1][j]
                    if up == 0 and down == 0 and random.random() < self.extra_connection_chance:
                        self.grid[i][j] = 2

    def _inBounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size
    def buildRooms(self) -> List[List[tile]]:
        """
        Iterate over self.grid (which holds ints 0..3) and return
        a new 2D list of room‐subclass instances corresponding to each tile.
        """
        tile_grid: List[List[tile]] = [[None] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                val = self.grid[i][j]
                if val == 0:
                    tile_grid[i][j] = Empty()
                elif val == 1:
                    tile_grid[i][j] = Home()
                elif val == 2:
                    tile_grid[i][j] = Hallway()
                elif val == 3:
                    tile_grid[i][j] = Room()
        return tile_grid
    def printMap(self):
        cell_repr = {
            Empty: '  ',
            Home: 'H ',
            Hallway: '. ',
            Room: 'R '
        }

        print('┌' + '─' * (2 * self.size) + '┐')
        for row in self.grid:
            line = ''
            for cell in row:
                for cls, symbol in cell_repr.items():
                    if isinstance(cell, cls):
                        line += symbol
                        break
            print(f'│{line}│')
        print('└' + '─' * (2 * self.size) + '┘')
        print(" H = Home")
        print(" . = Hallway")
        print(" R = Room")



