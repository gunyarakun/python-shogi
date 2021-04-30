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

import os
import codecs
import shutil
import unittest
import tempfile
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

TEST_KIF_STR_WITH_TIME = """# --- Kifu for Windows (HTTP) V6.54 棋譜ファイル ---
対局ID：1234\r
開始日時：2013/08/08 09:00\r
終了日時：2013/08/09 17:40\r
表題：王位戦\r
棋戦：第５４期王位戦七番勝負　第４局\r
持ち時間：各８時間\r
消費時間：78▲452△442\r
場所：ホテル日航福岡\r
図：投了\r
手合割：平手　　\r
先手：行方尚史\r
後手：羽生善治\r
先手省略名：行方\r
後手省略名：羽生\r
手数----指手---------消費時間--\r
*ホテルアイネにて\r
*\r
*コメントは複数行あるよ\r
   1 ７六歩(77)   ( 0:00/00:00:00)\r
*手の間にもコメントはある。\r
*こんな感じ\r
   2 ３四歩(33)   ( 0:00/00:00:00)\r
   3 ２六歩(27)   ( 0:00/00:00:00)\r
   4 ８四歩(83)   ( 0:00/00:00:00)\r
   5 ２五歩(26)   ( 0:00/00:00:00)\r
   6 ８五歩(84)   ( 0:00/00:00:00)\r
   7 ７八金(69)   ( 0:00/00:00:00)\r
   8 ３二金(41)   ( 0:00/00:00:00)\r
   9 ２四歩(25)   ( 0:00/00:00:00)\r
  10 同　歩(23)   ( 0:00/00:00:00)\r
  11 同　飛(28)   ( 0:00/00:00:00)\r
  12 ８六歩(85)   ( 0:00/00:00:00)\r
  13 同　歩(87)   ( 0:00/00:00:00)\r
  14 同　飛(82)   ( 0:00/00:00:00)\r
  15 ３四飛(24)   ( 0:00/00:00:00)\r
  16 ３三角(22)   ( 0:00/00:00:00)\r
  17 ３六飛(34)   ( 0:00/00:00:00)\r
  18 ８四飛(86)   ( 0:00/00:00:00)\r
  19 ２六飛(36)   ( 0:00/00:00:00)\r
  20 ２二銀(31)   ( 0:00/00:00:00)\r
  21 ８七歩打     ( 0:00/00:00:00)\r
  22 ５二玉(51)   ( 0:00/00:00:00)\r
  23 ４八銀(39)   ( 0:00/00:00:00)\r
  24 １四歩(13)   ( 0:00/00:00:00)\r
  25 １六歩(17)   ( 0:00/00:00:00)\r
  26 ２三銀(22)   ( 0:00/00:00:00)\r
  27 ５八玉(59)   ( 0:00/00:00:00)\r
  28 ５一金(61)   ( 0:00/00:00:00)\r
  29 ３八金(49)   ( 0:00/00:00:00)\r
  30 ６二銀(71)   ( 0:00/00:00:00)\r
  31 ７七角(88)   ( 0:00/00:00:00)\r
  32 ９四歩(93)   ( 0:00/00:00:00)\r
  33 ９六歩(97)   ( 0:00/00:00:00)\r
  34 ７七角成(33) ( 0:00/00:00:00)\r
  35 同　桂(89)   ( 0:00/00:00:00)\r
  36 ３三桂(21)   ( 0:00/00:00:00)\r
  37 ６八銀(79)   ( 0:00/00:00:00)\r
  38 ９三桂(81)   ( 0:00/00:00:00)\r
  39 ７五歩(76)   ( 0:00/00:00:00)\r
  40 ２四歩打     ( 0:00/00:00:00)\r
  41 ７四歩(75)   ( 0:00/00:00:00)\r
  42 同　歩(73)   ( 0:00/00:00:00)\r
  43 ７二歩打     ( 0:00/00:00:00)\r
  44 ６一金(51)   ( 0:00/00:00:00)\r
  45 ８六飛(26)   ( 0:00/00:00:00)\r
*昼食休憩へ。\r
*おなかすいた。\r
  46 同　飛(84)   ( 0:00/00:00:00)\r
  47 同　歩(87)   ( 0:00/00:00:00)\r
  48 ８九飛打     ( 0:00/00:00:00)\r
  49 ７九金(78)   ( 0:00/00:00:00)\r
  50 ９九飛成(89) ( 0:00/00:00:00)\r
  51 ８一飛打     ( 0:00/00:00:00)\r
  52 ７五香打     ( 0:00/00:00:00)\r
  53 ４一角打     ( 0:00/00:00:00)\r
*午後のおやつは、ミルクレープ。\r
  54 ５一玉(52)   ( 0:00/00:00:00)\r
  55 ５九銀(48)   ( 0:00/00:00:00)\r
  56 ７七香成(75) ( 0:00/00:00:00)\r
  57 同　銀(68)   ( 0:00/00:00:00)\r
  58 ７九龍(99)   ( 0:00/00:00:00)\r
  59 ６八銀(77)   ( 0:00/00:00:00)\r
  60 ９九龍(79)   ( 0:00/00:00:00)\r
  61 ５二香打     ( 0:00/00:00:00)\r
  62 ４二玉(51)   ( 0:00/00:00:00)\r
  63 ６一飛成(81) ( 0:00/00:00:00)\r
  64 ７六桂打     ( 0:00/00:00:00)\r
  65 ７九金打     ( 0:00/00:00:00)\r
  66 ６八桂成(76) ( 0:00/00:00:00)\r
  67 同　金(79)   ( 0:00/00:00:00)\r
  68 ４五桂(33)   ( 0:00/00:00:00)\r
  69 ６二龍(61)   ( 0:00/00:00:00)\r
  70 ８四角打     ( 0:00/00:00:00)\r
  71 ５一龍(62)   ( 0:00/00:00:00)\r
  72 同　角(84)   ( 0:00/00:00:00)\r
  73 同　香成(52) ( 0:00/00:00:00)\r
  74 ５七桂成(45) ( 0:00/00:00:00)\r
  75 同　金(68)   ( 0:00/00:00:00)\r
  76 ５九龍(99)   ( 0:00/00:00:00)\r
  77 同　玉(58)   ( 0:00/00:00:00)\r
  78 ７九飛打     ( 0:00/00:00:00)\r
*この手にて投了。\r
  79 投了         ( 0:00/00:00:00)\r
まで78手で後手の勝ち\r
"""

TEST_KIF_81DOJO = """#KIF version=2.0 encoding=UTF-8\r
開始日時：2020/12/31\r
場所：81Dojo\r
持ち時間：0分+10秒\r
手合割：平手\r
先手：KikiNoOmata\r
後手：XiaoNoOmata\r
手数----指手---------消費時間--\r
1   ７六歩(77)   (0:2/0:0:2)\r
2   ３四歩(33)   (0:5/0:0:5)\r
3   ７五歩(76)   (0:2/0:0:4)\r
4   ４四歩(43)   (0:8/0:0:13)\r
5   ７八飛(28)   (0:2/0:0:6)\r
6   ４二飛(82)   (0:1/0:0:14)\r
7   ６八銀(79)   (0:2/0:0:8)\r
8   ８二銀(71)   (0:2/0:0:16)\r
9   ７四歩(75)   (0:1/0:0:9)\r
10   同　歩(73)   (0:1/0:0:17)\r
11   同　飛(78)   (0:1/0:0:10)\r
12   投了   (0:5/0:0:22)\r
"""


TEST_KIF_CUSTOM_BOARD = """# ----  Kifu for Windows V4.01β 棋譜ファイル  ----
# ファイル名：D:\\b\\temp\\M2TOK141\\KIFU\\1t120600-1.kif
棋戦：１手詰
戦型：なし
手合割：平手　　
後手の持駒：飛　角　金四　銀三　桂四　香三　歩十七　
  ９ ８ ７ ６ ５ ４ ３ ２ １
+---------------------------+
| ・ ・ ・ ・ ・ ・ ・ ・v香|一
| ・ ・ ・ ・ 飛 馬 ・ ・v玉|二
| ・ ・ ・ ・ ・ ・ ・v歩 ・|三
| ・ ・ ・ ・ ・ ・v銀 ・ ・|四
| ・ ・ ・ ・ ・ ・ ・ ・ ・|五
| ・ ・ ・ ・ ・ ・ ・ ・ ・|六
| ・ ・ ・ ・ ・ ・ ・ ・ ・|七
| ・ ・ ・ ・ ・ ・ ・ ・ ・|八
| ・ ・ ・ ・ ・ ・ ・ ・ ・|九
+---------------------------+
先手の持駒：なし
先手：大内延介
後手：最新詰将棋２００選
手数----指手---------消費時間--
*作者：大内延介
*発表誌：最新詰将棋２００選
   1 ３一馬(42)   ( 0:00/00:00:00)
   2 中断         ( 0:00/00:00:00)
まで1手で中断
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

TEST_KIF_WITH_TIME_RESULT = {
    'moves': [
        '7g7f', '3c3d', '2g2f', '8c8d', '2f2e', '8d8e', '6i7h', '4a3b', '2e2d', '2c2d',
        '2h2d', '8e8f', '8g8f', '8b8f', '2d3d', '2b3c', '3d3f', '8f8d', '3f2f', '3a2b',
        'P*8g', '5a5b', '3i4h', '1c1d', '1g1f', '2b2c', '5i5h', '6a5a', '4i3h', '7a6b',
        '8h7g', '9c9d', '9g9f', '3c7g+', '8i7g', '2a3c', '7i6h', '8a9c', '7f7e', 'P*2d',
        '7e7d', '7c7d', 'P*7b', '5a6a', '2f8f', '8d8f', '8g8f', 'R*8i', '7h7i', '8i9i+',
        'R*8a', 'L*7e', 'B*4a', '5b5a', '4h5i', '7e7g+', '6h7g', '9i7i', '7g6h', '7i9i',
        'L*5b', '5a4b', '8a6a+', 'N*7f', 'G*7i', '7f6h+', '7i6h', '3c4e', '6a6b', 'B*8d',
        '6b5a', '8d5a', '5b5a+', '4e5g+', '6h5g', '9i5i', '5h5i', 'R*7i'
    ],
    'sfen': 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1',
    'names': [u'\u884c\u65b9\u5c1a\u53f2', u'\u7fbd\u751f\u5584\u6cbb'],
    'win': 'w',
}

TEST_KIF_81DOJO_RESULT = {
    'moves': [
        '7g7f', '3c3d', '7f7e', '4c4d', '2h7h', '8b4b', '7i6h', '7a8b', '7e7d', '7c7d', '7h7d'
    ],
    'sfen': 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1',
    'names': ['KikiNoOmata', 'XiaoNoOmata'],
    'win': 'b',
}

TEST_KIF_CUSTOM_BOARD_RESULT = {'names': ['大内延介', '最新詰将棋２００選'],
                                'sfen': '8l/4R+B2k/7p1/6s2/9/9/9/9/9 w 1r1b4g3s4n3l17p 1',
                                'moves': ['4b3a'],
                                'win': '-'}

class ParserTest(unittest.TestCase):
    def test_parse_str(self):
        result = KIF.Parser.parse_str(TEST_KIF_STR)
        self.assertEqual(result[0], TEST_KIF_RESULT)

    def test_parse_str_with_time(self):
        result = KIF.Parser.parse_str(TEST_KIF_STR_WITH_TIME)
        self.assertEqual(result[0], TEST_KIF_WITH_TIME_RESULT)

    def test_parse_str_81dojo(self):
        result = KIF.Parser.parse_str(TEST_KIF_81DOJO)
        self.assertEqual(result[0], TEST_KIF_81DOJO_RESULT)

    def test_parse_file(self):
        try:
            tempdir = tempfile.mkdtemp()

            # cp932
            path = os.path.join(tempdir, 'test1.kif')
            with codecs.open(path, 'w', 'cp932') as f:
                f.write(TEST_KIF_STR)
            result = KIF.Parser.parse_file(path)
            self.assertEqual(result[0], TEST_KIF_RESULT)

            # utf-8
            path = os.path.join(tempdir, 'test2.kif')
            with codecs.open(path, 'w', 'utf-8') as f:
                f.write(TEST_KIF_STR)
            result = KIF.Parser.parse_file(path)
            self.assertEqual(result[0], TEST_KIF_RESULT)

            # utf-8 (BOM)
            path = os.path.join(tempdir, 'test3.kif')
            with codecs.open(path, 'w', 'utf-8-sig') as f:
                f.write(TEST_KIF_STR)
            result = KIF.Parser.parse_file(path)
            self.assertEqual(result[0], TEST_KIF_RESULT)

            # .kif with custom starting position
            path = os.path.join(tempdir, 'test_tsume.kif')
            with codecs.open(path, 'w', 'cp932') as f:
                f.write(TEST_KIF_CUSTOM_BOARD)
            result = KIF.Parser.parse_file(path)
            self.assertEqual(result[0], TEST_KIF_CUSTOM_BOARD_RESULT)

        finally:
            shutil.rmtree(tempdir)
