# -*- coding: utf-8 -*-
#
# This file is part of the python-shogi library.
#
# Copyright (C) 2020- Yui Matsumura <yuiseki@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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

    def test_two_digit_in_hand(self):
        # 11 pawns in sente's hand
        board = shogi.Board('4+R3l/1r1+P2gk1/3p3s1/2pg5/1p4p2/SP7/2N2PKS1/2G2+n3/8L b b2n2lBGS11P 50')
        svg_file = board.svg()
        pieces = svg_file.split('<!-- BOARD PIECES -->')[1]
        board_positions = pieces.split('<!-- PIECES IN HAND -->')[0]
        hand_positions = pieces.split('<!-- PIECES IN HAND -->')[1]

        # check board pieces
        self.assertTrue(board_positions.count('bishop') == 0)
        self.assertTrue(board_positions.count('rook') == 1)
        self.assertTrue(board_positions.count('pawn') == 7)
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
        self.assertTrue(hand_positions.count('pawn') == 1)
        self.assertTrue(hand_positions.count('knight') == 1)
        self.assertTrue(hand_positions.count('lance') == 1)
        self.assertTrue(hand_positions.count('>11<') == 1)
