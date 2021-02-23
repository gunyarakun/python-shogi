import shogi
import unittest



class BoardTestCase(unittest.TestCase):
    def test_default_board(self):
        board = shogi.Board()
        svg_file = board.svg()
        pieces = svg_file.split('<!-- BOARD PIECES -->')[1]
        board_positions = pieces.split('<!-- PIECES IN HAND -->')[0]
        hand_positions = pieces.split('<!-- PIECES IN HAND -->')[1]

        # check board pieces
        self.assertTrue(board_positions.count('bishop') == 2)
        self.assertTrue(board_positions.count('rook') == 2)
        self.assertTrue(board_positions.count('pawn') == 18)
        self.assertTrue(board_positions.count('knight') == 4)
        self.assertTrue(board_positions.count('king') == 2)
        self.assertTrue(board_positions.count('gold') == 4)
        self.assertTrue(board_positions.count('silver') == 4)
        self.assertTrue(board_positions.count('lance') == 4)

    def test_complex_position(self):
        board = shogi.Board('4+R3l/1r1+P2gk1/3p1p1s1/2pg3pp/1p4p2/SP4PPP/2NP1PKS1/2G2+n3/8L w B2N2L3Pbgsp 10')
        svg_file = board.svg()
        pieces = svg_file.split('<!-- BOARD PIECES -->')[1]
        board_positions = pieces.split('<!-- PIECES IN HAND -->')[0]
        hand_positions = pieces.split('<!-- PIECES IN HAND -->')[1]

        # check board pieces
        self.assertTrue(board_positions.count('bishop') == 0)
        self.assertTrue(board_positions.count('rook') == 1)
        self.assertTrue(board_positions.count('pawn') == 14)
        self.assertTrue(board_positions.count('knight') == 2)
        self.assertTrue(board_positions.count('king') == 2)
        self.assertTrue(board_positions.count('gold') == 3)
        self.assertTrue(board_positions.count('silver') == 3)
        self.assertTrue(board_positions.count('lance') == 2)
        self.assertTrue(board_positions.count('dragon') == 1)
        self.assertTrue(board_positions.count('pro-pawn') == 1)
        self.assertTrue(board_positions.count('pro-knight') == 1)

        # check hand pieces (only checking 1 count per player)
        self.assertTrue(hand_positions.count('bishop') == 2)
        self.assertTrue(hand_positions.count('gold') == 1)
        self.assertTrue(hand_positions.count('silver') == 1)
        self.assertTrue(hand_positions.count('pawn') == 2)
        self.assertTrue(hand_positions.count('knight') == 1)
        self.assertTrue(hand_positions.count('lance') == 1)
