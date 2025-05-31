import random
from typing import List, Tuple

class MazeDungeonMap:
    def __init__(self,
                 size: int,
                 room_chance: float = 0.4):
        if size < 5:
            raise ValueError("Size must be at least 5 to create a  dungeon map.")
        if room_chance > 1 or room_chance < 0:
            raise ValueError("Room chance must be between 0 and 1.")
        if size % 2 == 0:
            size -= 1
        self.size = size

        # 0 = solid wall; 1 = home; 2 = corridor; 3 = room
        self.grid: List[List[int]] = [[0] * size for _ in range(size)]

        # Home tile is at the center of the grid
        self.home = (size // 2, size // 2)
        self.grid[self.home[0]][self.home[1]] = 1  

        self.room_chance = room_chance

    def generate(self) -> List[List[int]]:
 
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        stack = [self.home]

        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if self._in_bounds(nx, ny) and self.grid[nx][ny] == 0:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)

                wall_x, wall_y = (x + nx) // 2, (y + ny) // 2
                self.grid[wall_x][wall_y] = 2  
                self.grid[nx][ny] = 2          
                stack.append((nx, ny))
            else:
                stack.pop()

        dead_ends: List[Tuple[int,int]] = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 2:
                    cnt = 0
                    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        ni, nj = i + dx, j + dy
                        if self._in_bounds(ni, nj) and self.grid[ni][nj] in (1, 2):
                            cnt += 1
                    if cnt == 1:
                        dead_ends.append((i, j))
        for (i, j) in dead_ends:
            if random.random() < self.room_chance:
                self.grid[i][j] = 3

        return self.grid

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def print_square_map(self):

        cell_repr = {
            0: '  ',   # solid wall
            1: 'H ',   # home
            2: '. ',   # corridor
            3: 'R '    # room
        }

        print('┌' + '─' * (2 * self.size) + '┐')
        for row in self.grid:
            line = ''.join(cell_repr[cell] for cell in row)
            print(f'│{line}│')
 
        print('└' + '─' * (2 * self.size) + '┘')
        print(" H = Home")
        print(" . = Hallway")
        print(" R = Room")





dm = MazeDungeonMap(size=50, room_chance=1)
dm.generate()
dm.print_square_map()
