class tile:
    def __init__(self, name: str, type: str, position: tuple ):
        self.name = name
        self.type = type
        self.position = position

class Empty(tile):
    def __init__(self, position: tuple):
        super().__init__(name="Empty", type="Empty", position=position)

class Home(tile):
    def __init__(self, position: tuple):
        super().__init__(name="Home", type="Home", position=position)

class Hallway(tile):
    def __init__(self, position: tuple):
        super().__init__(name="Hallway", type="Hallway", position=position)

class Room(tile):
    def __init__(self, position: tuple):
        super().__init__(name="Room", type="Room", position=position)