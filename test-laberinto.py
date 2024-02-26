import unittest
from laberinto import Game

class TestGame(unittest.TestCase):
    
    def test_createRoom_returns_room_with_walls(self):
        game = Game()
        room = game.createRoom(1)
        self.assertIsNotNone(room.north)
        self.assertIsNotNone(room.south)
        self.assertIsNotNone(room.east)
        self.assertIsNotNone(room.west)

    def test_createRoom_returns_room_with_correct_id(self):
        game = Game()
        room = game.createRoom(5)
        self.assertEqual(room.id, 5)
        
    def test_createRoom_returns_different_rooms(self):
        game = Game()
        room1 = game.createRoom(1)
        room2 = game.createRoom(2)
        self.assertNotEqual(room1, room2)