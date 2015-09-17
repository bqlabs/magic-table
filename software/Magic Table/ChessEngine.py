__author__ = 'def'


class ChessEngine:

    def __init__(self):
        self.board = [[0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0]]

    def set_board(self, board_description):
        pass

    def parse(self, movement):
        pass

    @staticmethod
    def _tile_to_coord(tile):
        """From a tile description (a1) get its coordinates (0,0)"""
        pass

    @staticmethod
    def _coord_to_tile(coord):
        """From a coordinate (0,0) get its corresponding tile (a1)"""
        pass