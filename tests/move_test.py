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

class MoveTestCase(unittest.TestCase):
    def test_issue_8(self):
        move = shogi.Move.from_usi('9a9b')
        self.assertEqual(move.__hash__(), 9)

    def test_issue_9(self):
        self.assertEqual(bool(shogi.Move.null()), False)
        board = shogi.Board()
        board.push(shogi.Move.null())
        self.assertEqual(board.captured_piece_stack[0], 0)

if __name__ == '__main__':
    unittest.main()
