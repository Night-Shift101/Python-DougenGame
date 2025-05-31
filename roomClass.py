class tile:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

class Empty(tile):
    def __init__(self):
        super().__init__(name="Empty", type="Empty")

class Home(tile):
    def __init__(self):
        super().__init__(name="Home", type="Home")

class Hallway(tile):
    def __init__(self):
        super().__init__(name="Hallway", type="Hallway")

class Room(tile):
    def __init__(self):
        super().__init__(name="Room", type="Room")