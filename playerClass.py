from roomClass import Empty
class PlayerClass:
    def __init__(self, map):
        self.map = map
        self.location = None
        self.map.assignPlayer(self)
        self.hasMoved = False
        self.hardMode = False
        print(self.location)
    def move(self, window, direction: str):
        if window.completed:
            print("Game completed. No further moves allowed.")
            return
        if not self.hasMoved:
            self.hasMoved = True
            window.timer.start_timer()
        if self.location is None:
            print("Player has no location assigned.")
            return
        
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
            print("Invalid direction. Use 'up', 'down', 'left', or 'right'.")
            return
       
        if self.map.canMove(new_location):
            if self.hardMode:
                self.map.grid[y][x] = Empty([x, y])
            self.location = new_location
            print(f"Moved to {self.location}")
        else:
            print("Move out of bounds.")
        window.updateMap()