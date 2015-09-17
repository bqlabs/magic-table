import unittest
from ChessEngine import ChessEngine

__author__ = 'def'

class ChessEngineTest(unittest.TestCase):

    initial_board_description = """WP@a2
                           WP@b2
                           WP@c2
                           WP@d2
                           WP@e2
                           WP@f2
                           WP@g2
                           WP@h2
                           WR@a1
                           WB@b1
                           WN@c1
                           WQ@d1
                           WK@e1
                           WN@f1
                           WB@g1
                           WR@h1
                           BP@a7
                           BP@b7
                           BP@c7
                           BP@d7
                           BP@e7
                           BP@f7
                           BP@g7
                           BP@h7
                           BR@a8
                           BB@b8
                           BN@c8
                           BQ@d8
                           BK@e8
                           BN@f8
                           BB@g8
                           BR@h8"""

    def test_set_board(self):
        expected_result = [[2,3,4,5,6,4,3,2],
                           [1,1,1,1,1,1,1,1],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [7,7,7,7,7,7,7,7],
                           [8,9,10,11,12,10,9,8]]

        # Create chess engine
        engine = ChessEngine()
        engine.set_board(self.initial_board_description)
        self.assertEqual(engine.board, expected_result)

    def test_tile_to_coord(self):
        self.fail("Test not implemented")

    def test_coord_to_tile(self):
        self.fail("Test not implemented")

    def test_valid_moves(self):
        self.fail("Test not implemented")


    def test_move(self):
        commands_to_test = ['e4', 'e5', 'Qh5', 'Nc6', 'Bc4', 'Nf6']
        expected_results = []
        expected_results.append([[2,3,4,5,6,4,3,2],
                                 [1,1,1,1,0,1,1,1],
                                 [0,0,0,0,0,0,0,0],
                                 [0,0,0,0,1,0,0,0],
                                 [0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0],
                                 [7,7,7,7,7,7,7,7],
                                 [8,9,10,11,12,10,9,8]])
        expected_results.append([[2,3,4,5,6,4,3,2],
                                 [1,1,1,1,0,1,1,1],
                                 [0,0,0,0,0,0,0,0],
                                 [0,0,0,0,1,0,0,0],
                                 [0,0,0,0,7,0,0,0],
                                 [0,0,0,0,0,0,0,0],
                                 [7,7,7,7,0,7,7,7],
                                 [8,9,10,11,12,10,9,8]])
        expected_results.append([[2,3,4,0,6,4,3,2],
                                 [1,1,1,1,0,1,1,1],
                                 [0,0,0,0,0,0,0,0],
                                 [0,0,0,0,1,0,0,0],
                                 [0,0,0,0,7,0,0,5],
                                 [0,0,0,0,0,0,0,0],
                                 [7,7,7,7,0,7,7,7],
                                 [8,9,10,11,12,10,9,8]])
        expected_results.append([[2,3,4,0,6,4,3,2],
                                 [1,1,1,1,0,1,1,1],
                                 [0,0,0,0,0,0,0,0],
                                 [0,0,0,0,1,0,0,10],
                                 [0,0,0,0,7,0,0,5],
                                 [0,0,0,0,0,0,0,0],
                                 [7,7,7,7,0,7,7,7],
                                 [8,9,0,11,12,10,9,8]])
        expected_results.append([[2,3,4,0,6,0,3,2],
                                 [1,1,1,1,0,1,1,1],
                                 [0,0,0,0,0,0,0,0],
                                 [0,0,4,0,1,0,0,10],
                                 [0,0,0,0,7,0,0,5],
                                 [0,0,0,0,0,0,0,0],
                                 [7,7,7,7,0,7,7,7],
                                 [8,9,0,11,12,10,9,8]])
        expected_results.append([[2,3,4,0,6,0,3,2],
                                 [1,1,1,1,0,1,1,1],
                                 [0,0,0,0,0,0,0,0],
                                 [0,0,4,0,1,0,0,10],
                                 [0,0,0,0,7,0,0,5],
                                 [0,0,0,0,0,9,0,0],
                                 [7,7,7,7,0,7,7,7],
                                 [8,9,0,11,12,10,0,8]])

        # Create chess engine
        engine = ChessEngine()
        engine.set_board(self.initial_board_description)

        # Movement
        for move, result in zip(commands_to_test, expected_results):
            engine.parse(move)
            self.assertEqual(engine.board, expected_results)