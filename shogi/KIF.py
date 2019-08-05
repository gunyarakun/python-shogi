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
    MOVE_RE = re.compile(r'\A *[0-9]+ (\u4e2d\u65ad|\u6295\u4e86|\u6301\u5c06\u68cb|\u5148\u65e5\u624b|\u8a70\u307f|\u5207\u308c\u8ca0\u3051|\u53cd\u5247\u52dd\u3061|\u53cd\u5247\u8ca0\u3051|(([\uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18\uff19])([\u96f6\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d])|\u540c\u3000)([\u6b69\u9999\u6842\u9280\u91d1\u89d2\u98db\u7389\u3068\u674f\u572d\u5168\u99ac\u9f8d])(\u6253|(\u6210?)\(([0-9])([0-9])\)))\s*(\([ /:0-9]+\))?\s*\Z')

    HANDYCAP_SFENS = {
        '\u5e73\u624b': shogi.STARTING_SFEN,
        '\u9999\u843d\u3061': 'lnsgkgsn1/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u53f3\u9999\u843d\u3061': '1nsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u89d2\u843d\u3061': 'lnsgkgsnl/1r7/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u98db\u8eca\u843d\u3061': 'lnsgkgsnl/7b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u98db\u9999\u843d\u3061': 'lnsgkgsn1/7b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u4e8c\u679a\u843d\u3061': 'lnsgkgsnl/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u4e09\u679a\u843d\u3061': 'lnsgkgsn1/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u56db\u679a\u843d\u3061': '1nsgkgsn1/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u4e94\u679a\u843d\u3061': '2sgkgsn1/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u5de6\u4e94\u679a\u843d\u3061': '1nsgkgs2/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u516d\u679a\u843d\u3061': '2sgkgs2/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u516b\u679a\u843d\u3061': '4k4/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1',
        '\u305d\u306e\u4ed6': None
    }

    RESULT_RE = re.compile(r'\u3000*\u307e\u3067(\d+)\u624b\u3067((\u5148|\u4e0b|\u5f8c|\u4e0a)\u624b\u306e\u52dd\u3061|\u5343\u65e5\u624b|\u6301\u5c06\u68cb|\u4e2d\u65ad)')

    @staticmethod
    def parse_file(path):
        prefix, ext = os.path.splitext(path)
        enc = 'utf-8' if ext == '.kifu' else 'cp932'
        with codecs.open(path, 'r', enc) as f:
            return Parser.parse_str(f.read())

    @staticmethod
    def parse_pieces_in_hand(target):
        if target == '\u306a\u3057': # None in japanese
            return {}

        result = {}
        for item in target.split('\u3000'):
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
        line = line.replace('\u738b', '\u7389')
        line = line.replace('\u7adc', '\u9f8d')
        line = line.replace('\u6210\u9280', '\u5168')
        line = line.replace('\u6210\u6842', '\u572d')
        line = line.replace('\u6210\u9999', '\u674f')

        m = Parser.MOVE_RE.match(line)
        if m and m.group(1) not in [
                    '\u4e2d\u65ad',
                    '\u6295\u4e86',
                    '\u6301\u5c06\u68cb',
                    '\u5343\u65e5\u624b',
                    '\u8a70\u307f',
                    '\u5207\u308c\u8ca0\u3051',
                    '\u53cd\u5247\u304b\u52dd\u3061',
                    '\u53cd\u5247\u8ca0\u3051'
                ]:
            piece_type = shogi.PIECE_JAPANESE_SYMBOLS.index(m.group(5))
            if m.group(2) == '\u540c\u3000':
                # same position
                to_square = last_to_square
            else:
                to_field = 9 - shogi.NUMBER_JAPANESE_NUMBER_SYMBOLS.index(m.group(3))
                to_rank = shogi.NUMBER_JAPANESE_KANJI_SYMBOLS.index(m.group(4)) - 1
                to_square = to_rank * 9 + to_field
                last_to_square = to_square

            if m.group(6) == '\u6253':
                # piece drop
                return ('{0}*{1}'.format(shogi.PIECE_SYMBOLS[piece_type].upper(),
                    shogi.SQUARE_NAMES[to_square]), last_to_square)
            else:
                from_field = 9 - int(m.group(8))
                from_rank = int(m.group(9)) - 1
                from_square = from_rank * 9 + from_field

                promotion = (m.group(7) == '\u6210')
                return (shogi.SQUARE_NAMES[from_square] + shogi.SQUARE_NAMES[to_square] + ('+' if promotion else ''), last_to_square)
        return (None, last_to_square)

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
            elif '\uff1a' in line:
                (key, value) = line.split('\uff1a', 1)
                value = value.rstrip('\u3000')
                if key == '\u5148\u624b' or key == '\u4e0b\u624b': # sente or shitate
                    # Blacks's name
                    names[shogi.BLACK] = value
                elif key == '\u5f8c\u624b' or key == '\u4e0a\u624b': # gote or uwate
                    # White's name
                    names[shogi.WHITE] = value
                elif key == '\u5148\u624b\u306e\u6301\u99d2' or \
                        key == '\u4e0b\u624b\u306e\u6301\u99d2': # sente or shitate's pieces in hand
                    # First player's pieces in hand
                    pieces_in_hand[shogi.BLACK] == Parser.parse_pieces_in_hand(value)
                elif key == '\u5f8c\u624b\u306e\u6301\u99d2' or \
                        key == '\u4e0a\u624b\u306e\u6301\u99d2': # gote or uwate's pieces in hand
                    # Second player's pieces in hand
                    pieces_in_hand[shogi.WHITE] == Parser.parse_pieces_in_hand(value)
                elif key == '\u624b\u5408\u5272': # teai wari
                    sfen = Parser.HANDYCAP_SFENS[value]
                    if sfen is None:
                        raise ParserException('Cannot support handycap type "other"')
            elif line == '\u5f8c\u624b\u756a':
                # Current turn is white
                current_turn = shogi.WHITE
            else:
                (move, last_to_square) = Parser.parse_move_str(line, last_to_square)
                if move is not None:
                    moves.append(move)
                else:
                    m = Parser.RESULT_RE.match(line)
                    if m:
                        win_side_str = m.group(3)
                        if win_side_str == '\u5148' or win_side_str == '\u4e0b':
                            win = 'b'
                        elif win_side_str == '\u5f8c' or win_side_str == '\u4e0a':
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
