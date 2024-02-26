class MapElement:
    def __init__(self):
        pass
    def entrar(self):
        pass

class Game:
    def __init__(self):
        self.maze = None

    def createWall(self):
        return Wall()

    def createDoor(self, side1, side2):
        door = Door(side1, side2)
        door.side1 = side1
        door.side2 = side2
        return door

    def createRoom(self, id):
        room = Room(id)
        room.north=self.createWall()
        room.east=self.createWall()
        room.south=self.createWall()
        room.west=self.createWall()
        return Room(id) 

    def createMaze(self):
        return Maze()
    
    def make2RoomsMazeFM(self):
        self.maze = self.createMaze()
        room1 = self.createRoom(1)
        room2 = self.createRoom(2)
        door = self.createDoor(room1, room2)
        room1.south=door
        room2.north=door
        self.maze.addRoom(room1)
        self.maze.addRoom(room2)
        
        return self.maze
    
    def make2RoomsMaze(self):
        self.maze = Maze()
        room1 = Room(1)
        room2 = Room(2)
        self.maze.addRoom(room1)
        self.maze.addRoom(room2)

        door = Door(room1, room2)
        room1.south=door
        room2.north=door
        return self.maze

class Door(MapElement):
    def __init__(self, side1, side2):
        self.side1 = side1
        self.side2 = side2
        self.opened = False
    def entrar(self):
        if self.opened:
            self.side2.entrar()
        else:
            print("The door is locked")
        
class Wall(MapElement):
    def __init__(self):
        pass # Walls don't need any special attributes
    def entrar(self):
        print("You can't go through walls")

class BombedWall(Wall):
    def __init__(self):
        self.active = False
    def entrar(self):
        if self.active:
            print("The bomb has detonated")
        else:
            return super().entrar()

class BombedGame(Game):
    def create_wall(self):
        return BombedWall()

class Contenedor(MapElement):

    def __init__(self):
        self.Hijos = []
        
    def agregarHijo(self, hijo):
        self.Hijos.append(hijo)
        
    def eliminarHijo(self, hijo):
        self.Hijos.remove(hijo)


class Hoja(MapElement):
    def accept(self, visitor):
        visitor.visitHoja(self)

class Decorator(Hoja):
    def __init__(self, component):
        self.component = component

class Maze(Contenedor):
    def __init__(self):
        self.rooms = []
    def addRoom(self, room):
        self.rooms.append(room)
    def entrar(self):
        self.rooms[0].entrar()

class Room(Contenedor):
    def __init__(self, id):
        self.north=None
        self.east=None
        self.west=None
        self.south=None
        self.id = id

    def entrar(self):
        print("You are in room {}".format(self.id))

import unittest

from laberinto import Maze, Room, Door

class TestMaze(unittest.TestCase):
    
    def test_two_rooms(self):
        maze = Maze()
        room1 = Room(1)
        room2 = Room(2)
        maze.addRoom(room1)
        maze.addRoom(room2)
        
        door = Door(room1, room2)
        room1.south = door
        room2.north = door
        
        self.assertEqual(len(maze.rooms), 2)
        self.assertIs(room1.south, door)
        self.assertIs(room2.north, door)



# Create rooms  
game = Game()

game.make2RoomsMaze()
game.maze.entrar()

#game.make2RoomsMaze()
#game.maze.entrar()

#maze = Maze()
#room1 = Room(1)
#room2 = Room(2)
#maze.addRoom(room1)
#maze.addRoom(room2)

#door = Door(room1, room2)
#room1.south = door
#room2.north = door
#game.maze=maze

game = Game()
game.make2RoomsMazeFM()

game = BombedGame()
game.make2RoomsMazeFM()
game.maze.entrar()