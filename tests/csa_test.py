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
from mock import patch
from shogi import CSA

TEST_CSA = """'----------棋譜ファイルの例"example.csa"-----------------
'バージョン
V2.2
'対局者名
N+NAKAHARA
N-YONENAGA
'棋譜情報
'棋戦名
$EVENT:13th World Computer Shogi Championship
'対局場所
$SITE:KAZUSA ARC
'開始日時
$START_TIME:2003/05/03 10:30:00
'終了日時
$END_TIME:2003/05/03 11:11:05
'持ち時間:25分、切れ負け
$TIME_LIMIT:00:25+00
'戦型:矢倉
$OPENING:YAGURA
'平手の局面
P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
P2 * -HI *  *  *  *  * -KA * 
P3-FU-FU-FU-FU-FU-FU-FU-FU-FU
P4 *  *  *  *  *  *  *  *  * 
P5 *  *  *  *  *  *  *  *  * 
P6 *  *  *  *  *  *  *  *  * 
P7+FU+FU+FU+FU+FU+FU+FU+FU+FU
P8 * +KA *  *  *  *  * +HI * 
P9+KY+KE+GI+KI+OU+KI+GI+KE+KY
'先手番
+
'指し手と消費時間
+2726FU
T12
-3334FU
T6
%TORYO
'---------------------------------------------------------
"""

TEST_CSA_SUMMARY = {'moves': ['2g2f', '3c3d'], 'sfen': 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1', 'names': ['NAKAHARA', 'YONENAGA'], 'win': 'w'}

class ParserTest(unittest.TestCase):
    def parse_str_test(self):
        result = CSA.Parser.parse_str(TEST_CSA)
        self.assertEqual(result[0], TEST_CSA_SUMMARY)

TEST_SUMMARY = {
    'names': ['kiki_no_onaka_black', 'kiki_no_omata_white'],
    'sfen': 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1',
    'moves': [],
    'time': {'Time_Unit': '1sec', 'Total_Time': '900', 'Byoyomi': '0', 'Least_Time_Per_Move': '1'}
}

TEST_SUMMARY_STR = '''BEGIN Game_Summary
Protocol_Version:1.1
Protocol_Mode:Server
Format:Shogi 1.0
Declaration:Jishogi 1.1
Game_ID:20150505-CSA25-3-5-7
Name+:kiki_no_onaka_black
Name-:kiki_no_omata_white
Your_Turn:-
Rematch_On_Draw:NO
To_Move:+
Max_Moves:123
BEGIN Time
Time_Unit:1sec
Total_Time:900
Byoyomi:0
Least_Time_Per_Move:1
END Time
BEGIN Position
P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
P2 * -HI *  *  *  *  * -KA * 
P3-FU-FU-FU-FU-FU-FU-FU-FU-FU
P4 *  *  *  *  *  *  *  *  * 
P5 *  *  *  *  *  *  *  *  * 
P6 *  *  *  *  *  *  *  *  * 
P7+FU+FU+FU+FU+FU+FU+FU+FU+FU
P8 * +KA *  *  *  *  * +HI * 
P9+KY+KE+GI+KI+OU+KI+GI+KE+KY
+
END Position
END Game_Summary
'''

class TCPProtocolTest(unittest.TestCase):
    def setUp(self):
        patchers = []
        patchers.append(patch.object(CSA.TCPProtocol, 'connect', return_value=None))
        patchers.append(patch.object(CSA.TCPProtocol, 'write'))
        patchers.append(patch.object(CSA.TCPProtocol, 'read', return_value=0))
        for patcher in patchers:
            self.addCleanup(patcher.stop)
            patcher.start()

        self.maxDiff = None

    def add_response(self, csa_protocol, response):
        csa_protocol.recv_buf += response

    def test_login(self):
        tcp = CSA.TCPProtocol('127.0.0.1')
        self.add_response(tcp, 'LOGIN:python-syogi OK\n')
        login_result = tcp.login('python-syogi', 'password')
        self.assertTrue(login_result)

    def test_fail_login(self):
        tcp = CSA.TCPProtocol('127.0.0.1')
        self.add_response(tcp, 'LOGIN:incorrect\n')
        with self.assertRaises(ValueError):
            tcp.login('python-syogi', 'password')

    def test_wait_match(self):
        tcp = CSA.TCPProtocol('127.0.0.1')
        self.add_response(tcp, TEST_SUMMARY_STR)
        game_summary = tcp.wait_match()
        self.assertEqual(game_summary, {
            'summary': TEST_SUMMARY,
            'my_color': shogi.WHITE
        })

    def test_match(self):
        tcp = CSA.TCPProtocol('127.0.0.1')
        self.add_response(tcp, 'LOGIN:username OK\n')
        tcp.login('username', 'password')
        self.add_response(tcp, TEST_SUMMARY_STR)
        game_summary = tcp.wait_match()

        board = shogi.Board(game_summary['summary']['sfen'])
        self.add_response(tcp, 'START:20150505-CSA25-3-5-7\n')
        tcp.agree()

        self.add_response(tcp, '+5756FU,T1\n')
        (turn, usi, spend_time, message) = tcp.wait_server_message(board)
        board.push(shogi.Move.from_usi(usi))
        self.assertEqual(turn, shogi.BLACK)
        self.assertEqual(spend_time, 1.0)

        self.assertEqual(board.sfen(), 'lnsgkgsnl/1r5b1/ppppppppp/9/9/4P4/PPPP1PPPP/1B5R1/LNSGKGSNL w - 2')
        
        next_move = shogi.Move.from_usi('8c8d')
        board.push(next_move)
        self.add_response(tcp, '-8384FU,T2\n')
        response_line = tcp.move(board.pieces[next_move.to_square], shogi.WHITE, next_move)
        (turn, usi, spend_time, message) = tcp.parse_server_message(response_line, board)
        self.assertEqual(turn, shogi.WHITE)
        self.assertEqual(spend_time, 2.0)

if __name__ == '__main__':
    unittest.main()
