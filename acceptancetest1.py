import unittest
from construction_board import construct
from movement import is_valid_move, remove_mill

class AcceptanceTestNineMensMorris(unittest.TestCase):
    def setUp(self):
        # Set up the initial game state
        self.board = [[' ' for _ in range(13)] for _ in range(13)]
        self.board = construct(self.board)

    def test_game_scenario1(self):
        # Simulate a game scenario
        # Place a piece (X)
        self.board = is_valid_move(self.board, 'X')

        # Place a piece (O)
        self.board = is_valid_move(self.board, 'O')

        # Attempt to place a piece on an occupied position (should fail)
        initial_board = self.board.copy()
        self.board = is_valid_move(self.board, 'X')

        # Check that the board state has changed as expected
        self.assertEqual(self.board, initial_board)
    def test_game_scenario2(self):
        # Simulate a game scenario
        # Place a piece (X)
        self.board = is_valid_move(self.board, 'X')

        # Place a piece (O)
        self.board = is_valid_move(self.board, 'X')

        # Attempt to place a piece on an occupied position (should fail)
        initial_board = self.board.copy()
        self.board = is_valid_move(self.board, 'X')
        self.assertEqual(self.board,initial_board)

if __name__ == '__main__':
    unittest.main()
