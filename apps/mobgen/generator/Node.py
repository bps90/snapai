from .Position import Position

class Node:

    def __init__(self, id:int):
        self.id = id
        self.position = None
        

    def __str__(self):
        return f'Node(id: {self.id}, position: {self.position})'
    
    def initNode(self, x: float, y: float, z: float):
        self.position = Position(x, y, z)

    def setPosition(self, position: Position):
        self.position = position