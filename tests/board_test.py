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

class BoardTestCase(unittest.TestCase):
    def test_default(self):
        board_none = shogi.Board()
        board_sfen = shogi.Board(shogi.STARTING_SFEN)
        self.assertEqual(board_none, board_sfen)
        self.assertEqual(board_none.sfen(), shogi.STARTING_SFEN)
        self.assertEqual(str(board_none), str(board_sfen))
        self.assertEqual(repr(board_none), repr(board_sfen))
        self.assertEqual(board_none.turn, shogi.BLACK)

    def test_stalemate(self):
        board = shogi.Board('+R+N+SGKG+S+N+R/+B+N+SG+LG+S+N+B/P+LPP+LPP+LP/1P2P2P1/9/9/9/9/6k2 b - 200')
        self.assertEqual(len(board.pseudo_legal_moves), 0)

    def test_bishop_center(self):
        board = shogi.Board('9/9/9/9/4B4/9/9/9/9 b - 1')
        self.assertTrue(shogi.Move.from_usi('5e4d') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e3c') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e2b') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e1a') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e6f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e7g') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e8h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e9i') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e4f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e3g') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e2h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e1i') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e6d') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e7c') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e8b') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e9a') in board.legal_moves)

        self.assertTrue(shogi.Move.from_usi('5e3c+') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e2b+') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e1a+') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e7c+') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e8b+') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5e9a+') in board.legal_moves)

        self.assertEqual(len(board.legal_moves), 22)

    def test_bishop_9a(self):
        board = shogi.Board('B8/9/9/9/9/9/9/9/9 b - 1')
        self.assertEqual(len(board.legal_moves), 16)

    def test_double_pawn_in_a_row(self):
        board = shogi.Board('k8/9/9/9/9/9/9/9/P8 b P 1')
        self.assertFalse(shogi.Move.from_usi('P*9b') in board.legal_moves)
        self.assertFalse(shogi.Move.from_usi('P*9c') in board.legal_moves)
        self.assertFalse(shogi.Move.from_usi('P*9d') in board.legal_moves)
        self.assertFalse(shogi.Move.from_usi('P*9e') in board.legal_moves)
        self.assertFalse(shogi.Move.from_usi('P*9f') in board.legal_moves)
        self.assertFalse(shogi.Move.from_usi('P*9g') in board.legal_moves)
        self.assertFalse(shogi.Move.from_usi('P*9h') in board.legal_moves)
        self.assertEqual(len(board.legal_moves), 65)

    def test_suicide(self):
        board = shogi.Board('1k7/9/1G7/9/9/9/9/9/9 w - 1')
        self.assertTrue(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('8a8b')))
        self.assertTrue(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('8a9b')))
        self.assertTrue(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('8a7b')))
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('8a6b')))
        self.assertEqual(len(board.legal_moves), 2)

    def test_check_by_dropping_pawn(self):
        # check by dropping pawn
        board = shogi.Board('kn7/9/1G7/9/9/9/9/9/9 b P 1')
        self.assertTrue(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('P*9b')))
        self.assertEqual(len(board.legal_moves), 76)
        board = shogi.Board('kn7/9/9/1NN6/9/9/9/9/9 b P 1')
        self.assertTrue(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('P*9b')))
        self.assertEqual(len(board.legal_moves), 73)

        # king can escape
        board = shogi.Board('k8/9/9/9/9/9/9/9/9 b P 1')
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('P*9b')))
        self.assertEqual(len(board.legal_moves), 72)

        # dropping pawn is not protected and king cannot escape
        board = shogi.Board('kn7/1n7/9/9/9/9/9/9/9 b P 1')
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('P*9b')))
        self.assertEqual(len(board.legal_moves), 71)

        # dropping pawn is protected but king can escape
        board = shogi.Board('kn7/9/9/1N7/9/9/9/9/9 b P 1')
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('P*9b')))
        self.assertEqual(len(board.legal_moves), 73)
        board = shogi.Board('k8/9/1S7/9/9/9/9/9/9 b P 1')
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('P*9b')))
        self.assertEqual(len(board.legal_moves), 81)

        # dropping pawn can be captured other pieces besides king
        board = shogi.Board('kg7/9/1G7/9/9/9/9/9/9 b P 1')
        self.assertFalse(board.is_suicide_or_check_by_dropping_pawn(shogi.Move.from_usi('P*9b')))
        self.assertEqual(len(board.legal_moves), 77)

    def test_lance_move(self):
        board = shogi.Board('9/9/9/9/4L4/9/9/9/9 b - 1')
        self.assertEqual(len(board.legal_moves), 6)

    def test_is_fourfold_repetition(self):
        board = shogi.Board('ln3g2l/1r2g1sk1/1pp1ppn2/p2ps1ppp/1PP6/2GP4P/P1N1PPPP1/1R2S1SK1/L4G1NL w Bb 44')
        for move_str in ['9d9e', '8h6h', '8b6b', '6h8h', '6b8b', '8h6h', '8b6b', '6h8h',
                         '6b8b', '8h6h', '8b6b', '6h8h']:
            board.push(shogi.Move.from_usi(move_str))
        self.assertFalse(board.is_fourfold_repetition())
        board.push(shogi.Move.from_usi('6b8b'))
        self.assertTrue(board.is_fourfold_repetition())

    def test_legal_moves_in(self):
        # https://github.com/gunyarakun/python-shogi/issues/3
        board = shogi.Board()
        self.assertTrue(shogi.Move.from_usi('9g9f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('8g8f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('7g7f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('6g6f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5g5f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('4g4f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('3g3f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('2g2f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('1g1f') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('9i9h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('1i1h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('7i7h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('7i6h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('3i4h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('3i3h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('6i7h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('6i6h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('6i5h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('4i5h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('4i4h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('4i3h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('2h7h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('2h6h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('2h5h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('2h4h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('2h3h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('2h1h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5i6h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5i5h') in board.legal_moves)
        self.assertTrue(shogi.Move.from_usi('5i4h') in board.legal_moves)

        # opposite turn
        self.assertFalse(shogi.Move.from_usi('9c9d') in board.legal_moves)

if __name__ == '__main__':
    unittest.main()
