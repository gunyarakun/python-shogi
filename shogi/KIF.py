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

# NOTE: Don't support ki2(Kifu2) format

from __future__ import unicode_literals

import os
import re
import shogi
import codecs

class ParserException(Exception):
    pass

class Parser:
    MOVE_RE = re.compile(r'\A *[0-9]+\s+(中断|投了|持将棋|先日手|詰み|切れ負け|反則勝ち|反則負け|(([１２３４５６７８９])([零一二三四五六七八九])|同　)([歩香桂銀金角飛玉と杏圭全馬龍])(打|(成?)\(([0-9])([0-9])\)))\s*(\([ /:0-9]+\))?\s*\Z')

    HANDYCAP_SFENS = {
        '平手': shogi.STARTING_SFEN,
        '香落ち': 'lnsgkgsn1/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '右香落ち': '1nsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '角落ち': 'lnsgkgsnl/1r7/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '飛車落ち': 'lnsgkgsnl/7b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '飛香落ち': 'lnsgkgsn1/7b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '二枚落ち': 'lnsgkgsnl/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '三枚落ち': 'lnsgkgsn1/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '四枚落ち': '1nsgkgsn1/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '五枚落ち': '2sgkgsn1/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '左五枚落ち': '1nsgkgs2/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '六枚落ち': '2sgkgs2/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '八枚落ち': '4k4/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        'その他': None
    }

    RESULT_RE = re.compile(r'　*まで(\d+)手で((先|下|後|上)手の勝ち|千日手|持将棋|中断)')

    @staticmethod
    def parse_file(path):
        prefix, ext = os.path.splitext(path)
        for enc in ['cp932', 'utf-8-sig']:
            try:
                with codecs.open(path, 'r', enc) as f:
                    return Parser.parse_str(f.read())
            except:
                pass
        return None

    @staticmethod
    def parse_pieces_in_hand(target):
        if target == 'なし': # None in japanese
            return {}

        result = {}
        for item in target.split('　'):
            if len(item) == 1:
                result[shogi.PIECE_JAPANESE_SYMBOLS.index(item)] = 1
            elif len(item) == 2 or len(item) == 3:
                result[shogi.PIECE_JAPANESE_SYMBOLS.index(item[0])] = \
                    shogi.NUMBER_JAPANESE_KANJI_SYMBOLS.index(item[1:])
            elif len(item) == 0:
                pass
            else:
                raise ParserException('Invalid pieces in hand')
        return result

    @staticmethod
    def parse_move_str(line, last_to_square):
        # Normalize king/promoted kanji
        line = line.replace('王', '玉')
        line = line.replace('竜', '龍')
        line = line.replace('成銀', '全')
        line = line.replace('成桂', '圭')
        line = line.replace('成香', '杏')

        m = Parser.MOVE_RE.match(line)
        if m:
            if m.group(1) in [
                    '中断',
                    '投了',
                    '持将棋',
                    '千日手',
                    '詰み',
                    '切れ負け',
                    '反則か勝ち',
                    '反則負け'
            ]:
                return (
                    None,
                    None,
                    m.group(1)
                )

            piece_type = shogi.PIECE_JAPANESE_SYMBOLS.index(m.group(5))
            if m.group(2) == '同　':
                # same position
                to_square = last_to_square
            else:
                to_field = 9 - shogi.NUMBER_JAPANESE_NUMBER_SYMBOLS.index(m.group(3))
                to_rank = shogi.NUMBER_JAPANESE_KANJI_SYMBOLS.index(m.group(4)) - 1
                to_square = to_rank * 9 + to_field
                last_to_square = to_square

            if m.group(6) == '打':
                # piece drop
                return (
                    '{0}*{1}'.format(shogi.PIECE_SYMBOLS[piece_type].upper(), shogi.SQUARE_NAMES[to_square]),
                    last_to_square,
                    None
                )
            else:
                from_field = 9 - int(m.group(8))
                from_rank = int(m.group(9)) - 1
                from_square = from_rank * 9 + from_field

                promotion = (m.group(7) == '成')
                return (
                    shogi.SQUARE_NAMES[from_square] + shogi.SQUARE_NAMES[to_square] + ('+' if promotion else ''),
                    last_to_square,
                    None
                )
        return (None, last_to_square, None)

    @staticmethod
    def parse_str(kif_str):
        line_no = 1

        names = [None, None]
        pieces_in_hand = [{}, {}]
        current_turn = shogi.BLACK
        sfen = shogi.STARTING_SFEN
        moves = []
        last_to_square = None
        win = None
        kif_str = kif_str.replace('\r\n', '\n').replace('\r', '\n')
        for line in kif_str.split('\n'):
            if len(line) == 0 or line[0] == "*":
                pass
            elif '：' in line:
                (key, value) = line.split('：', 1)
                value = value.rstrip('　')
                if key == '先手' or key == '下手': # sente or shitate
                    # Blacks's name
                    names[shogi.BLACK] = value
                elif key == '後手' or key == '上手': # gote or uwate
                    # White's name
                    names[shogi.WHITE] = value
                elif key == '先手の持駒' or \
                        key == '下手の持駒': # sente or shitate's pieces in hand
                    # First player's pieces in hand
                    pieces_in_hand[shogi.BLACK] == Parser.parse_pieces_in_hand(value)
                elif key == '後手の持駒' or \
                        key == '上手の持駒': # gote or uwate's pieces in hand
                    # Second player's pieces in hand
                    pieces_in_hand[shogi.WHITE] == Parser.parse_pieces_in_hand(value)
                elif key == '手合割': # teai wari
                    sfen = Parser.HANDYCAP_SFENS[value]
                    if sfen is None:
                        raise ParserException('Cannot support handycap type "other"')
            elif line == '後手番':
                # Current turn is white
                current_turn = shogi.WHITE
            else:
                (move, last_to_square, special_str) = Parser.parse_move_str(line, last_to_square)
                if move is not None:
                    moves.append(move)
                    if current_turn == shogi.BLACK:
                        current_turn = shogi.WHITE
                    else: # current_turn == shogi.WHITE
                        current_turn = shogi.BLACK
                elif special_str in ['投了', '詰み', '切れ負け', '反則負け']:
                    if current_turn == shogi.BLACK:
                        win = 'w'
                    else: # current_turn == shogi.WHITE
                        win = 'b'
                elif special_str in ['反則勝ち', '入玉勝ち']:
                    if current_turn == shogi.BLACK:
                        win = 'b'
                    else: # current_turn == shogi.WHITE
                        win = 'w'
                elif special_str in ['持将棋', '先日手']:
                    win = '-'
                else:
                    m = Parser.RESULT_RE.match(line)
                    if m:
                        win_side_str = m.group(3)
                        if win_side_str == '先' or win_side_str == '下':
                            win = 'b'
                        elif win_side_str == '後' or win_side_str == '上':
                            win = 'w'
                        else:
                            # TODO: repetition of moves with continuous check
                            win = '-'
            line_no += 1

        summary = {
            'names': names,
            'sfen': sfen,
            'moves': moves,
            'win': win
        }

        # NOTE: for the same interface with CSA parser
        return [summary]
