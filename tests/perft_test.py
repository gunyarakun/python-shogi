# -*- coding: utf-8 -*-
#
# This file is part of the python-shogi library.
# Copyright (C) 2015- Tasuku SUENAGA <tasuku-s-github@titech.ac>
#
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

from __future__ import unicode_literals

import shogi
import unittest

def perft(board, depth):
    if depth > 1:
        count = 0

        for move in board.pseudo_legal_moves:
            board.push(move)

            if not board.was_suicide() and not board.was_check_by_dropping_pawn(move):
                count += perft(board, depth - 1)

            board.pop()

        return count
    else:
        return len(board.legal_moves)

class PerftTestCase(unittest.TestCase):
    def test_1(self):
        board = shogi.Board()
        self.assertEqual(perft(board, 1), 30)
        self.assertEqual(perft(board, 2), 900)

    def test_2(self):
        board = shogi.Board(shogi.STARTING_SFEN)
        self.assertEqual(perft(board, 1), 30)
        self.assertEqual(perft(board, 2), 900)

    def test_3(self):
        # stalemate
        board = shogi.Board('+R+N+SGKG+S+N+R/+B+N+SG+LG+S+N+B/P+LPP+LPP+LP/1P2P2P1/9/9/9/9/4k4 b 9P 200')
        self.assertEqual(perft(board, 1), 0)

    def test_4(self):
        # max perft with depth 1
        board = shogi.Board('R8/2K1S1SSk/4B4/9/9/9/9/9/1L1L1L3 b RBGSNLP3g3n17p 1')
        self.assertEqual(perft(board, 1), 593)

    def test_5(self):
        board = shogi.Board('4k4/9/9/9/9/9/9/9/9 b 16P 1')
        # 81 - (1 king) - (8 cannot move)
        self.assertEqual(perft(board, 1), 72)
        # 72 * 5 - (5 suicide move) = 355
        self.assertEqual(perft(board, 2), 355)

    def test_6(self):
        board = shogi.Board('r7k/6K2/7SP/4s2bb/9/9/9/9/9 b r4g2s4n4l17p 1')
        self.assertEqual(perft(board, 1), 4)

    def test_7(self):
        board = shogi.Board('l7l/5bS2/p1np5/6Sk1/4p2B1/PSpPPn1G1/1P1G2g1N/2+l6/L1KN1+r3 b R3Pgs7p 1')
        self.assertEqual(perft(board, 1), 1)

if __name__ == '__main__':
    unittest.main()
