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
from shogi import KIF

TEST_KIF_STR = """開始日時：2006/12/15 21:03\r
消費時間：▲359△359\r
棋戦：順位戦\r
戦型：四間飛車\r
\r
場所：東京「将棋会館」\r
\r
持ち時間：6時間\r
\r
手合割：平手\r
\r
後手：藤井猛\r
先手：羽生善治\r
手数----指手---------消費時間--\r
*棋戦詳細：第65期順位戦A級06回戦\r
*「羽生善治王将」vs「藤井　猛九段」\r
   1 ７六歩(77)        \r
   2 ３四歩(33)        \r
   3 ２六歩(27)        \r
   4 ４四歩(43)        \r
   5 ４八銀(39)        \r
   6 ４二飛(82)        \r
   7 ６八王(59)        \r
   8 ６二王(51)        \r
   9 ７八王(68)        \r
  10 ７二王(62)        \r
  11 ５六歩(57)        \r
  12 ３二銀(31)        \r
  13 ５七銀(48)        \r
  14 ４三銀(32)        \r
  15 ７七角(88)        \r
  16 ８二王(72)        \r
  17 ２五歩(26)        \r
  18 ３三角(22)        \r
  19 ８八王(78)        \r
  20 ５四銀(43)        \r
  21 ６六歩(67)        \r
  22 ９二香(91)        \r
  23 ９八香(99)        \r
  24 ９一王(82)        \r
  25 ９九王(88)        \r
  26 ８二銀(71)        \r
  27 ８八銀(79)        \r
  28 ７一金(61)        \r
  29 ５八金(49)        \r
  30 ７四歩(73)        \r
  31 ６八金(58)        \r
  32 ５二金(41)        \r
  33 ９六歩(97)        \r
  34 ９四歩(93)        \r
  35 ７九金(69)        \r
  36 ６二金(52)        \r
  37 ７八金(68)        \r
  38 １四歩(13)        \r
  39 １六歩(17)        \r
  40 ６四歩(63)        \r
  41 ２六飛(28)        \r
  42 ４五歩(44)        \r
  43 ３六飛(26)        \r
  44 ４三銀(54)        \r
  45 ６八銀(57)        \r
  46 ７二金(62)        \r
  47 ８六歩(87)        \r
  48 ５四歩(53)        \r
  49 ６五歩(66)        \r
  50 同　歩(64)        \r
  51 ３三角成(77)      \r
  52 同　桂(21)        \r
  53 ３一角打          \r
  54 ４一飛(42)        \r
  55 ６四角成(31)      \r
  56 ７三銀(82)        \r
  57 ６五馬(64)        \r
  58 ６一飛(41)        \r
  59 ６四歩打          \r
  60 ３九角打          \r
  61 ５五歩(56)        \r
  62 ６四銀(73)        \r
  63 ７四馬(65)        \r
  64 ７三金(72)        \r
  65 同　馬(74)        \r
  66 同　銀(64)        \r
  67 ５四歩(55)        \r
  68 ５二歩打          \r
  69 ６七歩打          \r
  70 ６三飛(61)        \r
  71 １七桂(29)        \r
  72 ９三角成(39)      \r
  73 ５六飛(36)        \r
  74 ４四銀(43)        \r
  75 ２四歩(25)        \r
  76 同　歩(23)        \r
  77 ２六飛(56)        \r
  78 ３五銀(44)        \r
  79 ５六飛(26)        \r
  80 ７四角打          \r
  81 ５三歩成(54)      \r
  82 同　歩(52)        \r
  83 ６六飛(56)        \r
  84 ６四歩打          \r
  85 ７五歩(76)        \r
  86 ４七角成(74)      \r
  87 ７七銀(68)        \r
  88 ７四歩打          \r
  89 ８五歩(86)        \r
  90 ７五歩(74)        \r
  91 ５二歩打          \r
  92 ６一金(71)        \r
  93 ８七銀(88)        \r
  94 ５二金(61)        \r
  95 ８八金(79)        \r
  96 ６二金(52)        \r
  97 ２三金打          \r
  98 ５四歩(53)        \r
  99 ３六歩(37)        \r
 100 ４四銀(35)        \r
 101 ２四金(23)        \r
 102 ７四銀(73)        \r
 103 ９五歩(96)        \r
 104 同　歩(94)        \r
 105 ３五歩(36)        \r
 106 ４六歩(45)        \r
 107 ３四歩(35)        \r
 108 ４五桂(33)        \r
 109 ３三歩成(34)      \r
 110 ８四歩(83)        \r
 111 ４八歩打          \r
 112 ３六馬(47)        \r
 113 ８六銀(77)        \r
 114 ８二馬(93)        \r
 115 ８四歩(85)        \r
 116 ８五歩打          \r
 117 ９五銀(86)        \r
 118 同　香(92)        \r
 119 同　香(98)        \r
 120 ９四歩打          \r
 121 同　香(95)        \r
 122 ９三歩打          \r
 123 ８三香打          \r
 124 同　銀(74)        \r
 125 同　歩成(84)      \r
 126 同　馬(82)        \r
 127 ９三香成(94)      \r
 128 同　桂(81)        \r
 129 ９四歩打          \r
 130 ９五香打          \r
 131 ９六銀(87)        \r
 132 ９八歩打          \r
 133 同　王(99)        \r
 134 ９六香(95)        \r
 135 同　飛(66)        \r
 136 ９五歩打          \r
 137 同　飛(96)        \r
 138 ９二歩打          \r
 139 ９三歩成(94)      \r
 140 同　歩(92)        \r
 141 ８五飛(95)        \r
 142 ８四香打          \r
 143 同　飛(85)        \r
 144 同　馬(83)        \r
 145 ８七香打          \r
 146 ８五歩打          \r
 147 ９六桂打          \r
 148 ７四馬(84)        \r
 149 ８四香打          \r
 150 ７二金(62)        \r
 151 ９二歩打          \r
 152 同　馬(74)        \r
 153 ８三歩打          \r
 154 ９五銀打          \r
 155 ８二銀打          \r
 156 同　金(72)        \r
 157 同　歩成(83)      \r
 158 同　馬(92)        \r
 159 同　香成(84)      \r
 160 同　王(91)        \r
 161 ７四金打          \r
 162 ７二銀打          \r
 163 ８三歩打          \r
 164 同　飛(63)        \r
 165 ８四歩打          \r
 166 ５三飛(83)        \r
 167 ７三歩打          \r
 168 同　飛(53)        \r
 169 ９一角打          \r
 170 同　王(82)        \r
 171 ７三金(74)        \r
 172 同　銀(72)        \r
 173 ８三歩成(84)      \r
 174 ８一金打          \r
 175 ９二歩打          \r
 176 同　金(81)        \r
 177 ７一飛打          \r
 178 ８一香打          \r
 179 ９二と(83)        \r
 180 同　王(91)        \r
 181 ７二飛成(71)      \r
 182 投了         \r
まで181手で先手の勝ち\r
"""

TEST_KIF_RESULT = {
    'moves': [
        '7g7f', '3c3d', '2g2f', '4c4d', '3i4h', '8b4b', '5i6h', '5a6b', '6h7h',
        '6b7b', '5g5f', '3a3b', '4h5g', '3b4c', '8h7g', '7b8b', '2f2e', '2b3c',
        '7h8h', '4c5d', '6g6f', '9a9b', '9i9h', '8b9a', '8h9i', '7a8b', '7i8h',
        '6a7a', '4i5h', '7c7d', '5h6h', '4a5b', '9g9f', '9c9d', '6i7i', '5b6b',
        '6h7h', '1c1d', '1g1f', '6c6d', '2h2f', '4d4e', '2f3f', '5d4c', '5g6h',
        '6b7b', '8g8f', '5c5d', '6f6e', '6d6e', '7g3c+', '2a3c', 'B*3a', '4b4a',
        '3a6d+', '8b7c', '6d6e', '4a6a', 'P*6d', 'B*3i', '5f5e', '7c6d', '6e7d',
        '7b7c', '7d7c', '6d7c', '5e5d', 'P*5b', 'P*6g', '6a6c', '2i1g', '3i9c+',
        '3f5f', '4c4d', '2e2d', '2c2d', '5f2f', '4d3e', '2f5f', 'B*7d', '5d5c+',
        '5b5c', '5f6f', 'P*6d', '7f7e', '7d4g+', '6h7g', 'P*7d', '8f8e', '7d7e',
        'P*5b', '7a6a', '8h8g', '6a5b', '7i8h', '5b6b', 'G*2c', '5c5d', '3g3f',
        '3e4d', '2c2d', '7c7d', '9f9e', '9d9e', '3f3e', '4e4f', '3e3d', '3c4e',
        '3d3c+', '8c8d', 'P*4h', '4g3f', '7g8f', '9c8b', '8e8d', 'P*8e', '8f9e',
        '9b9e', '9h9e', 'P*9d', '9e9d', 'P*9c', 'L*8c', '7d8c', '8d8c+', '8b8c',
        '9d9c+', '8a9c', 'P*9d', 'L*9e', '8g9f', 'P*9h', '9i9h', '9e9f', '6f9f',
        'P*9e', '9f9e', 'P*9b', '9d9c+', '9b9c', '9e8e', 'L*8d', '8e8d', '8c8d',
        'L*8g', 'P*8e', 'N*9f', '8d7d', 'L*8d', '6b7b', 'P*9b', '7d9b', 'P*8c',
        'S*9e', 'S*8b', '7b8b', '8c8b+', '9b8b', '8d8b+', '9a8b', 'G*7d', 'S*7b',
        'P*8c', '6c8c', 'P*8d', '8c5c', 'P*7c', '5c7c', 'B*9a', '8b9a', '7d7c',
        '7b7c', '8d8c+', 'G*8a', 'P*9b', '8a9b', 'R*7a', 'L*8a', '8c9b', '9a9b',
        '7a7b+'
    ],
    'sfen': 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1',
    'names': ['\u7fbd\u751f\u5584\u6cbb', '\u85e4\u4e95\u731b'],
    'win': 'b'
}

class ParserTest(unittest.TestCase):
    def parse_str_test(self):
        result = KIF.Parser.parse_str(TEST_KIF_STR)
        self.assertEqual(result[0], TEST_KIF_RESULT)
