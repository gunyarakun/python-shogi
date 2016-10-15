# -*- coding: utf-8 -*-
#
# This file is part of the python-shogi library.
# Copyright (C) 2012-2014 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>
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

__author__ = 'Tasuku SUENAGA a.k.a. gunyarakun'
__email__ = 'tasuku-s-github@titech.ac'
__version__ = '1.0.1'

import collections
import re

COLORS = [BLACK, WHITE] = range(2)
PIECE_TYPES_WITH_NONE = [NONE,
           PAWN,      LANCE,      KNIGHT,      SILVER,
           GOLD,
         BISHOP,       ROOK,
           KING,
      PROM_PAWN, PROM_LANCE, PROM_KNIGHT, PROM_SILVER,
    PROM_BISHOP,  PROM_ROOK,
] = range(15)
PIECE_TYPES = [
           PAWN,      LANCE,      KNIGHT,      SILVER,
           GOLD,
         BISHOP,       ROOK,
           KING,
      PROM_PAWN, PROM_LANCE, PROM_KNIGHT, PROM_SILVER,
    PROM_BISHOP,  PROM_ROOK,
]
PIECE_TYPES_WITHOUT_KING = [
           PAWN,      LANCE,      KNIGHT,      SILVER,
           GOLD,
         BISHOP,       ROOK,
      PROM_PAWN, PROM_LANCE, PROM_KNIGHT, PROM_SILVER,
    PROM_BISHOP,  PROM_ROOK,
]

MAX_PIECES_IN_HAND = [0,
        18, 4, 4, 4,
        4,
        2, 2,
        0,
        0, 0, 0, 0,
        0, 0,
]

PIECE_PROMOTED = [
           None,
      PROM_PAWN, PROM_LANCE, PROM_KNIGHT, PROM_SILVER,
           None,
    PROM_BISHOP,  PROM_ROOK,
           None,
           None,       None,        None,        None,
           None,       None,
];

PIECE_SYMBOLS = ['',   'p',  'l',  'n',  's', 'g',  'b',  'r', 'k',
                      '+p', '+l', '+n', '+s',      '+b', '+r']
PIECE_JAPANESE_SYMBOLS = [
    '',
    '\u6b69', '\u9999', '\u6842', '\u9280', '\u91d1', '\u89d2', '\u98db',
    '\u7389', '\u3068', '\u674f', '\u572d', '\u5168', '\u99ac', '\u9f8d'
]
NUMBER_JAPANESE_NUMBER_SYMBOLS = [
    '\uff10', '\uff11', '\uff12', '\uff13', '\uff14',
    '\uff15', '\uff16', '\uff17', '\uff18', '\uff19'
]
NUMBER_JAPANESE_KANJI_SYMBOLS = [
    '\u96f6', '\u4e00', '\u4e8c', '\u4e09', '\u56db',
    '\u4e94', '\u516d', '\u4e03', '\u516b', '\u4e5d',
    '\u5341', '\u5341\u4e00', '\u5341\u4e8c', '\u5341\u4e09', '\u5341\u56db',
    '\u5341\u4e94', '\u5341\u516d', '\u5341\u4e03', '\u5341\u516b'
]

STARTING_SFEN = 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1'

SQUARES = [
    A9, A8, A7, A6, A5, A4, A3, A2, A1,
    B9, B8, B7, B6, B5, B4, B3, B2, B1,
    C9, C8, C7, C6, C5, C4, C3, C2, C1,
    D9, D8, D7, D6, D5, D4, D3, D2, D1,
    E9, E8, E7, E6, E5, E4, E3, E2, E1,
    F9, F8, F7, F6, F5, F4, F3, F2, F1,
    G9, G8, G7, G6, G5, G4, G3, G2, G1,
    H9, H8, H7, H6, H5, H4, H3, H2, H1,
    I9, I8, I7, I6, I5, I4, I3, I2, I1,
] = range(81)

SQUARES_L90 = [
    A1, B1, C1, D1, E1, F1, G1, H1, I1,
    A2, B2, C2, D2, E2, F2, G2, H2, I2,
    A3, B3, C3, D3, E3, F3, G3, H3, I3,
    A4, B4, C4, D4, E4, F4, G4, H4, I4,
    A5, B5, C5, D5, E5, F5, G5, H5, I5,
    A6, B6, C6, D6, E6, F6, G6, H6, I6,
    A7, B7, C7, D7, E7, F7, G7, H7, I7,
    A8, B8, C8, D8, E8, F8, G8, H8, I8,
    A9, B9, C9, D9, E9, F9, G9, H9, I9,
]

SQUARES_R45 = [
    A9, I8, H7, G6, F5, E4, D3, C2, B1,
    B9, A8, I7, H6, G5, F4, E3, D2, C1,
    C9, B8, A7, I6, H5, G4, F3, E2, D1,
    D9, C8, B7, A6, I5, H4, G3, F2, E1,
    E9, D8, C7, B6, A5, I4, H3, G2, F1,
    F9, E8, D2, C6, B5, A4, I3, H2, G1,
    G9, F8, E7, D6, C5, B4, A3, I2, H1,
    H9, G8, F7, E6, D5, C4, B3, A2, I1,
    I9, H8, G7, F6, E5, D4, C3, B2, A1,
]

SQUARES_L45 = [
    B9, C8, D7, E6, F5, G4, H3, I2, A1,
    C9, D8, E7, F6, G5, H4, I3, A2, B1,
    D9, E8, F7, G6, H5, I4, A3, B2, C1,
    E9, F8, G7, H6, I5, A4, B3, C2, D1,
    F9, G8, H7, I6, A5, B4, C3, D2, E1,
    G9, H8, I7, A6, B5, C4, D3, E2, F1,
    H9, I8, A7, B6, C5, D4, E3, F2, G1,
    I9, A8, B7, C6, D5, E4, F3, G2, H1,
    A9, B8, C7, D6, E5, F4, G3, H2, I1,
]

# NOTE: In chess we use "file - rank" notation like 'a1',
#       in shogi we use a number for file, an alphabet for rank
#       and opposite direction of files and ranks like '9i'.
#       We use chess style notation internally, but exports it with this table.
SQUARE_NAMES = [
    '9a', '8a', '7a', '6a', '5a', '4a', '3a', '2a', '1a',
    '9b', '8b', '7b', '6b', '5b', '4b', '3b', '2b', '1b',
    '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c', '1c',
    '9d', '8d', '7d', '6d', '5d', '4d', '3d', '2d', '1d',
    '9e', '8e', '7e', '6e', '5e', '4e', '3e', '2e', '1e',
    '9f', '8f', '7f', '6f', '5f', '4f', '3f', '2f', '1f',
    '9g', '8g', '7g', '6g', '5g', '4g', '3g', '2g', '1g',
    '9h', '8h', '7h', '6h', '5h', '4h', '3h', '2h', '1h',
    '9i', '8i', '7i', '6i', '5i', '4i', '3i', '2i', '1i',
]

def file_index(square):
    return square % 9

def rank_index(square):
    return square // 9

BB_VOID = 0b000000000000000000000000000000000000000000000000000000000000000000000000000000000
BB_ALL = 0b111111111111111111111111111111111111111111111111111111111111111111111111111111111

BB_SQUARES = [
    BB_A9, BB_A8, BB_A7, BB_A6, BB_A5, BB_A4, BB_A3, BB_A2, BB_A1,
    BB_B9, BB_B8, BB_B7, BB_B6, BB_B5, BB_B4, BB_B3, BB_B2, BB_B1,
    BB_C9, BB_C8, BB_C7, BB_C6, BB_C5, BB_C4, BB_C3, BB_C2, BB_C1,
    BB_D9, BB_D8, BB_D7, BB_D6, BB_D5, BB_D4, BB_D3, BB_D2, BB_D1,
    BB_E9, BB_E8, BB_E7, BB_E6, BB_E5, BB_E4, BB_E3, BB_E2, BB_E1,
    BB_F9, BB_F8, BB_F7, BB_F6, BB_F5, BB_F4, BB_F3, BB_F2, BB_F1,
    BB_G9, BB_G8, BB_G7, BB_G6, BB_G5, BB_G4, BB_G3, BB_G2, BB_G1,
    BB_H9, BB_H8, BB_H7, BB_H6, BB_H5, BB_H4, BB_H3, BB_H2, BB_H1,
    BB_I9, BB_I8, BB_I7, BB_I6, BB_I5, BB_I4, BB_I3, BB_I2, BB_I1,
] = [1 << i for i in SQUARES]

BB_SQUARES_L90 = [BB_SQUARES[SQUARES_L90[square]] for square in SQUARES]
BB_SQUARES_L45 = [BB_SQUARES[SQUARES_L45[square]] for square in SQUARES]
BB_SQUARES_R45 = [BB_SQUARES[SQUARES_R45[square]] for square in SQUARES]

BB_FILES = [
    BB_FILE_9,
    BB_FILE_8,
    BB_FILE_7,
    BB_FILE_6,
    BB_FILE_5,
    BB_FILE_4,
    BB_FILE_3,
    BB_FILE_2,
    BB_FILE_1,
] = [
    BB_A9 | BB_B9 | BB_C9 | BB_D9 | BB_E9 | BB_F9 | BB_G9 | BB_H9 | BB_I9,
    BB_A8 | BB_B8 | BB_C8 | BB_D8 | BB_E8 | BB_F8 | BB_G8 | BB_H8 | BB_I8,
    BB_A7 | BB_B7 | BB_C7 | BB_D7 | BB_E7 | BB_F7 | BB_G7 | BB_H7 | BB_I7,
    BB_A6 | BB_B6 | BB_C6 | BB_D6 | BB_E6 | BB_F6 | BB_G6 | BB_H6 | BB_I6,
    BB_A5 | BB_B5 | BB_C5 | BB_D5 | BB_E5 | BB_F5 | BB_G5 | BB_H5 | BB_I5,
    BB_A4 | BB_B4 | BB_C4 | BB_D4 | BB_E4 | BB_F4 | BB_G4 | BB_H4 | BB_I4,
    BB_A3 | BB_B3 | BB_C3 | BB_D3 | BB_E3 | BB_F3 | BB_G3 | BB_H3 | BB_I3,
    BB_A2 | BB_B2 | BB_C2 | BB_D2 | BB_E2 | BB_F2 | BB_G2 | BB_H2 | BB_I2,
    BB_A1 | BB_B1 | BB_C1 | BB_D1 | BB_E1 | BB_F1 | BB_G1 | BB_H1 | BB_I1,
]

BB_RANKS = [
    BB_RANK_A,
    BB_RANK_B,
    BB_RANK_C,
    BB_RANK_D,
    BB_RANK_E,
    BB_RANK_F,
    BB_RANK_G,
    BB_RANK_H,
    BB_RANK_I
] = [
    BB_A1 | BB_A2 | BB_A3 | BB_A4 | BB_A5 | BB_A6 | BB_A7 | BB_A8 | BB_A9,
    BB_B1 | BB_B2 | BB_B3 | BB_B4 | BB_B5 | BB_B6 | BB_B7 | BB_B8 | BB_B9,
    BB_C1 | BB_C2 | BB_C3 | BB_C4 | BB_C5 | BB_C6 | BB_C7 | BB_C8 | BB_C9,
    BB_D1 | BB_D2 | BB_D3 | BB_D4 | BB_D5 | BB_D6 | BB_D7 | BB_D8 | BB_D9,
    BB_E1 | BB_E2 | BB_E3 | BB_E4 | BB_E5 | BB_E6 | BB_E7 | BB_E8 | BB_E9,
    BB_F1 | BB_F2 | BB_F3 | BB_F4 | BB_F5 | BB_F6 | BB_F7 | BB_F8 | BB_F9,
    BB_G1 | BB_G2 | BB_G3 | BB_G4 | BB_G5 | BB_G6 | BB_G7 | BB_G8 | BB_G9,
    BB_H1 | BB_H2 | BB_H3 | BB_H4 | BB_H5 | BB_H6 | BB_H7 | BB_H8 | BB_H9,
    BB_I1 | BB_I2 | BB_I3 | BB_I4 | BB_I5 | BB_I6 | BB_I7 | BB_I8 | BB_I9,
]


def shift_down(b):
    return (b << 9) & BB_ALL


def shift_2_down(b):
    return (b << 18) & BB_ALL


def shift_up(b):
    return b >> 9


def shift_2_up(b):
    return b >> 18


def shift_right(b):
    return (b << 1) & ~BB_FILE_9


def shift_2_right(b):
    return (b << 2) & ~BB_FILE_9 & ~BB_FILE_8


def shift_left(b):
    return (b >> 1) & ~BB_FILE_1


def shift_2_left(b):
    return (b >> 2) & ~BB_FILE_1 & ~BB_FILE_2


def shift_up_left(b):
    return (b >> 10) & ~BB_FILE_1


def shift_up_right(b):
    return (b >> 8) & ~BB_FILE_9


def shift_down_left(b):
    return (b << 8) & ~BB_FILE_1


def shift_down_right(b):
    return (b << 10) & ~BB_FILE_9

BB_PAWN_ATTACKS = [
    [shift_up(s) for s in BB_SQUARES],
    [shift_down(s) for s in BB_SQUARES],
]
BB_KNIGHT_ATTACKS = [[], []]
BB_SILVER_ATTACKS = [[], []]
BB_GOLD_ATTACKS = [[], []]
BB_KING_ATTACKS = []

for bb_square in BB_SQUARES:
    mask = BB_VOID
    mask |= shift_left(shift_2_up(bb_square))
    mask |= shift_right(shift_2_up(bb_square))

    BB_KNIGHT_ATTACKS[BLACK].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_left(shift_2_down(bb_square))
    mask |= shift_right(shift_2_down(bb_square))

    BB_KNIGHT_ATTACKS[WHITE].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_up_left(bb_square)
    mask |= shift_up(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_down_left(bb_square)
    mask |= shift_down_right(bb_square)

    BB_SILVER_ATTACKS[BLACK].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_down_left(bb_square)
    mask |= shift_down(bb_square)
    mask |= shift_down_right(bb_square)
    mask |= shift_up_left(bb_square)
    mask |= shift_up_right(bb_square)

    BB_SILVER_ATTACKS[WHITE].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_up_left(bb_square)
    mask |= shift_up(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_down(bb_square)

    BB_GOLD_ATTACKS[BLACK].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_down_left(bb_square)
    mask |= shift_down(bb_square)
    mask |= shift_down_right(bb_square)
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_up(bb_square)

    BB_GOLD_ATTACKS[WHITE].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_up(bb_square)
    mask |= shift_down(bb_square)
    mask |= shift_up_left(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_down_left(bb_square)
    mask |= shift_down_right(bb_square)
    BB_KING_ATTACKS.append(mask & BB_ALL)

# 128 means 2 ^ (9 - 1 - 1), patterns of emptiness of one row without each ends
BB_RANK_ATTACKS = [[BB_VOID for i in range(128)] for k in SQUARES]
BB_FILE_ATTACKS = [[BB_VOID for i in range(128)] for k in SQUARES]
BB_LANCE_ATTACKS = [
    [[BB_VOID for i in range(128)] for k in SQUARES],
    [[BB_VOID for i in range(128)] for k in SQUARES],
]

for square in SQUARES:
    for bitrow in range(0, 128):
        f = file_index(square) + 1
        q = square + 1
        while f < 9:
            BB_RANK_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            if (1 << f) & (bitrow << 1):
                break
            q += 1
            f += 1

        f = file_index(square) - 1
        q = square - 1
        while f >= 0:
            BB_RANK_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            if (1 << f) & (bitrow << 1):
                break
            q -= 1
            f -= 1

        r = rank_index(square) + 1
        q = square + 9
        while r < 9:
            BB_FILE_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            BB_LANCE_ATTACKS[WHITE][square][bitrow] |= BB_SQUARES[q]
            if (1 << (8 - r)) & (bitrow << 1):
                break
            q += 9
            r += 1

        r = rank_index(square) - 1
        q = square - 9
        while r >= 0:
            BB_FILE_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            BB_LANCE_ATTACKS[BLACK][square][bitrow] |= BB_SQUARES[q]
            if (1 << (8 - r)) & (bitrow << 1):
                break
            q -= 9
            r -= 1

BB_SHIFT_R45 = [
     1, 73, 65, 57, 49, 41, 33, 25, 17,
    10,  1, 73, 65, 57, 49, 41, 33, 25,
    19, 10,  1, 73, 65, 57, 49, 41, 33,
    28, 19, 10,  1, 73, 65, 57, 49, 41,
    36, 28, 19, 10,  1, 73, 65, 57, 49,
    45, 36, 28, 19, 10,  1, 73, 65, 57,
    54, 45, 36, 28, 19, 10,  1, 73, 65,
    63, 54, 45, 36, 28, 19, 10,  1, 73,
    72, 63, 54, 45, 36, 28, 19, 10,  1
]

BB_SHIFT_L45 = [
    10, 19, 28, 36, 45, 54, 63, 72,  1,
    19, 28, 36, 45, 54, 63, 72,  1, 11,
    28, 36, 45, 54, 63, 72,  1, 11, 21,
    36, 45, 54, 63, 72,  1, 11, 21, 31,
    45, 54, 63, 72,  1, 11, 21, 31, 41,
    54, 63, 72,  1, 11, 21, 31, 41, 51,
    63, 72,  1, 11, 21, 31, 41, 51, 61,
    72,  1, 11, 21, 31, 41, 51, 61, 71,
     1, 11, 21, 31, 41, 51, 61, 71, 81
]

BB_L45_ATTACKS = [[BB_VOID for i in range(128)] for k in SQUARES]
BB_R45_ATTACKS = [[BB_VOID for i in range(128)] for k in SQUARES]

for s in SQUARES:
    for b in range(0, 128):
        mask = BB_VOID

        q = s
        while file_index(q) > 0 and rank_index(q) < 8:
            q += 8
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_L45[q] >> BB_SHIFT_L45[s]):
                break

        q = s
        while file_index(q) < 8 and rank_index(q) > 0:
            q -= 8
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_L45[q] >> BB_SHIFT_L45[s]):
                break

        BB_L45_ATTACKS[s][b] = mask

        mask = BB_VOID

        q = s
        while file_index(q) < 8 and rank_index(q) < 8:
            q += 10
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_R45[q] >> BB_SHIFT_R45[s]):
                break

        q = s
        while file_index(q) > 0 and rank_index(q) > 0:
            q -= 10
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_R45[q] >> BB_SHIFT_R45[s]):
                break

        BB_R45_ATTACKS[s][b] = mask

try:
    from gmpy2 import popcount as pop_count
    from gmpy2 import bit_scan1 as bit_scan
except ImportError:
    try:
        from gmpy import popcount as pop_count
        from gmpy import scan1 as bit_scan
    except ImportError:
        def pop_count(b):
            return bin(b).count('1')

        def bit_scan(b, n=0):
            string = bin(b)
            l = len(string)
            r = string.rfind('1', 0, l - n)
            if r == -1:
                return -1
            else:
                return l - r - 1

def can_promote(square, piece_type, color):
    if piece_type not in [PAWN, LANCE, KNIGHT, SILVER, BISHOP, ROOK]:
        return False
    elif color == BLACK:
        return rank_index(square) <= 2
    else:
        return rank_index(square) >= 6

def can_move_without_promotion(to_square, piece_type, color):
    if color == BLACK:
        return ((piece_type != PAWN and piece_type != LANCE and piece_type != KNIGHT) or
                (piece_type == PAWN and rank_index(to_square) > 0) or
                (piece_type == LANCE and rank_index(to_square) > 0) or
                (piece_type == KNIGHT and rank_index(to_square) > 1) )
    else:
        return ((piece_type != PAWN and piece_type != LANCE and piece_type != KNIGHT) or
                (piece_type == PAWN and rank_index(to_square) < 8) or
                (piece_type == LANCE and rank_index(to_square) < 8) or
                (piece_type == KNIGHT and rank_index(to_square) < 7) )

class Piece(object):
    def __init__(self, piece_type, color):
        if piece_type is None:
            raise ValueError('Piece type must be set')
        if color is None:
            raise ValueError('Color must be set')
        self.piece_type = piece_type
        self.color = color

    def symbol(self):
        '''
        Gets the symbol `p`, `l`, `n`, etc.
        '''
        if self.color == BLACK:
            return PIECE_SYMBOLS[self.piece_type].upper()
        else:
            return PIECE_SYMBOLS[self.piece_type]

    def japanese_symbol(self):
        # no direction
        return PIECE_JAPANESE_SYMBOLS[self.piece_type]

    def japanese_symbol_with_direction(self):
        if self.color == BLACK:
            prefix = ' '
        else:
            prefix = 'v'
        return prefix + PIECE_JAPANESE_SYMBOLS[self.piece_type]

    def is_promoted(self):
        return self.piece_type >= PROM_PAWN

    def __hash__(self):
        return self.piece_type * (self.color + 1)

    def __repr__(self):
        return "Piece.from_symbol('{0}')".format(self.symbol())

    def __str__(self):
        return self.symbol()

    def __eq__(self, other):
        try:
            return self.piece_type == other.piece_type and self.color == other.color
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_symbol(cls, symbol):
        '''
        Creates a piece instance from a piece symbol.
        Raises `ValueError` if the symbol is invalid.
        '''
        if symbol.lower() == symbol:
            return cls(PIECE_SYMBOLS.index(symbol), WHITE)
        else:
            return cls(PIECE_SYMBOLS.index(symbol.lower()), BLACK)

class Move(object):
    '''
    Represents a move from a square to a square and possibly the promotion piece
    type.
    Null moves are supported.
    '''

    def __init__(self, from_square, to_square, promotion=False, drop_piece_type=None):
        # if from_square is None, it's a drop and
        self.from_square = from_square
        self.to_square = to_square
        if from_square is None and to_square is not None:
            if drop_piece_type is None:
                raise ValueError('Drop piece type must be set.')
            if promotion:
                raise ValueError('Cannot set promoted piece.')
            self.promotion = False
            self.drop_piece_type = drop_piece_type
        else:
            self.promotion = promotion
            if drop_piece_type:
                raise ValueError('Drop piece type must not be set.')
            self.drop_piece_type = None

    def usi(self):
        '''
        Gets an USI string for the move.
        For example a move from 7A to 8A would be `7a8a` or `7a8a+` if it is
        a promotion.
        '''
        if self:
            if self.drop_piece_type:
                return '{0}*{1}'.format(PIECE_SYMBOLS[self.drop_piece_type].upper(), SQUARE_NAMES[self.to_square])
            else:
                return SQUARE_NAMES[self.from_square] + SQUARE_NAMES[self.to_square] + \
                       ('+' if self.promotion else '')
        else:
            return '0000'

    def __bool__(self):
        return self.to_square is not None

    def __nonzero__(self):
        return self.to_square is not None

    def __eq__(self, other):
        try:
            return self.from_square == other.from_square and self.to_square == other.to_square and \
                   self.promotion == other.promotion and self.drop_piece_type == other.drop_piece_type
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Move.from_usi('{0}')".format(self.usi())

    def __str__(self):
        return self.usi()

    def __hash__(self):
        # 7 bit is enought to represent 81 patterns
        return self.to_square | (self.from_square or (81 + self.drop_piece_type)) << 7 | self.promotion << 14

    @classmethod
    def from_usi(cls, usi):
        '''
        Parses an USI string.
        Raises `ValueError` if the USI string is invalid.
        '''
        if usi == '0000':
            return cls.null()
        elif len(usi) == 4:
            if usi[1] == '*':
                piece = Piece.from_symbol(usi[0])
                return cls(None, SQUARE_NAMES.index(usi[2:4]), False, piece.piece_type)
            else:
                return cls(SQUARE_NAMES.index(usi[0:2]), SQUARE_NAMES.index(usi[2:4]))
        elif len(usi) == 5 and usi[4] == '+':
            return cls(SQUARE_NAMES.index(usi[0:2]), SQUARE_NAMES.index(usi[2:4]), True)
        else:
            raise ValueError('expected usi string to be of length 4 or 5')

    @classmethod
    def null(cls):
        '''
        Gets a null move.
        A null move just passes the turn to the other side (and possibly
        forfeits en-passant capturing). Null moves evaluate to `False` in
        boolean contexts.
        >>> bool(shogi.Move.null())
        False
        '''
        return cls(0, 0, NONE)


class Occupied(object):
    def __init__(self, occupied_by_black, occupied_by_white):
        self.by_color = [occupied_by_black, occupied_by_white]
        self.bits = occupied_by_black | occupied_by_white
        self.l45 = BB_VOID
        self.r45 = BB_VOID
        self.l90 = BB_VOID
        self.update_rotated()

    def update_rotated(self):
        for i in SQUARES:
            if BB_SQUARES[i] & self.bits:
                self.l90 |= BB_SQUARES_L90[i]
                self.r45 |= BB_SQUARES_R45[i]
                self.l45 |= BB_SQUARES_L45[i]

    def __getitem__(self, key):
        if key in COLORS:
            return self.by_color[key]
        raise KeyError('Occupied must be looked up with shogi.BLACK or shogi.WHITE')

    def ixor(self, mask, color, square):
        self.bits ^= mask
        self.by_color[color] ^= mask
        self.l90 ^= BB_SQUARES[SQUARES_L90[square]]
        self.r45 ^= BB_SQUARES[SQUARES_R45[square]]
        self.l45 ^= BB_SQUARES[SQUARES_L45[square]]

    def non_occupied(self):
        return ~self.bits & BB_ALL

    def __eq__(self, occupied):
        return not self.__ne__(occupied)

    def __ne__(self, occupied):
        if self.by_color[BLACK] != occupied.by_color[BLACK]:
            return True
        if self.by_color[WHITE] != occupied.by_color[WHITE]:
            return True
        return False

    def __repr__(self):
        return 'Occupied({0})'.format(repr(self.by_color))

class Board(object):
    '''
    A bitboard and additional information representing a position.
    Provides move generation, validation, parsing, attack generation,
    game end detection, move counters and the capability to make and unmake
    moves.
    The bitboard is initialized to the starting position, unless otherwise
    specified in the optional `sfen` argument.
    '''

    def __init__(self, sfen=None):
        self.pseudo_legal_moves = PseudoLegalMoveGenerator(self)
        self.legal_moves = LegalMoveGenerator(self)

        if sfen is None:
            self.reset()
        else:
            self.set_sfen(sfen)

    def reset(self):
        '''Restores the starting position.'''
        self.piece_bb = [
                BB_VOID,                       # NONE
                BB_RANK_C | BB_RANK_G,         # PAWN
                BB_A1 | BB_I1 | BB_A9 | BB_I9, # LANCE
                BB_A2 | BB_A8 | BB_I2 | BB_I8, # KNIGHT
                BB_A3 | BB_A7 | BB_I3 | BB_I7, # SILVER
                BB_A4 | BB_A6 | BB_I4 | BB_I6, # GOLD
                BB_B2 | BB_H8,                 # BISHOP
                BB_B8 | BB_H2,                 # ROOK
                BB_A5 | BB_I5,                 # KING
                BB_VOID,                       # PROM_PAWN
                BB_VOID,                       # PROM_LANCE
                BB_VOID,                       # PROM_KNIGHT
                BB_VOID,                       # PROM_SILVER
                BB_VOID,                       # PROM_BISHOP
                BB_VOID,                       # PROM_ROOK
        ]

        self.pieces_in_hand = [collections.Counter(), collections.Counter()]

        self.occupied = Occupied(BB_RANK_G | BB_H2 | BB_H8 | BB_RANK_I, BB_RANK_A | BB_B2 | BB_B8 | BB_RANK_C)

        self.king_squares = [I5, A5]
        self.pieces = [NONE for i in SQUARES]

        for i in SQUARES:
            mask = BB_SQUARES[i]
            for piece_type in PIECE_TYPES:
                if mask & self.piece_bb[piece_type]:
                    self.pieces[i] = piece_type

        self.turn = BLACK
        self.move_number = 1
        self.captured_piece_stack = collections.deque()
        self.move_stack = collections.deque()
        self.incremental_zobrist_hash = self.board_zobrist_hash(DEFAULT_RANDOM_ARRAY)
        self.transpositions = collections.Counter((self.zobrist_hash(), ))

    def clear(self):
        self.piece_bb = [
                BB_VOID,                       # NONE
                BB_VOID,                       # PAWN
                BB_VOID,                       # LANCE
                BB_VOID,                       # KNIGHT
                BB_VOID,                       # SILVER
                BB_VOID,                       # GOLD
                BB_VOID,                       # BISHOP
                BB_VOID,                       # ROOK
                BB_VOID,                       # KING
                BB_VOID,                       # PROM_PAWN
                BB_VOID,                       # PROM_LANCE
                BB_VOID,                       # PROM_KNIGHT
                BB_VOID,                       # PROM_SILVER
                BB_VOID,                       # PROM_BISHOP
                BB_VOID,                       # PROM_ROOK
        ]

        self.pieces_in_hand = [collections.Counter(), collections.Counter()]

        self.occupied = Occupied(BB_VOID, BB_VOID)

        self.king_squares = [None, None]
        self.pieces = [NONE for i in SQUARES]

        self.turn = BLACK
        self.move_number = 1
        self.captured_piece_stack = collections.deque()
        self.move_stack = collections.deque()
        self.incremental_zobrist_hash = self.board_zobrist_hash(DEFAULT_RANDOM_ARRAY)
        self.transpositions = collections.Counter((self.zobrist_hash(), ))

    def piece_at(self, square):
        '''Gets the piece at the given square.'''
        mask = BB_SQUARES[square]
        color = int(bool(self.occupied[WHITE] & mask))

        piece_type = self.piece_type_at(square)
        if piece_type:
            return Piece(piece_type, color)

    def piece_type_at(self, square):
        '''Gets the piece type at the given square.'''
        return self.pieces[square]

    def add_piece_into_hand(self, piece_type, color, count=1):
        p = self.pieces_in_hand[color]
        if piece_type >= PROM_PAWN:
            piece_type = PIECE_PROMOTED.index(piece_type)
        p[piece_type] += count

    def remove_piece_from_hand(self, piece_type, color):
        p = self.pieces_in_hand[color]
        if piece_type >= PROM_PAWN:
            piece_type = PIECE_PROMOTED.index(piece_type)
        p[piece_type] -= 1
        if p[piece_type] == 0:
            del p[piece_type]
        elif p[piece_type] < 0:
            raise ValueError('The piece is not in hand: {0}'.format(Piece(piece_type, self.turn)))

    def has_piece_in_hand(self, piece_type, color):
        if piece_type >= PROM_PAWN:
            piece_type = PIECE_PROMOTED.index(piece_type)
        return piece_type in self.pieces_in_hand[color]

    def remove_piece_at(self, square, into_hand=False):
        '''Removes a piece from the given square if present.'''
        piece_type = self.piece_type_at(square)

        if piece_type == NONE:
            return

        if into_hand:
            self.add_piece_into_hand(piece_type, self.turn)

        mask = BB_SQUARES[square]

        self.piece_bb[piece_type] ^= mask

        color = int(bool(self.occupied[WHITE] & mask))

        self.pieces[square] = NONE
        self.occupied.ixor(mask, color, square)

        # Update incremental zobrist hash.
        if color == BLACK:
            piece_index = (piece_type - 1) * 2
        else:
            piece_index = (piece_type - 1) * 2 + 1
        self.incremental_zobrist_hash ^= DEFAULT_RANDOM_ARRAY[81 * piece_index + 9 * rank_index(square) + file_index(square)]

    def set_piece_at(self, square, piece, from_hand=False, into_hand=False):
        '''Sets a piece at the given square. An existing piece is replaced.'''
        if from_hand:
            self.remove_piece_from_hand(piece.piece_type, self.turn)

        self.remove_piece_at(square, into_hand)

        self.pieces[square] = piece.piece_type

        mask = BB_SQUARES[square]

        piece_type = piece.piece_type

        self.piece_bb[piece_type] |= mask

        if piece_type == KING:
            self.king_squares[piece.color] = square

        self.occupied.ixor(mask, piece.color, square)

        # Update incremental zorbist hash.
        if piece.color == BLACK:
            piece_index = (piece.piece_type - 1) * 2
        else:
            piece_index = (piece.piece_type - 1) * 2 + 1
        self.incremental_zobrist_hash ^= DEFAULT_RANDOM_ARRAY[81 * piece_index + 9 * rank_index(square) + file_index(square)]

    def generate_pseudo_legal_moves(self, pawns=True, lances=True, knights=True, silvers=True, golds=True,
            bishops=True, rooks=True,
            kings=True,
            prom_pawns=True, prom_lances=True, prom_knights=True, prom_silvers=True, prom_bishops=True, prom_rooks=True,
            pawns_drop=True, lances_drop=True, knights_drop=True, silvers_drop=True, golds_drop=True,
            bishops_drop=True, rooks_drop=True):

        move_flags = [False,
                      pawns, lances, knights, silvers,
                      golds, bishops, rooks,
                      kings,
                      prom_pawns, prom_lances, prom_knights, prom_silvers,
                      prom_bishops, prom_rooks]
        drop_flags = [False,
                      pawns_drop, lances_drop, knights_drop, silvers_drop,
                      golds_drop, bishops_drop, rooks_drop]

        for piece_type in PIECE_TYPES:
            # piece move
            if move_flags[piece_type]:
                movers = self.piece_bb[piece_type] & self.occupied[self.turn]
                from_square = bit_scan(movers)

                while from_square != -1 and from_square is not None:
                    moves = Board.attacks_from(piece_type, from_square, self.occupied, self.turn) & ~self.occupied[self.turn]
                    to_square = bit_scan(moves)
                    while to_square != - 1 and to_square is not None:
                        if can_move_without_promotion(to_square, piece_type, self.turn):
                            yield Move(from_square, to_square)
                        if can_promote(from_square, piece_type, self.turn) or can_promote(to_square, piece_type, self.turn):
                            yield Move(from_square, to_square, True)
                        to_square = bit_scan(moves, to_square + 1)
                    from_square = bit_scan(movers, from_square + 1)

        # Drop pieces in hand.
        moves = self.occupied.non_occupied()
        to_square = bit_scan(moves)

        while to_square != -1 and to_square is not None:
            for piece_type in range(PAWN, KING):
                # Check having the piece in hand, can move after place
                # and double pawn
                if drop_flags[piece_type] and self.has_piece_in_hand(piece_type, self.turn) and \
                        can_move_without_promotion(to_square, piece_type, self.turn) and \
                        not self.is_double_pawn(to_square, piece_type):
                    yield Move(None, to_square, False, piece_type)

            to_square = bit_scan(moves, to_square + 1)

    def is_attacked_by(self, color, square, piece_types=PIECE_TYPES):
        if square is None:
            return False

        for piece_type in piece_types:
            is_attacked = Board.attacks_from(piece_type, square, self.occupied, color ^ 1) & self.piece_bb[piece_type] & self.occupied[color]
            if is_attacked:
                return True

        return False

    def attacker_mask(self, color, square):
        attackers = BB_VOID
        for piece_type in PIECE_TYPES:
            attackers |= Board.attacks_from(piece_type, square, self.occupied, color ^ 1) & self.piece_bb[piece_type]
        return attackers & self.occupied[color]

    def attackers(self, color, square):
        return SquareSet(self.attacker_mask(color, square))

    def is_check(self):
        return self.is_attacked_by(self.turn ^ 1, self.king_squares[self.turn])

    @staticmethod
    def attacks_from(piece_type, square, occupied, move_color):
        if piece_type == NONE:
            return BB_VOID
        if piece_type == PAWN:
            return BB_PAWN_ATTACKS[move_color][square]
        elif piece_type == LANCE:
            return BB_LANCE_ATTACKS[move_color][square][(occupied.l90 >> (((square % 9) * 9) + 1)) & 127]
        elif piece_type == KNIGHT:
            return BB_KNIGHT_ATTACKS[move_color][square]
        elif piece_type == SILVER:
            return BB_SILVER_ATTACKS[move_color][square]
        elif piece_type in [GOLD, PROM_PAWN, PROM_LANCE, PROM_KNIGHT, PROM_SILVER]:
            return BB_GOLD_ATTACKS[move_color][square]
        elif piece_type == BISHOP:
            return (BB_R45_ATTACKS[square][(occupied.r45 >> BB_SHIFT_R45[square]) & 127] |
                    BB_L45_ATTACKS[square][(occupied.l45 >> BB_SHIFT_L45[square]) & 127])
        elif piece_type == ROOK:
            return (BB_RANK_ATTACKS[square][(occupied.bits >> (((square // 9) * 9) + 1)) & 127] |
                    BB_FILE_ATTACKS[square][(occupied.l90 >> (((square % 9) * 9) + 1)) & 127])
        elif piece_type == KING:
            return BB_KING_ATTACKS[square]
        elif piece_type == PROM_BISHOP:
            return (BB_KING_ATTACKS[square] |
                    BB_R45_ATTACKS[square][(occupied.r45 >> BB_SHIFT_R45[square]) & 127] |
                    BB_L45_ATTACKS[square][(occupied.l45 >> BB_SHIFT_L45[square]) & 127])
        elif piece_type == PROM_ROOK:
            return (BB_KING_ATTACKS[square] |
                    BB_RANK_ATTACKS[square][(occupied.bits >> (((square // 9) * 9) + 1)) & 127] |
                    BB_FILE_ATTACKS[square][(occupied.l90 >> (((square % 9) * 9) + 1)) & 127])

    def is_suicide_or_check_by_dropping_pawn(self, move):
        '''
        Checks if the given move would move would leave the king in check or
        put it into check.
        '''

        self.push(move)
        is_suicide = self.was_suicide()
        is_check_by_dropping_pawn = self.was_check_by_dropping_pawn(move)
        self.pop()
        return is_suicide or is_check_by_dropping_pawn

    def was_suicide(self):
        '''
        Checks if the king of the other side is attacked. Such a position is not
        valid and could only be reached by an illegal move.
        '''
        return self.is_attacked_by(self.turn, self.king_squares[self.turn ^ 1])

    def was_check_by_dropping_pawn(self, move):
        # NOTE: We ignore the case "Saigo no shinpan" (by Koji Nuita, 1997)
        # We don't use is_checkmate() because it's slow due to generating all leagl moves
        # And we don't consider suicide of a king.

        pawn_square = move.to_square

        # Pawn is dropped?
        if move.drop_piece_type != PAWN:
            return False

        king_square = self.king_squares[self.turn]

        # Does king exist?
        if king_square is None:
            return False

        # Pawn can capture a king next move?
        moves = BB_PAWN_ATTACKS[self.turn ^ 1][pawn_square] & ~self.occupied[self.turn ^ 1]
        if not moves & BB_SQUARES[king_square]:
            return False

        # Can king escape? (including capturing a dropped pawn)
        moves = Board.attacks_from(KING, king_square, self.occupied, self.turn) & ~self.occupied[self.turn]
        square = bit_scan(moves)
        while square != -1 and square is not None:
            if not self.is_attacked_by(self.turn ^ 1, square):
                return False
            square = bit_scan(moves, square + 1)

        # Pieces besides king can capture the pawn?
        if self.is_attacked_by(self.turn, pawn_square, PIECE_TYPES_WITHOUT_KING):
            return False

        return True

    def generate_legal_moves(self, pawns=True, lances=True, knights=True, silvers=True, golds=True, bishops=True,
            rooks=True, king=True,
            pawns_drop=True, lances_drop=True, knights_drop=True, silvers_drop=True, golds_drop=True,
            bishops_drop=True, rooks_drop=True):
        return (move for move in self.generate_pseudo_legal_moves(
                pawns, lances, knights, silvers, golds, bishops, rooks, king,
                pawns_drop, lances_drop, knights_drop, silvers_drop, golds_drop, bishops_drop, rooks_drop
            ) if not self.is_suicide_or_check_by_dropping_pawn(move))

    def is_pseudo_legal(self, move):
        # Null moves are not pseudo legal.
        if not move:
            return False

        # Get square masks of the move destination.
        to_mask = BB_SQUARES[move.to_square]

        # Destination square can not be occupied by self.
        if self.occupied[self.turn] & to_mask:
            return False

        if move.from_square:
            from_mask = BB_SQUARES[move.from_square]
            # Source square must not be vacant.
            piece = self.piece_type_at(move.from_square)
            if not piece:
                return False
            # Check turn.
            if not self.occupied[self.turn] & from_mask:
                return False

            # Promotion check
            if move.promotion:
                if piece == GOLD or piece == KING or piece >= PROM_PAWN:
                    return False
                if self.turn == BLACK and rank_index(move.to_square) > 2:
                    return False
                elif self.turn == WHITE and rank_index(move.to_square) < 6:
                    return False

            # Can move without promotion
            if not move.promotion and not can_move_without_promotion(move.to_square, piece, self.turn):
                return False

            # Handle moves by piece type.
            return bool(Board.attacks_from(piece, move.from_square, self.occupied, self.turn ^ 1) & to_mask)
        elif move.drop_piece_type:
            # Cannot set promoted piece
            if move.promotion:
                return False

            # Have a piece in hand
            if not self.has_piece_in_hand(move.drop_piece_type, self.turn):
                return False

            # Can move without promotion
            if not can_move_without_promotion(move.to_square, move.drop_piece_type, self.turn):
                return False

            # Not double pawn
            if self.is_double_pawn(move.to_square, move.drop_piece_type):
                return False

            return True
        else:
            # Drop piece or move piece
            return False

    def is_legal(self, move):
        return self.is_pseudo_legal(move) and not self.is_suicide_or_check_by_dropping_pawn(move)

    def is_game_over(self):
        '''
        Checks if the game is over due to checkmate, stalemate or
        fourfold repetition.
        '''

        # Stalemate or checkmate.
        try:
            next(self.generate_legal_moves().__iter__())
        except StopIteration:
            return True

        # Fourfold repetition.
        if self.is_fourfold_repetition():
            return True

        return False

    def is_checkmate(self):
        '''Checks if the current position is a checkmate.'''
        if not self.is_check():
            return False

        try:
            next(self.generate_legal_moves().__iter__())
            return False
        except StopIteration:
            return True

    def is_stalemate(self):
        '''Checks if the current position is a stalemate.'''
        if self.is_check():
            return False

        try:
            next(self.generate_legal_moves().__iter__())
            return False
        except StopIteration:
            return True

    def is_fourfold_repetition(self):
        '''
        a game is ended if a position occurs for the fourth time
        on consecutive alternating moves.
        '''
        zobrist_hash = self.zobrist_hash()

        # A minimum amount of moves must have been played and the position
        # in question must have appeared at least four times.
        if self.transpositions[zobrist_hash] < 4:
            return False

        return True

    def is_double_pawn(self, to_square, piece_type):
        if piece_type != PAWN:
            return False
        return self.piece_bb[PAWN] & BB_FILES[file_index(to_square)]

    def push(self, move):
        '''
        Updates the position with the given move and puts it onto a stack.
        Null moves just increment the move counters, switch turns and forfeit
        en passant capturing.
        No validation is performed. For performance moves are assumed to be at
        least pseudo legal. Otherwise there is no guarantee that the previous
        board state can be restored. To check it yourself you can use:
        >>> move in board.pseudo_legal_moves
        True
        '''
        # Increment move number.
        self.move_number += 1

        # Remember game state.
        captured_piece = self.piece_type_at(move.to_square) if move else NONE
        self.captured_piece_stack.append(captured_piece)
        self.move_stack.append(move)

        # On a null move simply swap turns.
        if not move:
            self.turn ^= 1
            return

        if move.drop_piece_type:
            # Drops.
            piece_type = move.drop_piece_type
            from_hand = True
        else:
            # Promotion.
            piece_type = self.piece_type_at(move.from_square)
            from_hand = False

            if move.promotion:
                piece_type = PIECE_PROMOTED[piece_type]

            # Remove piece from target square.
            self.remove_piece_at(move.from_square, False)

        # Put piece on target square.
        self.set_piece_at(move.to_square, Piece(piece_type, self.turn), from_hand, True)

        # Swap turn.
        self.turn ^= 1

        # Update transposition table.
        self.transpositions.update((self.zobrist_hash(), ))

    def pop(self):
        '''
        Restores the previous position and returns the last move from the stack.
        '''
        move = self.move_stack.pop()

        # Update transposition table.
        self.transpositions.subtract((self.zobrist_hash(), ))

        # Decrement move number.
        self.move_number -= 1

        # Restore state.
        captured_piece_type = self.captured_piece_stack.pop()
        captured_piece_color = self.turn

        # On a null move simply swap the turn.
        if not move:
            self.turn ^= 1
            return move

        # Restore the source square.
        piece_type = self.piece_type_at(move.to_square)
        if move.promotion:
            piece_type = PIECE_PROMOTED.index(piece_type)

        if move.from_square is None:
            self.add_piece_into_hand(piece_type, self.turn ^ 1)
        else:
            self.set_piece_at(move.from_square, Piece(piece_type, self.turn ^ 1))

        # Restore target square.
        if captured_piece_type:
            self.remove_piece_from_hand(captured_piece_type, captured_piece_color ^ 1)
            self.set_piece_at(move.to_square, Piece(captured_piece_type, captured_piece_color))
        else:
            self.remove_piece_at(move.to_square)

        # Swap turn.
        self.turn ^= 1

        return move

    def peek(self):
        '''Gets the last move from the move stack.'''
        return self.move_stack[-1]

    def sfen(self):
        '''
        Gets an SFEN representation of the current position.
        '''
        sfen = []
        empty = 0

        # Position part.
        for square in SQUARES:
            piece = self.piece_at(square)

            if not piece:
                empty += 1
            else:
                if empty:
                    sfen.append(str(empty))
                    empty = 0
                sfen.append(piece.symbol())

            if BB_SQUARES[square] & BB_FILE_1:
                if empty:
                    sfen.append(str(empty))
                    empty = 0

                if square != I1:
                    sfen.append('/')

        sfen.append(' ')

        # Side to move.
        if self.turn == WHITE:
            sfen.append('w')
        else:
            sfen.append('b')

        sfen.append(' ')

        # Pieces in hand
        pih_len = 0
        for color in COLORS:
            p = self.pieces_in_hand[color]
            pih_len += len(p)
            for piece_type in p.keys():
                if p[piece_type] >= 1:
                    if p[piece_type] > 1:
                        sfen.append(str(p[piece_type]))
                    piece = Piece(piece_type, color)
                    sfen.append(piece.symbol())
        if pih_len == 0:
            sfen.append('-')

        sfen.append(' ')

        # Move count
        sfen.append(str(self.move_number))

        return ''.join(sfen)

    def set_sfen(self, sfen):
        '''
        Parses a SFEN and sets the position from it.
        Rasies `ValueError` if the SFEN string is invalid.
        '''
        # Ensure there are six parts.
        parts = sfen.split()
        if len(parts) != 4:
            raise ValueError('sfen string should consist of 6 parts: {0}'.format(repr(sfen)))

        # Ensure the board part is valid.
        rows = parts[0].split('/')
        if len(rows) != 9:
            raise ValueError('expected 9 rows in position part of sfen: {0}'.format(repr(sfen)))

        # Validate each row.
        for row in rows:
            field_sum = 0
            previous_was_digit = False
            previous_was_plus = False

            for c in row:
                if c in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    if previous_was_digit:
                        raise ValueError('two subsequent digits in position part of sfen: {0}'.format(repr(sfen)))
                    if previous_was_plus:
                        raise ValueError('Cannot promote squares in position part of sfen: {0}'.format(repr(sfen)))
                    field_sum += int(c)
                    previous_was_digit = True
                    previous_was_plus = False
                elif c == '+':
                    if previous_was_plus:
                        raise ValueError('Double promotion prefixes in position part of sfen: {0}'.format(repr(sfen)))
                    previous_was_digit = False
                    previous_was_plus = True
                elif c.lower() in ['p', 'l', 'n', 's', 'g', 'b', 'r', 'k']:
                    field_sum += 1
                    if previous_was_plus and (c.lower() == 'g' or c.lower() == 'k'):
                      raise ValueError('Gold and King cannot promote in position part of sfen: {0}')
                    previous_was_digit = False
                    previous_was_plus = False
                else:
                    raise ValueError('invalid character in position part of sfen: {0}'.format(repr(sfen)))

            if field_sum != 9:
                raise ValueError('expected 9 columns per row in position part of sfen: {0}'.format(repr(sfen)))

        # Check that the turn part is valid.
        if not parts[1] in ['b', 'w']:
            raise ValueError("expected 'b' or 'w' for turn part of sfen: {0}".format(repr(sfen)))

        # Check pieces in hand is valid.
        # TODO: implement with checking parts[2]

        # Check that the fullmove number part is valid.
        # 0 is allowed for compability but later replaced with 1.
        if int(parts[3]) < 0:
            raise ValueError('fullmove number must be positive: {0}'.format(repr(sfen)))

        # Clear board.
        self.clear()

        # Put pieces on the board.
        square_index = 0
        previous_was_plus = False
        for c in parts[0]:
            if c in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                square_index += int(c)
            elif c == '+':
                previous_was_plus = True
            elif c == '/':
                pass
            else:
                piece_symbol = c
                if previous_was_plus:
                  piece_symbol = '+' + piece_symbol
                self.set_piece_at(square_index, Piece.from_symbol(piece_symbol))
                square_index += 1
                previous_was_plus = False

        # Set the turn.
        if parts[1] == 'w':
            self.turn = WHITE
        else:
            self.turn = BLACK

        # Set the pieces in hand
        self.pieces_in_hand = [collections.Counter(), collections.Counter()]
        if parts[2] != '-':
            piece_count = 0
            for c in parts[2]:
                if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    piece_count *= 10
                    piece_count += int(c)
                else:
                    piece = Piece.from_symbol(c)
                    if piece_count == 0:
                        piece_count = 1
                    self.add_piece_into_hand(piece.piece_type, piece.color, piece_count)
                    piece_count = 0

        # Set the mover counters.
        self.move_number = int(parts[3]) or 1

        # Reset the transposition table.
        self.transpositions = collections.Counter((self.zobrist_hash(), ))

    def push_usi(self, usi):
        '''
        Parses a move in standard coordinate notation, makes the move and puts
        it on the the move stack.
        Raises `ValueError` if neither legal nor a null move.
        Returns the move.
        '''
        move = Move.from_usi(usi)
        self.push(move)
        return move

    def kif_pieces_in_hand_str(self, color):
        builder = [[
            '\u5148\u624b\u306e\u6301\u99d2\uff1a',
            '\u5f8c\u624b\u306e\u6301\u99d2\uff1a',
        ][color]]

        for piece_type in range(ROOK, NONE, -1):
            if self.has_piece_in_hand(piece_type, color):
                piece_count = self.pieces_in_hand[color][piece_type]
                if piece_count:
                    builder.append('\u3000')
                    piece = Piece(piece_type, color)
                    builder.append(piece.japanese_symbol())
                    if piece_count > 1:
                        builder.append(NUMBER_JAPANESE_KANJI_SYMBOLS[piece_count])

        return ''.join(builder)


    def kif_str(self):
        builder = []

        builder.append(self.kif_pieces_in_hand_str(WHITE))

        builder.append('\n ')
        for file_num in range(9, 0, -1):
            builder.append(' ')
            builder.append(NUMBER_JAPANESE_NUMBER_SYMBOLS[file_num])
        builder.append('\n+---------------------------+\n')

        for square in SQUARES:
            piece = self.piece_at(square)

            if BB_SQUARES[square] & BB_FILE_9:
                builder.append('|')

            if piece:
                builder.append(piece.japanese_symbol_with_direction())
            else:
                builder.append(' \u30fb')

            if BB_SQUARES[square] & BB_FILE_1:
                builder.append('|')
                builder.append(NUMBER_JAPANESE_KANJI_SYMBOLS[rank_index(square) + 1])
                builder.append('\n')

        builder.append('+---------------------------+\n')

        builder.append(self.kif_pieces_in_hand_str(BLACK))

        return ''.join(builder)

    def __repr__(self):
        return "Board('{0}')".format(self.sfen())

    def __str__(self):
        builder = []

        for square in SQUARES:
            piece = self.piece_at(square)

            if piece:
                if not piece.is_promoted():
                    builder.append(' ')
                builder.append(piece.symbol())
            else:
                builder.append(' .')

            if BB_SQUARES[square] & BB_FILE_1:
                if square != I1:
                    builder.append('\n')
            else:
                builder.append(' ')

        if len(self.pieces_in_hand[BLACK]) + len(self.pieces_in_hand[WHITE]) > 0:
            builder.append('\n\n')

            # pieces in hand
            for color in COLORS:
                for piece_type, piece_count in self.pieces_in_hand[color].items():
                    builder.append(' ')
                    piece = Piece(piece_type, color)
                    builder.append(piece.symbol())
                    builder.append('*')
                    builder.append(str(piece_count))

        return ''.join(builder)

    def __eq__(self, board):
        return not self.__ne__(board)

    def __ne__(self, board):
        try:
            if self.occupied != board.occupied:
                return True
            if self.piece_bb != board.piece_bb:
                return True
            if self.pieces_in_hand != board.pieces_in_hand:
                return True
            if self.turn != board.turn:
                return True
            if self.move_number != board.move_number:
                return True
        except AttributeError:
            return True

        return False

    def zobrist_hash(self, array=None):
        '''
        Returns a Zobrist hash of the current position.
        '''
        # Hash in the board setup.
        zobrist_hash = self.board_zobrist_hash(array)

        if array is None:
            array = DEFAULT_RANDOM_ARRAY

        if self.turn == WHITE:
            zobrist_hash ^= array[2268]

        # pieces in hand pattern is
        # 19 * 5 * 5 * 5 * 5 * 3 * 3 = 106875 < pow(2, 17)
        # just checking black side is okay in normal state
        i = (
                self.pieces_in_hand[BLACK][ROOK] * 35625 +
                self.pieces_in_hand[BLACK][BISHOP] * 11875 +
                self.pieces_in_hand[BLACK][GOLD] * 2375 +
                self.pieces_in_hand[BLACK][SILVER] * 475 +
                self.pieces_in_hand[BLACK][KNIGHT] * 95 +
                self.pieces_in_hand[BLACK][LANCE] * 19 +
                self.pieces_in_hand[BLACK][PAWN])
        bit = bit_scan(i)
        while bit != -1 and bit is not None:
            zobrist_hash ^= array[2269 + bit]
            bit = bit_scan(i, bit + 1)

        return zobrist_hash

    def board_zobrist_hash(self, array=None):
        if array is None:
            return self.incremental_zobrist_hash

        zobrist_hash = 0

        squares = self.occupied[BLACK]
        square = bit_scan(squares)
        while square != -1 and square is not None:
            piece_index = (self.piece_type_at(square) - 1) * 2
            zobrist_hash ^= array[81 * piece_index + 9 * rank_index(square) + file_index(square)]
            square = bit_scan(squares, square + 1)

        squares = self.occupied[WHITE]
        square = bit_scan(squares)
        while square != -1 and square is not None:
            piece_index = (self.piece_type_at(square) - 1) * 2 + 1
            zobrist_hash ^= array[81 * piece_index + 9 * rank_index(square) + file_index(square)]
            square = bit_scan(squares, square + 1)

        return zobrist_hash


class PseudoLegalMoveGenerator(object):

    def __init__(self, board):
        self.board = board

    def __bool__(self):
        try:
            next(self.board.generate_pseudo_legal_moves())
            return True
        except StopIteration:
            return False

    __nonzero__ = __bool__

    # TODO: Counting without generating actual moves
    def __len__(self):
        return sum(1 for _ in self)

    def __iter__(self):
        return self.board.generate_pseudo_legal_moves()

    def __contains__(self, move):
        return self.board.is_pseudo_legal(move)


class LegalMoveGenerator(object):

    def __init__(self, board):
        self.board = board

    def __bool__(self):
        try:
            next(self.board.generate_legal_moves())
            return True
        except StopIteration:
            return False

    __nonzero__ = __bool__

    def __len__(self):
        count = 0

        for move in self.board.generate_legal_moves():
            count += 1

        return count

    def __iter__(self):
        return self.board.generate_legal_moves()

    def __contains__(self, move):
        return self.board.is_legal(move)


class SquareSet(object):

    def __init__(self, mask):
        self.mask = mask

    def __bool__(self):
        return bool(self.mask)

    __nonzero__ = __bool__

    def __eq__(self, other):
        try:
            return int(self) == int(other)
        except ValueError:
            return False

    def __ne__(self, other):
        try:
            return int(self) != int(other)
        except ValueError:
            return False

    def __len__(self):
        return pop_count(self.mask)

    def __iter__(self):
        square = bit_scan(self.mask)
        while square != -1 and square is not None:
            yield square
            square = bit_scan(self.mask, square + 1)

    def __contains__(self, square):
        return bool(BB_SQUARES[square] & self.mask)

    def __lshift__(self, shift):
        return self.__class__((self.mask << shift) & BB_ALL)

    def __rshift__(self, shift):
        return self.__class__(self.mask >> shift)

    def __and__(self, other):
        try:
            return self.__class__(self.mask & other.mask)
        except AttributeError:
            return self.__class__(self.mask & other)

    def __xor__(self, other):
        try:
            return self.__class__((self.mask ^ other.mask) & BB_ALL)
        except AttributeError:
            return self.__class__((self.mask ^ other) & BB_ALL)

    def __or__(self, other):
        try:
            return self.__class__((self.mask | other.mask) & BB_ALL)
        except AttributeError:
            return self.__class__((self.mask | other) & BB_ALL)

    def __ilshift__(self, shift):
        self.mask = (self.mask << shift & BB_ALL)
        return self

    def __irshift__(self, shift):
        self.mask >>= shift
        return self

    def __iand__(self, other):
        try:
            self.mask &= other.mask
        except AttributeError:
            self.mask &= other
        return self

    def __ixor__(self, other):
        try:
            self.mask = (self.mask ^ other.mask) & BB_ALL
        except AttributeError:
            self.mask = (self.mask ^ other) & BB_ALL
        return self

    def __ior__(self, other):
        try:
            self.mask = (self.mask | other.mask) & BB_ALL
        except AttributeError:
            self.mask = (self.mask | other) & BB_ALL
        return self

    def __invert__(self):
        return self.__class__(~self.mask & BB_ALL)

    def __oct__(self):
        return oct(self.mask)

    def __hex__(self):
        return hex(self.mask)

    def __int__(self):
        return self.mask

    def __index__(self):
        return self.mask

    def __repr__(self):
        return 'SquareSet({0})'.format(bin(self.mask))

    def __str__(self):
        builder = []

        for square in SQUARES:
            mask = BB_SQUARES[square]

            if self.mask & mask:
                builder.append('1')
            else:
                builder.append('.')

            if mask & BB_FILE_1:
                if square != I1:
                    builder.append('\n')
            else:
                builder.append(' ')

        return ''.join(builder)

    def __hash__(self):
        return self.mask

# 81 * (14 piece types * (white or black) - 1) + 9 * (ranks - 1) + (files - 1) + ((white or black) - 1) + (current turn) + log2((19 pawn in hand) * (5 lance in hand) * (5 knight in hand) * (5 silver in hand) * (5 gold in hand) * (3 bishop) * (3 rook))
#  = 2268 + 1 + 17 = 2286
#
# Genetation code example:
# import random
# for i in range(2286):
#     if i % 4 == 0:
#         print '    ',
#     print '0x{0:016X},'.format(random.randint(0, 0xffffffffffffffffL)),
#     if i % 4 == 3:
#         print ''

DEFAULT_RANDOM_ARRAY = [
    0xA00BA23D355457E0, 0x936C0433901EA29F, 0x193885748B2FACB5, 0x464E150938BDAF0F,
    0x2B7DDF4DC0930A5B, 0x14ADD43280013F55, 0xF262C03F5FC85FC2, 0x376DB10E5C008CAD,
    0xCC929DA83D4FC6D6, 0xD9848B631A50F710, 0x240DF7C8054E13FD, 0xA42FC71E6A939CAA,
    0x877E00101419152D, 0xAF085DBE0083B1BA, 0x0E6E14ACE7437F02, 0xDD3283EE937A4E10,
    0xB8158CEF51A5389E, 0xCAAD242159C62E1E, 0xF569C9FBC2BFC0D2, 0x5030988B015F4378,
    0xD3E685335E93DC15, 0xA2B7F6DEDA98AB2B, 0x75D95C333ECAC1E2, 0x04A513645871D07F,
    0x6B7AEDC285B335A6, 0xA812F75D625DCF44, 0xC02BE585F106C48F, 0x8E57AA4A75B38E15,
    0xE57DB684A7D3EF5B, 0x2BB45225A58F8749, 0x6AFB82ECC2DDC467, 0xE55F9C94ABCBFA0A,
    0x2BFA7A36AD3C712A, 0x52CF96C10DD820F6, 0x2CDA6E705E2BB9CA, 0xB7023DF3291918D3,
    0xC80F2D5A84448FC4, 0xEA293DEA88751CE5, 0xFFCF7D0F37B7E03A, 0x6C141861D60C4647,
    0xD6CB3FC399888E08, 0x2829A8BD05E27AA2, 0x936D39883BD1F706, 0x26EBC5AC48AE8FB8,
    0xA28ED33DB4E62404, 0x2E6808E4F95869B2, 0x4550E44501CBFF27, 0xB4BFD4588EBFFAC9,
    0xC508049124CCF6FC, 0x0B1B181E2F9BEE1D, 0xA55A06DA715FA127, 0x0D284C5618C592D4,
    0xB7E11E3BAE60005E, 0x731A5B1DF88D5ED5, 0xF0DCDF771FFA119E, 0x1C5957CB95AE5522,
    0xA43A7EC7EB939EFB, 0x1F334BEFF7200FED, 0xAA7D5ABA2700CE2B, 0x6A0697B9A30A6693,
    0x16BD65B1F0BDD4EA, 0x81D6129B0FB02A23, 0x64D9A564B0D01DCF, 0xF6C5B44831A810C0,
    0x53F777EAA417A0F9, 0x7D9884177198E8CF, 0x2F419147731115B4, 0x2F74531B894D0379,
    0x84EBAD88DE7DE769, 0x8D51F4318DC7AF63, 0xCDF9704B501B5D07, 0xB15452A0C8EDF394,
    0x897FCC50399C95B4, 0x72C68C0DD3F8E99D, 0x9588ED137D46A419, 0xD0E381A842AC59CD,
    0xE2357FDB3467E4FB, 0x8434B5D95B00B8B3, 0xFC842734D396FD1C, 0xDBC33DBF1175FB0B,
    0x966622B80B69B5DD, 0x4F0CB805575D7CB6, 0xE7775F663936867C, 0xC0A8A91679E004FA,
    0xAB4C4DB95C2A7B92, 0x0AED4EA2C515B1D4, 0xCA3C2DEFCE5FAED8, 0x88EE78388EE392F2,
    0x67AB518A15CACB5B, 0x3140A90C26EA14B1, 0xBBE6A425421D10FA, 0x72CB596EA36963B9,
    0x1A4CBA0E04CDF0AD, 0xE69268FDF2E9A1B8, 0xEC8CEA165DB466A9, 0x86DABCEB018BE562,
    0x0D0EBE1F622F9E12, 0x9D84352FB02B3BE4, 0x05F18A3FC1A0477D, 0x536A6C5323E1E085,
    0x0A97998A1F1D1C26, 0x720C002ACDC8FFE3, 0xFDA186C7FB5BF103, 0xED5F1326873A76D0,
    0x4C6A337095BB82F2, 0x494FD73838180591, 0x7E0B05692AA08C38, 0xB8D625DF12C14DDD,
    0xCD29FE893A1F2679, 0xF357DDBE9F26B82E, 0xA0F4EB53DA95338D, 0xA4BD25FB26A8AE97,
    0xA451A03D79C6A18A, 0xA5BAA791C0398CAB, 0x6550A0E11A93B258, 0x0AEE0F8D9AAC5543,
    0x79CE9694D4374634, 0xA746752AD5D30921, 0x33595C54AECBA086, 0x3502F347B409EF01,
    0x6CF4D916FF9D23F0, 0x32D5BF1BA27B0176, 0xC8109CF0C0B3E371, 0xA22665CB2039E416,
    0x41B5F2D822F5A4F7, 0x6A4CB9C032DA4B24, 0x1BD3B20B47D1AB13, 0xF0DBF057B6C60C50,
    0x779010079AA8A356, 0x9264FA86C5012F4B, 0x19CFD491A9A5AC6C, 0xC36F84CB5E72EB4E,
    0x0FCDD6C4250B8D70, 0x4BF882E3DDD13C14, 0x1D5FB18BF0CD9E8A, 0x8E704B6FE500D6D8,
    0x7D10E0EC401738F6, 0x26C269FDFADB69EC, 0x385C1FA93484929F, 0x923BEB958D924789,
    0x4CDF4EDBCD957634, 0x975190ADAE851F5A, 0xB4A341100F4EC7C8, 0x776B0894B34FDCD5,
    0xEFCDC5CE193F5364, 0xE68EA733D43D237C, 0x092EC792E29BA1ED, 0xC7233B53BE0CF3A0,
    0x49D1E81ED122A6F7, 0x22D80C3071B79934, 0xE90642AE2A90A5FB, 0x96E1F2B12EE4DBF6,
    0x16C8E0BC2D2EAD42, 0xFF2568F09BD0870E, 0xDB3905CAE304917E, 0xE4EDC1D6CD8FCF3B,
    0x69FF649B065DE164, 0x9949AB8FE3E44F88, 0xB6901862E34A4DCD, 0xC6E584E7672EC476,
    0xFE2C23F96939A067, 0xCDC319E76A508A11, 0xED48D7CECF09ACB1, 0x0FC9ADB5BECAAC7A,
    0xC02DB31C58D4BEA2, 0xF7819CB89209A67B, 0xEACFC8CDB8C2E184, 0xE683757DCCF29DB9,
    0xAEC6AE4C40DD991A, 0x258B19878E41A2A2, 0xAF91386900709CEF, 0x396E405CFC79F447,
    0x7E2D8878401264CF, 0x81E504C7AA30A38E, 0xD426943C837B9501, 0xBD796D89867AE1AF,
    0x35830D45D65F40AD, 0xA50B9EE6D329CFCE, 0xEA83AFC2257D0EEE, 0xE30A4245B7EB4F86,
    0x0DF32B6CA1830319, 0x00311690861E91B1, 0x2F47FBE9BE2789CC, 0x4E7526AE0D6CFFEB,
    0xDC547D5BF15DFFA7, 0x98BF3B2A6274C3D9, 0xAB9920F6B16B433F, 0xBCBD761A2E4AB74B,
    0xE67BE386071DC0AA, 0x2104D78BC2E7A94C, 0x742A98B985C1A29E, 0xE210C85E7D42B6AC,
    0x4492C5941CD0DB4D, 0x1474DAD7BE23239A, 0xD0906E273E837ACD, 0x53A1DF02D01A9D81,
    0x3DB1031774656A6D, 0xE391E90CF9FCBE3D, 0xC220F3CA9DEB87F6, 0xEE1496102DE66CC4,
    0xCBF35C876A09E6A3, 0xB48C5C395CD1EF44, 0xF82E573F81B369D7, 0x419BC7AE31B08111,
    0xC8403A113B79996F, 0xF764756573F780C5, 0xFC0F970349E032D9, 0xAD8BD7A071919A6E,
    0x3E3EFC60F538FEF6, 0xEF565998939D7734, 0x24D5253A4F1C3569, 0xC7D1D27FE61E377C,
    0xA6B8C4F3D5F6AA6A, 0xB60D6F85FB7A6371, 0x0D0013855A1BE4A0, 0x2B10CD68CF6D1A9B,
    0xC76C19696DE43DCB, 0x8F6740BE3011AC80, 0x72BBC5CFC30818EB, 0x9DB8F455AD6BE2B7,
    0xAC33A2F639DF7BD4, 0x82DB7F12CC641738, 0x1EC601CE5D00A78B, 0xB420244C4B92DFD6,
    0xEBCB6D61B7323F57, 0xD69DFA7B0256F69F, 0x802419D8E1EA82C9, 0x5AC538C8DC8D1D3B,
    0xA139C70C6242CD23, 0x487616A09708914C, 0x88D35B13220B123C, 0x5DB7D52B8B5739F1,
    0x262EC5FAE0EE1C0E, 0xB79AF8250D9B9A15, 0x5BA21695C48E2B38, 0xF6FC646689CB919B,
    0xF010CC3A3B7160D3, 0x151E2D79D8DDF6EC, 0x2613BCDF13EC0851, 0x4369A31B741C9A5D,
    0x62A4BFBC58C7EE52, 0x7AE684DB83ED2887, 0xF870B2F0EDD67AA9, 0x26A0FFE9841DD7F5,
    0x66EF8F73D4D70BB7, 0xE9E51993D5AA7F4C, 0xC094AECE63FDDD0D, 0x91478F0BB2EF94F5,
    0xA66F4D63B05086A8, 0x6E41D92AEAEAF8F6, 0x3EC6E42F5C499DE1, 0xA82E455D57DC3CB9,
    0xF04B8DE7E4F0AA54, 0x003058B9CC6E078F, 0xD1B0E2D6AFF5AD2F, 0xF62E9878ABCB0857,
    0xA22311551FB15F21, 0x90DE44DF934DE4A0, 0xA5FC7A28D913F6F6, 0xBBDF2F78993B571A,
    0xCD7EA31E0C73E742, 0x9FB52D2234C510E2, 0xE7BA0CE83DE0FA3E, 0x1E64DB39338A795D,
    0xC1D6A95C118CC413, 0x893568E51AFD81B2, 0xB25A3E684A39A686, 0x29A7087482D9BCB0,
    0xC149EDE2719D23D9, 0x5365D8B5220796FC, 0xE4638F1131693693, 0xB664ED4FFB816E2F,
    0x4AD24AF2F0DD045A, 0xDD4ED35D7D639578, 0xEDE8FFEB8E65F1D6, 0x06828EE95B3151E9,
    0x97D8F755E0B47C56, 0x81362D9AF3366E7F, 0xDEC6053A145873E3, 0x04D7AEEFFE4AA2A1,
    0xE740A5BE6D063D4A, 0x55DAEA772E241C89, 0xA943BE183D7C3627, 0x9F5D0B5DDC73C6AE,
    0x596CE71E41F3D75E, 0x6236A7177F255476, 0xAA75067085FDEBF6, 0x167B0977F34E1FE8,
    0x52B4A8AA120BA9CF, 0xE7A243F0F25A6AED, 0x1AEF9869EFDC56DE, 0xFF8D063E1AB43BA4,
    0xC724A48D226EC6B9, 0x33607D7D2D59B024, 0x7736EDECB514F4EF, 0x149A4E2B1F3C10BA,
    0x24AAFAFC81D57786, 0x3763AEB07E6B2510, 0x5052AC57433726A5, 0x067493B80290BB05,
    0x94693A00B49619F9, 0x2B255EF78C7BFBA7, 0x9942FB79FFF21592, 0x174C1FCDFB079FAC,
    0x04B8C8867159AAE9, 0xB738DF33198DB3B5, 0x93730D00ACCD4037, 0xD85E1B5A20736068,
    0x5A95D87EFAA089B2, 0x253EB1A474EA6288, 0xC9C3F536BF42AEA6, 0x4EF3AB7F2BF9BF54,
    0x567F4328169F24B7, 0xF1B047ABF87DCB17, 0x4A28CB0D722F53B0, 0x75D8462C8262EF76,
    0x92E9BEA65D14A921, 0x7AFB0D0701D86C50, 0x1A56176096AF324F, 0x1D003EE90057FBA5,
    0xA9E394E2F08BF59B, 0x58755C97EC7B5AE6, 0x7A3EF1E8AF2B0DDB, 0x0D5DA4F40F4B2CAC,
    0xC6D5A53382EBD6D5, 0x30EC2CF8DDD96C0E, 0xDD5B8BBDBFB7C554, 0x3228918DE85C09A1,
    0x4D930DB58B88282B, 0x3A05F8392718599B, 0x4B2DE9E42039E5D7, 0x092528B5B57367B1,
    0xDE3E4A47A464D6BE, 0x0DB9249534AD2B6C, 0x53CC04328683BF8E, 0x0E7C6FC4202740F1,
    0x1D8F44275E8F53CB, 0x7A820F3F26E59EF7, 0xF8DD47C037DA8688, 0xD3A7B7A4480B35AE,
    0x11C8985C856C4C3D, 0x1410591BA4395E38, 0x2A17331E08234B97, 0x067AF6CFCC702E15,
    0x6624D2B7013FE4AD, 0x32A31B99B9FEC1C1, 0xD08CC1E24108D187, 0x411C8F05CED44A06,
    0x35BD2D92AE7997A2, 0xF0C84F5796B7A24F, 0x0F1486ADE4E82C42, 0xC8CCB81964200A07,
    0xD7FFFF207A585650, 0x57E2B1B0814BF6A1, 0x0B374E507696B4EA, 0x10237B6863E8CC06,
    0x78BF9A38915FE015, 0xBD53660E2C67A23C, 0xB25043F2CB243423, 0xD08FF1D5715B02C1,
    0xF8B340701490E1D4, 0xD89C11AF6A259C84, 0x8172832EAF06797B, 0xA8325217C83FD6C1,
    0x5ABC78C661631D6E, 0x1A3F94F20614FE78, 0xA570A49909789AED, 0x5B6E7268950D700A,
    0x089C5E864BCF8B21, 0x523FC763DD7B48D6, 0x8EDFC46663EEAFBA, 0xDE59F8E0C946A6ED,
    0xA59F9AD89F2DC9E8, 0xA54DB71AAA033895, 0xA7B56E001F5C9D2E, 0xF9062E68C5E3662F,
    0x802D0A585F1C8F28, 0xE24C971FC96C2B6C, 0x7BE607E510C80969, 0xDEA89DDB23C2D430,
    0xD3B7F5A1786C4CE5, 0x4E7EE8E6E6DD5952, 0xBB2C4AF67FEC5D4C, 0xB5407707ED3B1E85,
    0xE7CF04396ECA58C0, 0xD3EA022B2A719C16, 0xBA638CEEED5FEF09, 0x7431B69C555935B6,
    0x10AC75451C2813F1, 0xE5754A5BDF6584F2, 0x0925FDC15EB0C3B3, 0xE2A91CB7E7DA1492,
    0xFD78EA49C116C114, 0xC574016FF6869445, 0xCA53A5B148242B8E, 0xFA16ACB7217EF7CA,
    0x224845F728B8FF39, 0x5A8B95E10212973B, 0x4A49FD0AF0E2D6D6, 0x28816B3576074F68,
    0xD1ABA4312C405EAB, 0xF4E56EB1C1023738, 0x601BF27BAC7C5D1B, 0x8A90270F73DA657F,
    0x04AE05E56D4C3450, 0xC2AB502760751DC9, 0x88B3AD3D7561E08E, 0xA994C0F1B955E094,
    0x18948BCCFC27E0FA, 0xBA9D3B472BBD86CD, 0x40E76AD659945CDC, 0x5EED560120086544,
    0x43A9C46B663D78B9, 0x404864276947C491, 0xDAEC54E80E52BA50, 0xB52597C9514C9A2B,
    0xE62DE20C1DE36694, 0xA8BDB02B3B5E6285, 0xD43DC16DB2313422, 0xC668FB7C7AC50FDB,
    0x0D1DD55BFB37EF6E, 0x8DD0DF3AD9FEE362, 0xB0C726DB9FCF1137, 0x7994234667F704E4,
    0x812E47434872A6CB, 0x4B9593CC74C4E23E, 0x04E99AC9CE222703, 0xA9BF8D6161CB1C52,
    0x9CAE47BC73C6606F, 0xDD1F909A9227EAC5, 0xA5FAA6BA5AF5D52B, 0x2F3BC9C701D08059,
    0x95B79F047ED88C8E, 0x9EB6301FA7A409C3, 0xB7F55F64CDB9B81B, 0x359318CE15711EC6,
    0x58295696874B7F79, 0x622B4FCB9D69CFE5, 0xE8628FB74FFAD49B, 0x5BC91869EE674CC7,
    0x55D1DB5345FC2720, 0xBB2DEA324B054D9C, 0x61AA39CE5528F535, 0xFA4CCCFE0391C1FA,
    0x29EF639FC03EC02F, 0x4BFE417296F883A7, 0x96273312F85C32BF, 0x75BB78FF4791FFCE,
    0xBA0AA0CD591E6C16, 0x8B7D571028C56FF6, 0xF4EAC9E321BCED4B, 0x55DFA1CDC4BDD757,
    0x68DCE935E3296D64, 0x2DA2C9B683680F2A, 0xC013769CA0A804DC, 0x51CE26B02C8793B9,
    0xBA4D03F52CE8687C, 0x93E4332394E1B048, 0xBC554E73DCE92888, 0x1C7FEFA1AEA4C9AA,
    0x91B4BB0835FE283A, 0x03904BE9F0D185C5, 0xE3751C469A8C54A1, 0xCF6E99F40BDCEC90,
    0x2F782298A4837AE0, 0x29F1613796A89293, 0xADC6C375AA68A7AC, 0x486E3A284453B97B,
    0x3A8E0E761D485E44, 0x7E62405B92A07652, 0xBFAE1AC972D34CCA, 0xBF9B6767E7764304,
    0xE7D3A0FAC4BE771D, 0xB3D8D00AF7A86C02, 0x7CAA0A77BA1CDABA, 0x624AFB8D3F8934F5,
    0x7D0657E39DF95BAC, 0xA386A2A108E65044, 0x54ADE61EE027AC20, 0x50E40C3073530090,
    0x086212BB3FCE2C22, 0xFA5D8C9F43EFEA60, 0xEBD5B1112C821C49, 0x736BCFF414D77ADA,
    0xCB07FD3ACC7293F9, 0x5E4546217EFF46BB, 0x54C9296AC5BA5727, 0x54FA19D7599CCF69,
    0x9094C51211768BE0, 0x1277DAEC209F2582, 0x427584F6A2D1631D, 0xFECEA4563C63EE96,
    0x18FF358A6ABF72BC, 0x425E8EA718F8EFD4, 0xB94AA058096A56D9, 0xAAB222C2385B1F71,
    0x0BDDFBC8717BD1CB, 0xAC8F42F146E5B353, 0x3CF484B3530226E8, 0x82F40BE7AD45DBBC,
    0x85CD09A0AD037903, 0x36FD00EADEACE5CF, 0x5DE672368BE30CD5, 0xF1AA9DC429EFC876,
    0x133BE5A01FE82019, 0x19B1A118A5B70C8C, 0xB21ECA75F747D0DE, 0x065C62240A48A09C,
    0x53768F39E19C19A7, 0x45EDFDA4C93D891C, 0xADA788FDE3C86CFC, 0xAB1929B80CAE49EB,
    0xAF3019855043D95D, 0xC34EE06A52259A7C, 0xBF843FC35C326563, 0xFCE77C10C6B0279F,
    0xF9C892A0EBBB3D63, 0xEB1C97BA61A6087C, 0x292108BF1918C6F5, 0x0848762119723E94,
    0xE2ABD3AC256CB5E5, 0xBB8F71AB62FE4C5C, 0x30761718634F6686, 0x8ED3656FBEEC46D9,
    0xBDC039E5B28889FF, 0xEA954A8049B12187, 0x3D3F938B86C28537, 0x9C5652F42256EC1F,
    0x5CCEF2CDF8F3078D, 0xA44A36BA1472F4B5, 0xDDE673E83D46972C, 0xC3D1C35F755C37C6,
    0x0C2273C2510DE27E, 0xBC04185D5DA738B8, 0xA6CC4F8478FD7261, 0xD51D785CF05C46D3,
    0x24CFF1FFECEAEC8B, 0x99CE44F283B4403F, 0x3C524F367DF78BAD, 0xBBF91F42729B2260,
    0x138663D07ADA1700, 0x7E24D44A38CAB76F, 0x80C0E8D26BA03DE8, 0x5C88FFED1E48434D,
    0x4130AEFB08B4F0D2, 0x65038466196288B3, 0x60574643F0E648B4, 0x8F3567B41E92098C,
    0xE26D43C4FD3A9870, 0x78778C0104D8CAD5, 0xE1B8FE48C591EAF2, 0xB33FBDC0376D285E,
    0x7706CB1741C89098, 0xF34A46F318542F96, 0xA22BD9034977AEE4, 0xAD90E2F475D7A8B3,
    0x6D91F9139DCCF28A, 0xDD07EBBD42F8AF86, 0x8DD017B8113F10E5, 0x62CDBACDF31C3C77,
    0x09379CB6A9EE83BB, 0x9FB494503B262BA2, 0x03B1E5E75C2946DE, 0xF38FF8445A49EC4F,
    0xFBD168E7D92C5049, 0x4EEE59A25BB4FFFB, 0xD0FE26E7528FFAEF, 0x82F8876302549876,
    0x5A6D82DF7EC10DD8, 0x1774C23FF5010C15, 0x4DC29C0290410B53, 0xA666FB99E14787A8,
    0x33F7CB48CF3743B4, 0x416D890DA3E2F342, 0xC5B65856FA25E803, 0xE3AF313992F955DF,
    0x89199050110CB849, 0x17E3C56F18872764, 0x57077BA2F844359F, 0x7C3CDA5CB4BDF4BB,
    0x9185E565C9A93C7C, 0x9C14A811FFCB0126, 0xB1E4953D61FE27C3, 0x5D7F6FC4D665723C,
    0xEB4EEFA13C3547CE, 0xD82379950BFAF669, 0xC03FB3CC0016B937, 0xBDCB5D66AD67552C,
    0x927C40FCFE60A61E, 0xF12BB75B76593001, 0x61B9F054FC97753C, 0x0DE262CD119BD7E9,
    0xE0DE632C20444252, 0xE108EFF314190FBF, 0x89AFD5246C16730D, 0xB46863E7F50A73C5,
    0x90AB39EC06AB34CC, 0x6D067DAAB7265028, 0xC648DCCB262123ED, 0xB6DFD095FF7769F3,
    0x8E838A9FF4DA0FCB, 0xF7A8BC705F87476A, 0xDDCA4E1F689F8E56, 0x1CB953BEBD2E3457,
    0xA4F598F6415A46B0, 0xDBCD7E875CD80A1A, 0x7DF8D0A38E48568A, 0xD6D7F96DB9C1A687,
    0x8E689A8C710102A1, 0xE493431A3E2B7C54, 0x2915D1DEA0D088AD, 0xD53B5FAD1FCBA717,
    0x70E5DDAACFD429B3, 0x2CC0D4D4CAA81EE6, 0x8883236AC41C5637, 0xF03971A224834CF7,
    0x002329F9638C6A5C, 0x68EC5EAFE7AB5745, 0x939E90B13D19C655, 0x4656EE3195B592F3,
    0x5037D54D994C4496, 0xB6A5EF2D8C300C1E, 0xB005C9E981EE4503, 0x3ED7AD923C3AD06E,
    0xA08C8159C627A010, 0xE040ADD121E6DC57, 0x79E43806AC565EED, 0x6B6F8846656881F3,
    0x7F0D084E182A2A3C, 0x635F66FF040B7105, 0x6DF22AEE59DC7CB8, 0x6EB26E28FDB03A04,
    0x5949C06B909A2A71, 0x709BD091CB65F0EC, 0xB553945B9A401F4E, 0x9C845E0507EA5627,
    0x81BD66F3521F66BC, 0xE419A052094B50E1, 0xF509BB41CD0EFF7E, 0xE31B827394F8BC40,
    0xA950B468DD64A100, 0x328951565E9A9DDC, 0x481651CDD3CB6227, 0x00CE03851BF71227,
    0x2A26C8124602AAA0, 0x8C7FBADE0B86C8FC, 0x053944BEAF1C4FEE, 0xBD5E8A2F40699F03,
    0xE86E8D8F11842670, 0xEDE464F15425CA57, 0x7E65CCA87FF3BC51, 0xD9562E7E0ED6343A,
    0xD866D454EE266B04, 0xF6AB2DE352F0951F, 0x410F6CF186CB5FBF, 0xE7EA30DC4C6D6758,
    0x261939333BF7865D, 0xBE86BEB54056154B, 0x20EB0F6C4A2D1661, 0xEDF0131E3F5C5E5F,
    0x103BE6C2535D991F, 0xC85DE9ECF15C82DD, 0xDBCDB1D178BD3BDE, 0x1FE54C60065A1B35,
    0x71C99FBF1F18D27A, 0x8F32DF8B7D57393B, 0x713158957F6D7841, 0xA7296AB9CCF6D1D1,
    0x471F75AA44673854, 0x70B5BA5297F652D9, 0x3B8C0DA7EDA55D8F, 0x14D9AF90DF6EA6EE,
    0x655E39F23922931A, 0xB4E56394B2176AA8, 0x79F5B23AEC3F9DB2, 0xEDB5B70B42DAB48E,
    0x8DC91563F44E3FA9, 0xFCC94748E20FC827, 0x25472B093CC8458D, 0x1837538B68FB8889,
    0x63FD334397033E55, 0x86093E15417F05DF, 0x13F3758CAC9956A8, 0xC2943FE092E84A9C,
    0x6A65997966826C92, 0xBB2C683C8504E96E, 0xB6025AA5F8E85CAE, 0x9EFA7859EBE02F09,
    0xE51AE6E422370239, 0x552F974C2EB3B76C, 0xC2A980E3C914A608, 0x757D06140DD59827,
    0xD3FBA78CCFAA4BD1, 0x7A1F7F052DD1B3D6, 0x07367452A2A04722, 0xA072C14B5438CDFC,
    0x0FBADF576281E9BF, 0xD8D31BA9D6F5EB00, 0x490440D0DC90891C, 0xF45329DDDF3D5AF4,
    0x8A1E1529C4674DB7, 0x63DF8C2FD0785921, 0xA3E67831FF49E820, 0x1E0CE839CCACA057,
    0x9D617BCCACA1F61A, 0x115D6AC213E9A929, 0x26C70BD4722AA72E, 0x2E523633931CD350,
    0x7235FD6B9019A822, 0x1C9B85D6A19CAFCD, 0xBDEC95F117EC75C3, 0x110E06E88F4E9BFD,
    0x151BE34C87BB10DA, 0xED3E760B01A36C69, 0x3538FE7B1A576DE3, 0x3BB881926F38876E,
    0x9EB69AF830167B38, 0x4E411C52932EFE07, 0x1237BFD3732D62CE, 0xFD760C2EFD734BE1,
    0xE7CF72ED76EB8A44, 0xD2E3BC092B714F71, 0x66F3D8D4A713A0E5, 0x01BAB92DA5748BF5,
    0x342A571A975955B9, 0x1B7D8ED9B69878E7, 0x9AE7DC63C7E0E8EE, 0x84B9F47C85699918,
    0x777723C84C23412F, 0x69E69B51C9BDC332, 0x9BDA9F1DACF4CF75, 0xDC1BD8D99A886E23,
    0x919F22BC78941978, 0xF79254C550106357, 0xB6252F8C6D69D0E7, 0x721D4D6721C73D01,
    0xE2C2BF22E083CA92, 0xF21AC04951C1D9B9, 0x14C992A2EABE886C, 0x3556332978C619AF,
    0xC26D33C67BF85756, 0xFBC3D828941DA841, 0xFECE9A7EB5AFF016, 0xA132D9E3A9AA5127,
    0x15C755D4C94804B9, 0xB6B49CF0F4B64338, 0xE4CDAC5341557E6B, 0x0621EAE2DFA2F6CB,
    0xC72FCF87FD403F8A, 0x504E9675BF5FC266, 0xA5D25CD9165A77F6, 0x4E26C0DC85AC2C49,
    0x69D61207CDEF560E, 0xC6472FEC8CB0E4C2, 0x22D155C75A4B5247, 0x24B7723011E50E62,
    0x0B1A47CE680D9F38, 0xF53A84D6AB670915, 0x4FBC7C00A5D5796E, 0x75951EDF3429F55B,
    0xAFC2595FF16FD112, 0xC93A4850DAEE1BB2, 0x2F37F523CE49AD53, 0xB252DE9DFDE1223F,
    0xF1B8D2332FE5BC0D, 0xE19AD9E4CBA82AE9, 0x975A45A2D3F8F274, 0x9B33BC02D9715C2E,
    0x932CCEF05A056D7B, 0xA4EF9894BDF93FC6, 0xC0A0DD968C618324, 0x97C3D213263BB979,
    0xEADCA751B0AD467D, 0x738AAAB01244DA5A, 0xA17FC4B4D11E42F4, 0x74402FE129D5DE07,
    0xBB5C214D0CF1B44F, 0x168EF7E2E1AB7F4D, 0x7F3706286FFDEBE7, 0x0B00C019C8BB9AE7,
    0xD0AF0878F8997474, 0x8BB5649C29142D8E, 0x0C9665449CEA9EEF, 0xD8A5A01116DDCA0A,
    0xFCC5905D8E445380, 0x1A5D8B37DF6CCDFE, 0x9B1EA2A83E4C942A, 0x9F10D5A10D656D0C,
    0xFE8C9C21E8C89B26, 0x75AE4221B9E1DA6C, 0x2DE6A6F2604B8208, 0x39ECF93BB702E49F,
    0x6F162FE2F294CF18, 0x1CB907C198E356BA, 0xB3441A081C1CD0C9, 0x352982000B33D547,
    0x4B7C41668C647A11, 0x5D77EE2DA62E65E5, 0x618544FCD1FB47EB, 0xD316BEF2542DC0A8,
    0xEB7C68E9903381F4, 0x5AA961A4F78BD15C, 0x5F5EF5FFE1FE048F, 0x1564C468BA4D017F,
    0xB72163B4AAC61D5D, 0x9CDCCAA247CBE914, 0x9926D5A678F8EFCB, 0x6A302BD345B3A1BD,
    0xD0E0B8AE1A0E1C43, 0x783DAD0CBFB57520, 0x6F054C4B3AB2E9F0, 0x7C62D951EA85A11F,
    0xA2899E9449A4A967, 0x38861B47572E1681, 0x6069EC9763725557, 0xCC768D7499BDCCC9,
    0xCB4663D23B2F9855, 0x616DF9E489BAEA86, 0xB469C0B5BBDAB8A1, 0xE6B398AD341A8331,
    0x63080A4291A4C1B9, 0xE316456FD715847A, 0x27EBC87D2AD2B927, 0xA08B0678C157527D,
    0xEC5D2A1C85CC681A, 0x623BAAFD2727A250, 0x1133740C6CFC6CB6, 0x80748CCF73DBCFDA,
    0x201244C426690974, 0x53381DF7A70B2AD3, 0xB6CD289FDBFD059F, 0xC1AD46D6BEF89D83,
    0x1D64982DA2109FD3, 0xFEC3AFA061B611D6, 0x41159AFA405C1D89, 0x78C669A365869F5E,
    0x85A594B75B13C882, 0x1E3905E6BE4D924E, 0x7FA1A43416177BAC, 0xF28BADE11925B9E4,
    0xD89CB7451BC8E559, 0x0180AC2AF7409FD9, 0x1296B60DF474F3EB, 0x49BA8FAF4D934983,
    0xBDBDDB12567F6B8A, 0x5C71702F31C0137B, 0x393BE38CBC76155C, 0xB6B83FD6E6C1809B,
    0xA27458CFD3889CF0, 0x7C5C47A117149319, 0x7EAAC09A6DC33CF3, 0xD3CF98B0A6C88E04,
    0x265AC83C4EB12ADD, 0xA4B9918DEFEF523B, 0x7F6E30EE7709BC02, 0x2CA145882B173957,
    0x357E0F58AB1AAF7B, 0x90AFC02108F22BC5, 0x73E37E74F1C01A53, 0x14A243B60F18802F,
    0x5C66B3DAED552C45, 0x9B4EB9E5B57163C8, 0xF2694B2E8297AF3F, 0x70E89F59C1DAEADC,
    0x49C386A6D367D3CF, 0x0BD5E74E75F9D730, 0x243F3BCAE64DE94E, 0x022B20DFAE24052A,
    0x814F0965C748AD0A, 0xD2469C17B11854B1, 0x943185E29E182D5B, 0x573523B9E86BBBE7,
    0xCF440557587DE6A6, 0xA4E3664FAB19EFBA, 0xE12616541E7A2E72, 0x419C1D20CF24A271,
    0x2CBA15E2056FAB44, 0x79E9FD65B45E3914, 0xD0EB9E9ABF92A861, 0x78A38B5DA7425F45,
    0xDE928891F9931B6E, 0x47E6EB2D2E823368, 0x3F681D90960F337D, 0xD887AB666B4C499B,
    0x05AD513851E9BF68, 0x8C687A7EE47F7D25, 0x810523990D59BF90, 0x7D3F6F2785C6D3AB,
    0x4DFE94E4059BC853, 0x62F6E44E4C84B096, 0xC88C5CE9559A22DA, 0xB7D2F77383182BF8,
    0x4815EB93A6C87464, 0x150EB66C37841C6A, 0x6D13A555B85E4040, 0x33E0321900ED585D,
    0x3384741FCFB0A729, 0xC82E5D453D46260B, 0x7CC8255146253F1F, 0x3CCF4C6AE351015C,
    0x68FD1029A77E2226, 0x7489A221E5349D94, 0x79FB38C097165D29, 0xA2E7F7527632EA61,
    0x1C1340F8612B7193, 0x80B614B875D24754, 0x443404F6625D8099, 0x963A0AC936CD877F,
    0x1E979DBB54FF8A8B, 0x904227195702ADDD, 0x47F34E448EB9088A, 0x3B81097F7BC8D214,
    0x74F36D5815D50C30, 0x2D13F7F62DEF9ACA, 0xDCCB590DD8BDEDF3, 0x9293A1858BBA1AF7,
    0x12B7D619F1706DA0, 0x9B882A0B1F603796, 0xAB81300C020DA9B1, 0xBDDBEF66422A27F9,
    0x96B5B110407E694F, 0xEEB6BE9BEDF9F29B, 0x47A037ADEF5956BC, 0x884791A723C2E7B4,
    0xA8A21C9753E9B351, 0x7856BAB31A616103, 0x1C2A29A6F45FE28F, 0xF36AED513752672A,
    0x93A06023BEB3F8BE, 0x2FC2F319D597E4AB, 0x5EC010D7CE73798E, 0x6584578449364186,
    0x53869D173F1D4319, 0x92F169F3D6F47AB9, 0xC8CD2761F4176844, 0xD4B7D409526077F3,
    0x4B55DDE61B53F9AD, 0x8C1678AEE4C5E061, 0xFBAA21100C5D2BCE, 0x9BB1865BA995707D,
    0x6B3F2289884B82A8, 0xA3E2D2BB10D01C5A, 0xD1B8170160D60922, 0x321B5D4C94907806,
    0x79FCD950A768A978, 0x8C0A6490B024F548, 0x888C40422CEA265D, 0x709F31D74EFECCCD,
    0x00C28A8967985321, 0xF0F4B14D8C4D0409, 0x4C193E20F6B77D11, 0x60E0140FEB52479C,
    0x3D99FAA266C33DD5, 0x3498E66F465DAD5F, 0xA149DDC95CAF1432, 0x7675EE3631C3AD1F,
    0x7B8FC3991F5579FA, 0x912D8F89D9ECDB89, 0x63F1D6CB5D3793A3, 0xE80BC9A9FFDE45F4,
    0x1AA3A11377F801DB, 0xD13CB1062803937A, 0x2B56042FA92401BF, 0xCE426948E1C51B7F,
    0xC88AFD39F5A4A161, 0x2DE276B42DEBDF9B, 0x1EE3D4AD404A0FB0, 0x93A84911C7189102,
    0x79D8DD7F4795CB42, 0x1479901D3A98BF51, 0xF604BE062077EB9D, 0x3FC5391171110CD2,
    0x9AF1450826B4003D, 0x41B5BA810AFB00BA, 0xD0BC955195900AE0, 0x8B7BE52566937E01,
    0x223B7F139F3BA5C8, 0xE6CA8B85FC6E2BB9, 0x98FD22BA8DA54E3A, 0xFEFC5534B49A2562,
    0x40087D919D16B16D, 0x0C76F06E68665C5E, 0xE46B19926DAACE9B, 0xF7FD9A58E650DCA1,
    0xC488E6B238091AD7, 0xAB5056643206EAE6, 0xDCFD432653BACC21, 0x3413EDBA09672EA7,
    0x99550763A13670D9, 0xE3F1D39D84C2215F, 0x33DAC447C5061976, 0x748EE9593918CDA9,
    0xDD8E275502E4979B, 0x3BEE7284D159C018, 0xCA68CB18DFE69FCF, 0x82E894C23CE9CE84,
    0x8528E1C60FCC4D2F, 0x527E5D131E00EC2C, 0xD8A8535F71F31379, 0xA5103E5C98FDA7D8,
    0x723F85534DBE9714, 0xC7CFC91459EBBC1A, 0xB1C071207E69056D, 0x96FDC7CB90567D47,
    0xECDE521944AEB0DE, 0xA2E346418DD1E1B2, 0x6349FBA54A70AB9F, 0x515BE7D43DF1FBAF,
    0x549228281B3FB892, 0x9049678279BDE467, 0x4EC8E5C81E8B8025, 0x915C83D9A188B7FD,
    0xF4EED25072CABA8D, 0x3E80D22E086F7623, 0xC7D7D73F357ACBB9, 0xA4A3E48181BAF632,
    0xD2638D4BB92F386B, 0x908372BE5A3D348A, 0x595E42BE0230D45A, 0x84D26C048AB06145,
    0xBEE8F9BE05854664, 0xCDD12D1E389362B1, 0x40150743C4A520E0, 0x305C4E57E402997E,
    0x20FD9C1F360FB62D, 0x8927A9E2719EB499, 0xECFC14DE4CE5C602, 0x89EDDF8C22B671EF,
    0x248D187B856BCD61, 0xC47B1CA256E12211, 0x1B613A25500384B2, 0xF589A5E06D2866AF,
    0x93C9B009A57CDFB8, 0x9CD1AC1E742EDBD4, 0xBA836F39ABBAB722, 0x78ECBAE662893E5F,
    0x80F4E484EEFA7EBA, 0x1AA94BA795C4DEDD, 0x21584A9E94C25C2E, 0x1E919ABACF025AEE,
    0xD568B420C6EA3B1C, 0xAEAB43291FAC6F16, 0x91F3DD0D1E434E98, 0xABCA3CED2B592356,
    0xDC0347E302E48B23, 0xDEBA190FE055B8DE, 0x512D99BED9368CD3, 0x5F8538EFD3B8B015,
    0x4B34626165100913, 0xD9FD1922BB367411, 0xD57BA08FAA6270E3, 0x99ECA5CC6B50D1FA,
    0xFA6F5A226B4A052C, 0x74F4E725EB993DCB, 0x4851F0E100E3CD70, 0x441F4A4FF0576F0E,
    0x058960133B127EE2, 0xD78CC2631A63D16C, 0x69F669EB86EB56DA, 0x0AC5EA7467403CCD,
    0x751EB91683753A95, 0xB07EDF24907A6FEC, 0x22223B79F2E7FB9F, 0x31D2B1D22A392497,
    0x2C07F74DDE60FBA2, 0xEE8448D0BA29C175, 0xD29FBCBCFBBB62D2, 0xB05E7AD553B6FEBF,
    0x63FC843379E06D62, 0x3C3C02EF6A0B6AD1, 0x78B9C8F9F3EB1230, 0x103F7D11E6F409CE,
    0x3E67F18D3671346E, 0x4A6B5D0C58B4E0D8, 0x95AAAE8A79A3CC21, 0xD6DBADBEB8A64418,
    0x23F157F287057CDE, 0xA10FA9FC94423BFC, 0xCF32D086A04EF325, 0x24CFE96CBF5A8A13,
    0xABECE5EA73B60D86, 0xFAEE8E5F7C95F501, 0x8F4D748C54D28829, 0x0B6F70AFC90A302F,
    0x58396E61DA4538BA, 0x34628A8BBFDFC1A3, 0x4D0E4465F4F76B68, 0x5E8614FF681C9436,
    0x5D3C43C7D1B6165C, 0xAF00F339158A76B3, 0x14058235DAE730DA, 0x0702BC359C662863,
    0x1AF90A425C1F3F16, 0x75EBA944307DE36D, 0x85D2226D87F127A6, 0x5E3F529F03195D9E,
    0xC0EB37AA2C9218FF, 0xC56705BD3F5C6325, 0xA10CBF745E0819CB, 0xD69DE8500BC97C22,
    0x54CDA92BFA37D893, 0x3331AD0E9C259AC8, 0x6BEB2C3A020A900D, 0x4418BF5C564222C4,
    0x9803D829E0FF2356, 0x0CC8A013539B0B50, 0xF6C2FBE89A2CE1F0, 0x3197C23A1A12E4F7,
    0x2560162647BB5336, 0x655C1934CD272F7B, 0x627B0B1BA2C3CA66, 0x12AFDD71B754FF52,
    0x4DB566CE30B388CC, 0x77CB6243E1BD7924, 0xF052C31E105B25F0, 0x2353B34E54F1EE2B,
    0x3C975CE17DE6C540, 0x48D347E3181B39B3, 0x2C2864186218A91C, 0x5A9DB230E43E09EE,
    0x0AFBF915AFC2B67E, 0xE323C3019044BD93, 0x83378D0DE5B57FF4, 0x068CEE67965DAC09,
    0x765EF86E6686DF37, 0xFA0E511786EE61D4, 0x9304CBD0E7AC8CAC, 0xAE93F62AA6084E4B,
    0x9921E5C8D680735F, 0xF5C97D1C290C14D5, 0xC865483D486BF2F7, 0x2A2A789A14BBC911,
    0x199038226098905C, 0xAA68DE57EBF7B126, 0x832F9E554693F3DE, 0xD706AE876600FD9C,
    0xB5F68C77E56DD729, 0xF643A74A1518ABEF, 0x8D591B7159FE0E28, 0x4DE53CD68B8F0F87,
    0x7B9E0A5368D0655B, 0x2BF84799263CF452, 0xCB3D142DDC2ACBCA, 0xCADC3FAE996D64B6,
    0x0193EAAD76355A20, 0xE3420EB4E3E8FA16, 0x68427959E65381E6, 0x6ED984E3F40E9387,
    0x2543AB293F5FD5D7, 0x744F74836AE414A3, 0xA209E3AE660B3382, 0x33A53CF16B3B6B0D,
    0xC046561AD4912813, 0x132DD87970CD4AAA, 0x078BC087AE560DA1, 0xCD870059F11114B2,
    0x88B7BBE460D8A4A0, 0xD5E88973F6948BA3, 0xE70D42EF13513DC6, 0x5600505893E53C4B,
    0x5824A620231D49BA, 0xC2BC466F5FF572CE, 0xD026A48834D1BB9D, 0x4B1EFD0E7B48A760,
    0xD85119BE4B391163, 0xFCC1C1D92B0B64AE, 0x9B4CE48867D7E3B9, 0xB5204268CD2BADE5,
    0x71547B501B53CE4A, 0x16ABD3D65B02EEBF, 0x67BCE5C5C24CEA8D, 0x4A66E0B1F10B818A,
    0xC7868ABA4E03D15D, 0x8A63034F4C304042, 0x4C0953DDA12196FD, 0xCAA7E0FEE10F5DAE,
    0x11FF63D178A19364, 0xA65D8662E57B1AD2, 0xBA3963A0C72C75C6, 0x9034BE591037856E,
    0x9902A375E2E8355D, 0xF9724E16A896AA23, 0x01374F7317F2CE10, 0xADE8BCF80ED7A72E,
    0x1AFE5DE83EC0A916, 0xA00A5258CDD8301E, 0x051FF7B1A19661B1, 0x6B8CCC20C101F340,
    0xC26017BEBF3DB0B8, 0xD611BAFB8745AC54, 0x74B155F80A7E65ED, 0x86C08F8B9FA49D69,
    0x389CF57CF7752D35, 0x97029194A62A289C, 0x69B0B4AE470C127C, 0xFF1866F3AF466D04,
    0x694036C26CA454D6, 0x3F312386471EF40C, 0x0A33C2A2F8217F60, 0x4D5E3CDECAE606DB,
    0xC936D22D947EBC6C, 0x3836BEADA7CCB517, 0x4B0765EAF10ADAE8, 0xC4F2C60FE67F5D38,
    0x83F21A76F3AA9887, 0x34A39DB310C3CCAF, 0x3C0E3F8A4D7E3C73, 0xD24DB80DDD8BFFA5,
    0xBB52592084DB15D5, 0xFDAFA0B03F2ADE68, 0x6A91B20989210A12, 0xC0AFDCCA303AC7F6,
    0xCB94047A7F9D19A6, 0x2209499EA033C07C, 0x267B525EAFC4EC19, 0xB1CEC23CF7E793B1,
    0x5B2F5A313A0951DD, 0xCA2A3A77ACB715DC, 0x1771C0DB3B3A04FA, 0x2501691C7E5604E4,
    0x93DE22473A9A12E8, 0xA5EBC53ECE427105, 0xF2525007282DF2B6, 0xD17DAF1EEEFDB763,
    0xBA5304258A0037BE, 0x174CC4D7BACBA7B6, 0x798B8C09CA1D8F68, 0xF2D59C5A6385B038,
    0xE06920F87627145F, 0x4EC61A6DC54C34CE, 0xDDB4522BA987B3B2, 0x13FC30252D01914F,
    0xDAB9E1BEF8DD08FA, 0x416493F04ABBB1A3, 0x7E5B0E527A5871C2, 0xD7FDB475CC35AE64,
    0xB22C28CE941721B7, 0xA97DCBFF4BA63F2E, 0x6A843244425F4E28, 0xCFB009BFFCB63A52,
    0xE818A9B031EE20A2, 0x2DCBB26A2A3F6DB5, 0x8B4C7A2A02EC0AF4, 0x3EA5637D92F78A12,
    0x928A355D2F453279, 0xB4C4BEF9AD595B9A, 0x88625A9E6E524C08, 0x00989F85C32049DD,
    0x4BC48CE663C733B8, 0x37361690BA63F214, 0x2182F0D51748275E, 0x40EDCC0A50EFDDC1,
    0x74A525961A3571F6, 0x234D5C331B67C071, 0xD16B0F8D10BF304C, 0x83FAC2DD18BA7426,
    0x07D97A0682001553, 0x7BD3519ECD00CCC1, 0x0DEB43E1061EA26B, 0x87833A43EF61F491,
    0xE4F766B4C2454DB2, 0xA5FCEBA033C901BE, 0x50E244110355BBBA, 0x85FBE3E3A86F56C1,
    0x7F22F42DC4648843, 0x5DC21BBD0CD0CB8A, 0x4091921E85AC5CA2, 0xDD1EED83C1E7645B,
    0x92C20E1F9316B84D, 0xEF49B1C8A2EC9D98, 0x4F6A446ED28A3CB5, 0x7FEBD22AD49C961A,
    0xEEA0B3760EE934FB, 0x7CBC0619DFBF22D0, 0x2DE8B5CFDB451C28, 0x4517F55ACF3AA4B8,
    0x9F38E135F6E5A7D3, 0xED3BE7B8DBC0A529, 0x38C6B547F84EA5F2, 0x56AE1EEEDFBA7536,
    0x6534B8FA56360664, 0x43BB799A8E8A32CF, 0xE3E8EF79EC40BF0A, 0x102BDC7C1F01AFC4,
    0xAC71B78FBEBA91A1, 0x588F791909EBD4D9, 0x9C9AF1F83205EA3E, 0xD8A83FA73308FC6E,
    0x23522671F7B7D2B1, 0xBC0EC72D68F968A3, 0x822AE0BBC0ED435E, 0x1ABDDE8247601099,
    0xF7D07A64FE5F0637, 0x7A60C38226C641FE, 0x13FD9D3F532982BB, 0xFCA21AD49B0C7039,
    0x84E378E2ACF1BE67, 0xD2FAFABED52D9505, 0xF2FA6FB286BF377C, 0xF1677CC673C52B7D,
    0x8D1E497B258164C8, 0x9702B50F9BC8B5AC, 0xA95BFA06AD12DDF0, 0x85E7D948C8FC6402,
    0xFED5BC45B71D9AAE, 0xA18A776AC7E34EB0, 0xA89508DB613AD35C, 0x155E209362908C04,
    0x7FC614D7E0792105, 0x65B24C5223097B02, 0xB5EC435173FF9C38, 0x806AE6BF4C0C3DB6,
    0xFB88D69D2684B2C9, 0x4735DFD679E8F632, 0x3A7FE3FACF6F68EE, 0xA27A19379FD77132,
    0x195C10EB58A5EA91, 0xEFB56ACAB7D016D6, 0x5D00017A85C02D18, 0xA3FB7DB5A355851A,
    0xFF2B8F4328399A8B, 0x4FEE0F79EE64D94B, 0x09CCA85B4568F349, 0x630A12AF237D8E5E,
    0x5F640E42B3EE0977, 0xB8F31ACE5441C975, 0xC933818A9F51F7B9, 0x263B75F6413FF545,
    0xA966D13AD9DC86D4, 0x4B18CE95ABB69BB7, 0x841DD8CD7BE75215, 0x32FD3FD67429A57C,
    0x51093FDDF32788AA, 0xA02560D711254FCF, 0x772C39A73EACF053, 0xF30C4302C3C41F16,
    0x41A70EA7B68AAD97, 0x97E27F6920FC5D98, 0x30EF0D0B163E9C94, 0x98CF8BFC8F031D8B,
    0x57A7B88572435BFF, 0xC0CD72E1ACB0C334, 0xB7A772998B643F54, 0x7F0FA4D3582F5CCB,
    0x752987881F5C6992, 0x2C606407DA6283BF, 0x74B50031D8D1EE7B, 0xDA2D342B7184A547,
    0xB6F965F291EBB1B3, 0xAC2E5AB105104998, 0xC9A8C40EC82B446E, 0x8DE3A4B6D0621E33,
    0xB03A579583625BD8, 0x9B8364B9B413C04A, 0x6F8DA00EE50A7F2D, 0x4BBB21683504F9A5,
    0xA9A25656B4827ADD, 0xBECA73C19E3A0725, 0xF56D7FD649BD3564, 0x6419EDB9EB2C969B,
    0x6BF3277AFABA0581, 0xE6EAEEA3D36E248C, 0x2126A6E4C4917246, 0xAF4B59C2796879C7,
    0x8D5209C53870F542, 0xDF7FBB9E8B983E51, 0x74196929EA5B9FFC, 0xDEB6EA9C9C812DB0,
    0x28FC2ECBC0F0BA9B, 0x5B8FB6BB7DC569AB, 0xF25607CBC7A4FDE2, 0x8365D9FCC5D4273B,
    0xF1325399AF22E459, 0x5259B1B03F9EC8A7, 0x4C9440FCDBAC55F9, 0x899C300A4466D581,
    0xC5BDF9DC41917C3C, 0x08F0B0926332FFF9, 0x191C551537153DEB, 0x343F73DDD6AD23BD,
    0x757997A7A5E1A637, 0xBCCE52CFCBDEB6B8, 0x9B5A220C2231D494, 0xC75B8F4D7D8F2251,
    0xCD23B39253FC503D, 0xE5A4BB7A082DA242, 0xF7C192C2CF1AB68E, 0xB66D344BF1503F83,
    0x101C9ED2EB319F58, 0x48E61917DAB64D0D, 0xDC45C13E1E4F3128, 0x2EB38FE431EF212F,
    0xB05BD64D08341EC8, 0x50CDF9DF276606AC, 0xB212AF70580E0F69, 0xD1C9BC3B8C53501B,
    0xB9C2DC5A0BE04C51, 0x0EFE7857FD5E2342, 0x62BB0603A5E66D13, 0xB686CAB243CA6B61,
    0x896F1CCE6D896887, 0x0D40EAC58F82782B, 0x32BF523134771ED6, 0x659A9514BF6AE340,
    0xFA57702AD9FD6AC0, 0x0D617F1343C56397, 0xA8453EA5B9527C8D, 0x579EA66B213C53E9,
    0xA867C682A3F289C9, 0xA66424203689EC00, 0x2A42C64CAD15D6C9, 0xB70E394104B3F861,
    0x4E94A06E60D90B2A, 0xD25BE2075C285FF1, 0xA7E15BC979120A47, 0xB0195B2E7BFEF7A1,
    0xF7B495F16FDE4DB4, 0x972727D30AFE9223, 0xDFBA7A4A128B978E, 0x88C3188C9BA5CF81,
    0xA26654E2A30F1FC2, 0xA75EB6EFFF951827, 0x608C45B791266EFF, 0x61312AA9B9672472,
    0xB1FE8864AAEEC02A, 0xC1D17D2369302A0A, 0xD86750CC08FE3970, 0xB2E1CF6ABC6638BE,
    0xF71A7E7FA1E1686F, 0x0DFED0A885B887EA, 0x254F3AD00E653E1A, 0x9BE0730886D96760,
    0x8D5122BE69716C21, 0x3BF189999FBBB2C5, 0xBA60D9794E50D021, 0xD5DB946C85D72CD2,
    0x145136D3377FD483, 0xD8FF29AF4945D47C, 0x85D9D01B231F31B1, 0xA7F5D5A18F440D61,
    0x4E5CD2CCF8480939, 0x4E60B0EE5D4A9EE7, 0x7ABCB7E135DF7CCC, 0x7C47750E41C0A68E,
    0x716E0E6594E06BAD, 0x185928CD4B9FF2EF, 0x06C6FD83FB430E99, 0x638231D41CC35CE8,
    0xC00F731405377227, 0xD82F0935942EC512, 0x703AE71AEE42FD32, 0xA75C95B51365AE8A,
    0x0C2EF6EE6F4B216E, 0xF3FA6B290DC089EE, 0x98F3CC79898EBE82, 0x839A00ABC963A75B,
    0x9AA4A4E87190F649, 0x6DA75E0D69F8D9C6, 0x5AA6AB44F1A9C2E4, 0x734FE28033E9C456,
    0x67C86CBC8951299E, 0x2709F901E1C25858, 0x43FF825728F0FBEC, 0x3BB0F072BE35AAA7,
    0xF73E719B30A452F1, 0x4D43D360FFDC7428, 0x8B119C8B71604C45, 0x9C8893B34CFD7EC9,
    0xF90E135F7E4B701C, 0x65123B98EDC5A6ED, 0x75332CF0735F5A1B, 0x2537FE7263A4983C,
    0x21BDD63A9B648BB6, 0x3EE3500BBC09E203, 0x39EB4CCEE56A36CA, 0xA242B5AE9414F271,
    0xE86A727C4102BE96, 0xAA1B2D0121D6B0ED, 0xF8482705CE227AF4, 0xD3B4DFEB788A3EBD,
    0xFD59132E9E53A9A9, 0xF38E2126F40F6F06, 0xD6D24D7357D77897, 0x897C4C65F4A31F18,
    0x933E52E7BCD3813C, 0x56ACC69B012CEDCB, 0xE6F9F340D7AD7C38, 0xE71EA920FB80E19C,
    0xB23C84E4650523DD, 0x3A716DBA36141E0F, 0xAC44B3223AD854F5, 0x0D64BB45E0A1A087,
    0xDFD70B9D3CF0DCEF, 0x87A5C7977103CF0D, 0x8E9454CF15367BB9, 0xC10004AF14DDEEC9,
    0xED6AB946A9E7A209, 0x7F7D5024A8386A4D, 0xBD0DD154A8288082, 0x55DB6C51190C90DE,
    0xEEE4DD558FB005B0, 0xD08105B937A4A146, 0xBAB4434BEEB9A121, 0x4857EEFFC4869B63,
    0xBF682C9185FC0961, 0x49695172586C1030, 0xEEFBE8C09888E097, 0x74A3EA0025F61BB3,
    0xF7FB4EF384BEC3D6, 0x4A65D00E8174D016, 0xC557A9879321683D, 0x7DFBA1E4B1953C18,
    0x041C7A67F87B32C4, 0x8F23C1DAB86BC152, 0x2A7D6F6835977A2B, 0x0E78251A15E10023,
    0x64BBB084ED57F67C, 0x57F9706AEE1A09FC, 0x218812D1029A99D6, 0xBAE36D200954F102,
    0xA5E63B92E2EE683A, 0xD12B7DCB5ECEC23F, 0xA355A9DD8202D7D2, 0xE9D5E07C5A0A653D,
    0xC88078D7689B549F, 0xD419DD72B842C9A9, 0x9AAF5ADF5F05E417, 0x55FCA70D2A0E8BDD,
    0xEE8A97F5C7A6A15A, 0x17D4DB0C38CA0D1D, 0xFF8019178F73C679, 0x17D6638E3DDB7735,
    0x5D895A51CDA4319B, 0x72F2CBAB9899BE6B, 0x7466E6DC5EC45354, 0x845B986F992AF551,
    0x0D773BB5A2E025B4, 0x28F620FA877A8676, 0x3E187D0385520537, 0x3479F08EDF38D6B8,
    0x88C5B5FD612AFC42, 0xC8DB4BC278D99FAF, 0xB4034BB630221B2E, 0xAE53C20E47E5B62D,
    0xF89E86EEFA1DC63D, 0xB693F0E7A122D1AC, 0xCE8CBFF5A54309A7, 0xEC24434553212267,
    0x48081797ED0FBCC3, 0xF6EBFB0005441BA2, 0x23ED7A9D01B784CE, 0x9AA0E40DD47651E7,
    0xDE177E376F39F801, 0x9E35471EB03DB45E, 0x3B16E30978C8A579, 0xCDC7845E72BBCE05,
    0x2C224B9B6E92B55F, 0x2E671ACA4FFBF469, 0x3C9BE5819E68BDB3, 0x1F69652F90FD731E,
    0xA33DAF09CF7F0CB9, 0x312C391613F779A5, 0x9134BF87070D1773, 0x7812586BBF17F3CD,
    0x68B7FD4A3B5F9DC5, 0x231EEED5C463D9A5, 0xA4822CB2771D57F3, 0xD1F9A1262395EFE9,
    0x068888197C49FFAE, 0xAF36A6071BDCF1D1, 0x9939F40B6C4E44ED, 0xAE489085EEBA866B,
    0x2ABD7A857D95695A, 0xA00F93CB7A973F0A, 0xBEA753779F661295, 0x326B6CF36AB1215B,
    0x88CBE6031EB43F07, 0x6E6D7336FDA5D2F0, 0xF134E4B1092DD233, 0x89007D9E7320EFD7,
    0xDCE2D27F603494D2, 0xA22078DD56C1D189, 0xC1C8521277769E89, 0xBD527398598BA920,
    0xD1B8A563D2561E19, 0xFADC071CE1165837, 0x93AA8F20B322EFBB, 0x49E07F0C06CE2D86,
    0x05B243011383E74C, 0xD504BB46C3ABF856, 0x2952406344C2F60D, 0x00D918252E5432C3,
    0xCDCC67EBDF56A7F4, 0xE50309D0327B3DBE, 0xA756B8C8576CF601, 0x6196BC2E28DD2CEC,
    0x8153E30E73041E7E, 0x32605ED1DC28ACAC, 0x5136548EB9C8D19E, 0xB59195C485CDF52E,
    0x5667CCD50544BB8D, 0x7614CBF1D89B7717, 0x0A7C5D164A9127D4, 0x2974C1AC91FC4488,
    0x8580524AD20B4915, 0xE3D515CB87AB679F, 0x887B4F11FC9FBF79, 0xD4FF9E623A7BC8EF,
    0x8C1EAE634BD2EE5B, 0x3A6EA1D8507E1107, 0xC7F4317487EABA6F, 0xEBAC4A7AEF691854,
    0x6EA388C69135A78B, 0x630FD4EE42A043ED, 0xD903118E0EF70B12, 0x95D38BF9041FE5A3,
    0x59DCAE1C022AF62E, 0xD4F239F9E4D97F1F, 0x319232D9B0785643, 0x2013F5B0843EFE3A,
    0xF8B0F755BF7D23AD, 0xE4B17EAB4CCD4311, 0x08CABF8CFC5E5B80, 0x98C2CCD24269565D,
    0xC03E5DB545E1FC03, 0x862C17766CF2E899, 0xE5F418F93A14248A, 0x15646A4B396C50BD,
    0x8318E7ACB580679B, 0x5B1F7F615FC45A2F, 0x8BD8FD3312F62532, 0x4B488FF07293EA20,
    0xE6A178170CEE3975, 0xC8E0ADBC1F35BC4A, 0x1F98C80E953F0175, 0xF3515E280489C50D,
    0x1429A2956E8AE415, 0xE5061BD486CC1124, 0x43F49A8D0693ABD4, 0xC1E7F57D99B1FEA3,
    0x5556DD0428D677ED, 0x8D6841EDDD259684, 0x2554D10D97F6B02D, 0x6E14973C3F6FFF02,
    0x82E1405A36E9A533, 0xE95C40CDDC1C4A66, 0x96979391EFD9637D, 0x983DB6549F2ED96C,
    0x9548A4646C460C38, 0xEA9AAA5355E4E6B7, 0x64364725CB3E4D8B, 0x1856D3BBE465FFEF,
    0xD6A16663AD16C102, 0x500219E44ED07569, 0x7F03F5398D22430C, 0x4C4FC23637DF4C6F,
    0x6833D36B51E29083, 0x5CA0160A9A715198, 0x42ECFF9A1BA20973, 0xEE17C8112807E950,
    0xDD10CE81367F83A6, 0x53FFA7822B166909, 0xC7D933197AA3EB78, 0x5451B77561C4DD5F,
    0xC03F82F7717EB223, 0xA14D671550D35D07, 0xCF8F7BF03DBFB4D6, 0xE5E84C73D8B3C1A9,
    0x1E2A8C865720E685, 0x9784642169E17DBB, 0x49B8F5E99B438194, 0xC3C2983E9405B33A,
    0x3E600D5452175978, 0x0B23CE725B5451BC, 0x9FB3577791B77457, 0x2546F7EBBC40CA28,
    0x275F9914C33C6960, 0xAE4E932158F0B561, 0x92F9F85140182BA9, 0x3B6723F8B40EFE17,
    0x882B2CC2BCF9FE50, 0x617633DD7B90897C, 0xA13F7570DA66EF56, 0x5662AB878F7E426C,
    0x1E00566D8088380D, 0xF573C4DF84B358DF, 0xD24020EE801F00D6, 0xA069BA541588E4C1,
    0xFF0F8EBB3A250BF9, 0xF6ED372B5B0878E6, 0x110C222F440CDE9F, 0xBAAA13C9E37FD9CB,
    0x98A97C0CB09C5DBE, 0x502E078E21CB0C1E, 0xE35AE46FF751E164, 0x0E1CC45C6D401084,
    0xB151BECF7E0ECB88, 0xB99FB2119D5B2387, 0x857418299213460F, 0x028EEA76F1B27E7A,
    0x283E810533856160, 0x9253DF185FD5FA23, 0x23DCD24564121C59, 0x7D9CB225D2D8653E,
    0x768FEDC9E38816A6, 0xFA3CF6C6F8ED6AAB, 0xD3F05B469AB7BB07, 0x9EDB3969272F8EF2,
    0x575B67E23ACCCCDF, 0x1820F318916EFFDE, 0xC697D7BD2E49D9B1, 0xABC01525F6885CF0,
    0x3DB6F75AC837491F, 0xDE88E9B0223F6E4E, 0x2DB334396027E543, 0x1A0227CBEEB9E887,
    0xAB8FB0C67661522E, 0x1CB50FEA0261C208, 0x462ACF22CBB6F451, 0x11253AC487CCA972,
    0x903A2C4B5D9E53DD, 0xB02CF3B873839280, 0xA4FFB6E2208079A4, 0x91CA7DDDCF9665A6,
    0x87EEF7D52CD22384, 0xD7E1AA6554F83369, 0x3A5105690C9544D1, 0x0BBC80B953DC6EC7,
    0xC33A0CA7FF722E82, 0xBFFB059AF06D71AC, 0xE15C897BFBE9A304, 0xDEACDDCE6B70DDFA,
    0x227FB7045143074B, 0x9F72D9472D138302, 0xB2BEA8580DA42879, 0x4DE0E280B81DB863,
    0xAF03B24C341F9779, 0x2D53A85A546D7414, 0xA3A0B705FDA846A5, 0x975E49D7CE4B13C0,
    0xCF03D277D0E4D282, 0xB024BF01617FD0A3, 0x40957A42CEACE224, 0xA17E14F73B363250,
    0x4C2C80980BE7B3B5, 0xD9826CD78E0FF4C3, 0x06170CD0D6072E60, 0x887571B3515C64F8,
    0x230573EEE4329BAA, 0xB273CF5195D6E5D5, 0x75542CC6D698A3A5, 0x97F57BB09DD1EBD7,
    0xB9E1ACD12073BEF5, 0x2DA3CAB7DB95984D, 0x103954D02833920C, 0xE8BE082E79507512,
    0x9CC39C87752E3B08, 0x1801AE0691F23AB5, 0x3BCD7E9B6D35CCB0, 0xC50F1FFE407DEDC4,
    0x0D34292A90245461, 0x4697CCDDFF25400B, 0x3DE21B68723BE291, 0xFAC17D65DD6C9AC5,
    0xC473E4DD21F4B32E, 0xB919D36451177352, 0xB4B0E378F4330B1E, 0x4D763DADCEE37B33,
    0xF06B8E1D851FA1A3, 0x04534E30DA848356, 0x062A553F94F5856A, 0x99827797BBCC648A,
    0x3524C78F28AC934D, 0xD0665F2294F56513, 0xB31B6FDADF441E83, 0xD80F4E6C86C4F4B3,
    0x618E9E0FC8706FB6, 0xFCE76857880B4253, 0x6EAA32EBB04D3798, 0x760CD2BD8F608742,
    0x03EF8CE630E1B1BD, 0x2A1B2AE9790BE4CE, 0xFBED9CC1BCDE7EC9, 0x86DD91F50C431657,
    0x467272280E83C32C, 0x76C52468BE5D9783, 0x32F685BB070DAEED, 0x14358C6AAFCD80BC,
    0xD7F60D091F032446, 0x871E20EDE00CEDA3, 0x2150114EAF286F8F, 0xBFD292BEA1A02427,
    0x9C0D49B47FB0BC9F, 0x9E45BCB3A8BCC393, 0x46EDF3E80482C42B, 0xAABE0F2015AE2EA8,
    0xBCF5D634E568C0E9, 0xCA7471962EF14BC9, 0xE92F2437D6FFD487, 0x4F31598F3B38D28E,
    0x7A5519988D745EA3, 0x96EC41B9C8810F3B, 0x1D4636609D252229, 0xED82723815D6C64C,
    0x70C8117CEF424144, 0xC14F1B2D69D1F810, 0x91A4FE87AF52EAE4, 0x9030AD6AAF72D2DE,
    0x52EAD274AE4F5909, 0x812F4D5B4E22FF82, 0x1DC40363E63BB751, 0x5715904F33939FC8,
    0x037EDADD73DBA5D3, 0x29E563752C5B13A5, 0xD39D926077F95FC3, 0x31F5195C69A30D7E,
    0x093734C4AE3B78D4, 0xF3975B613570B138, 0x598BF6F17797A38A, 0xA130B4ACBAB4B678,
    0x647B719BD331FC55, 0x6BDBB50D9F76DB12, 0xCD948C3AFCF2DD20, 0x5E3E088BA23EA10C,
    0xAD95AF80E89EB451, 0x3932A88EEEAFA83F, 0x3929175F4516EC7C, 0x6548BA8A96F6EA34,
    0xBC4AD103328B7999, 0xF51CD765FAD29096, 0xBF69FAFC9E73C31D, 0xEB3B5543A8478EF6,
    0xFE2A7BD9D5AE06C5, 0x5E19EF0B2EBDD728, 0x0AD7440D7BC39E76, 0x1F1D6289072E7A70,
    0xAD7F71893AF9DDB0, 0x82A9E8C648F604A2, 0x2A8EBB6D83184038, 0x36C40F1EC3B3EF3E,
    0x45FC8BEDC5EA018C, 0xD88D8DC186E838AB, 0xB17331F8D48D9FB5, 0xC0D08A2A1AD80481,
    0x6FC28B35698BE793, 0x0E3539FDFFA7BF5E, 0x45D16FC1BAC257A1, 0x83962EF568D8D57C,
    0x91641F8A5690313A, 0xF6DCBE650934710E, 0x5EC179536EEA3252, 0x2B58AC48ADF3C6D4,
    0xBB9339465A4E6C13, 0x8668FDE20C1B5E81, 0xFD1CC80E0A67D819, 0x385CBF609B948890,
    0x821E8C4AE39FD02B, 0x5A143D148B8FE4B3, 0xE1C163CD3B2BA9C9, 0xB7F449FFF60C0CD5,
    0x441FA6775B84FEAC, 0x96AD9CCDC4F8B61F, 0x2E1F2A0828C8A04F, 0x170417C4F9DA639F,
    0x8D040BCD59F006FF, 0xECA6FEF1122DFBBC, 0x8F4AB53839EA3514, 0x4ABA0E88B8272E43,
    0xC9DF049131BDC6C3, 0x78798E29BD6D62C0, 0x3297102512B3FE5A, 0x8403CB2CCB336AF6,
    0x5D6E7678C8858A3E, 0x0AA7DAB1620B7ECD, 0x5D3F3200B3DB31E8, 0x701DB0B0664FD7BB,
    0x14B6529EF9FB100A, 0x8F7CEE291898D3D2, 0x853299C2A0585E54, 0xB37AF89CDA933060,
    0xFB97E5B3CBB9A6CC, 0x16B4B85475D78C1E, 0x40C2751F8BBE5D2A, 0x2E25E22C711BE96E,
    0x243FD62F96AC7AEF, 0xC1E929FE528C5DB5, 0xCCBA9D903375D323, 0xE15530D3768EE768,
    0x00E2B4E3E67A71ED, 0xED35712D327634B1, 0x4612CD07DCDC6880, 0x85FB6835E686ADD4,
    0xCD11CD72FEC640FD, 0xF37E3046F6DC1C9F, 0x79EC7492B39BD41C, 0x34588F810764EC51,
    0xDF75C45424252007, 0xDE967B73199B6A80, 0x39866279C8629CE3, 0xF82DFD3C6CC14965,
    0xACEE6609EA16AAB5, 0x1D80A697DB28639D, 0x1E34732A5E21BC49, 0x6FB6AE60D9703B98,
    0xC26487AE9AEC039E, 0x7C6EE90290A89E9C, 0xB371EC50FE8F543B, 0x45CFB7F3CBCB82D5,
    0xAAA19450DBD84CA5, 0xB69235F669D2B921, 0x4A9E2C94A3D24838, 0x261D8C54B2875F6B,
    0xD31E44BC83B6DD47, 0xBFF537A3112E8CB0, 0xA6CB6E6A0105625F, 0xDE8382ADA244BE08,
    0x13B6C6AEA8C00E09, 0x72A2EE883E105737, 0x6EDD6B9B80260BA0, 0x6945B46A387B8EEC,
    0x6CDD2A61E86F969D, 0x9B968B6534F03C5F, 0x451DF1913B66DECD, 0x78CBC550467D62BE,
    0xBD43095349297DA3, 0x426AF209C8149A81, 0x8EA7C891903D97C1, 0xCAC3A3A25C09CE1D,
    0x4AC207D8AE99ADEA, 0x87859C5DC9CF5606, 0xAB25C65196F8C156, 0x3FE15E5656B60ABE,
    0xFB017CEC47164A94, 0x952EAAAAA0066C56, 0xCF0F14D62FC58C75, 0x0918D7AB4215F6D4,
    0x4ADDFA08C00BF825, 0x511494382D99FD46, 0x56864B6B28CDCF17, 0xDE1A493A389B04BB,
    0x0DA9D86EB21C5BC9, 0x18F296A54ED8ADF5, 0xCE673AF9CAF40589, 0xFBB55F9ABFB32AC1,
    0x78FF5D12E9827AD9, 0xB4AAC2A74B2686BA, 0x6E08C0C930827C4E, 0x65C2CAEFD8A43D73,
    0x5D0CAC59D4F7C837, 0x2133C246582586F8, 0x5E25BEA51960613C, 0x8DF57245B1D6EE3E,
    0x9D212FC80A0D6E1F, 0xFC9EED201FF3B87C, 0x7C0743E90BB406E0, 0xA71753E5CD25B05C,
    0xEF8035134EDB091C, 0x5E4391D100449CF1, 0xF75E11469F5DC61B, 0xA557256D964AF004,
    0x07096CD9E44C68E1, 0x5653F131D869C904, 0x33C1956A6E394CA2, 0x641FBB066CAE7F3C,
    0xFCF24B8BBA141579, 0x6E380EC9594E3831, 0xB9E3670E4FE44C9D, 0x3D3A1BE3B3999576,
    0x6AEF2FDBB92256F0, 0xCED89F19932AB23B, 0x3113C940FCC6D752, 0x038681322DC46EEB,
    0xA6DFEB59A29C1D45, 0xAA1A0102749CC4F9, 0x8C1FDB7C6599E2CA, 0x559467907271BF5E,
    0x3AF1A4C8739E4BDD, 0x5A2D4EB90D2F5E70, 0x84CB25D9E01E677A, 0x023B5A8F3F0E0016,
    0x76690B7403BC1916, 0xAA12A3BE08787D5A, 0x6A651CEA7D7BBF1F, 0x38C31DE0BC5B938B,
    0xA73CA9F72E3C70A7, 0x7054F5C62006B41C, 0x0404BC0975A5FDB1, 0x6978FC69E3F7244D,
    0x11B50772EFE98BD5, 0x8AFA4AAD773C9A99, 0x8A7E512FF79EE456, 0x731AB90FB19295D5,
    0x2B8193CDA88131DA, 0x594D202CC82FD078, 0xF186B3D6441CB9DF, 0xF374E1D7F3CD3325,
    0x0D5D19AABD202097, 0xDC34251A0F472D4C, 0xF15048C1ACFDA528, 0x7A3993181B4C6672,
    0xFCBF019460120812, 0x0D3EA7A145BBA084, 0x893C7516897A838A, 0xC0F1D3F0547EA1DE,
    0x9F8CCF198E7EEE7D, 0x4EA0B0404CD65E8A, 0xE391C74CF4C36574, 0xEB42A29782634334,
    0xDFA63D54452BDD00, 0xBC2F0ADD85ED933B, 0xED9E4F7DB57783B3, 0xB0A536A3E4660A33,
    0xB2CEAE8E47248974, 0xDEE7A9510FA14F10, 0x2E859EBB8D852CAF, 0x5C735103C06A5E73,
    0x444692AC7CAC569E, 0x4AA5994A4FE1F3F5, 0x110738D57527E8DB, 0x18CB8C345AA8B2DA,
    0x6ADABBCFCEC2667D, 0xEA9B89FDD88C74A9, 0x2DE8CE72E39405BE, 0x28C367DC36E97DC6,
    0x280E355171F929C4, 0xC64051D1EECF3C1E, 0xA67152BBAF4AF427, 0x27EB333225EDFD54,
    0x4D6002AF9828F278, 0xFF67D3E38E7BB20B, 0x44F9D29F993D7B6B, 0x21F858262E4EBEF8,
    0xE391563681D0F6EE, 0x02352E5E0D7F09D6, 0xC98BD4C915309F92, 0xE5FC146DB48D4317,
    0x185B9173066CCA99, 0x6FADEE7918470C7A, 0x962A52938000327D, 0x2F0C1A1E15DE0EA3,
    0x24043ADC9226DB65, 0xE63EEB355E620E30, 0xFF4F629BF94B6739, 0xD30852E8647F42D0,
    0x3528720F45F6E53D, 0x589015DA51971E01, 0x218FC58AF21A4E7B, 0x60298069D520DC14,
    0xFA2A7A57D492AA6E, 0x31FA7C3FE154CB11, 0x05F1A1B16D93C6C3, 0x3B03B923C61EEDCE,
    0x3DE04826B3109DFA, 0xAAED71634D3F78B0, 0x72F6B82A6DC9A543, 0x4E50B62E63FDF42E,
    0x1BD0A68ABD419DFD, 0x0F19587D0CBEA6BB, 0xED6F2D759EF8B71E, 0x3815512F50C04313,
    0xCEE7A28ED8EF687D, 0xCD1ED3D1BAE13C2B, 0xE330972FC900BF14, 0x71FA27FB20ACAFAD,
    0xD75B0C76FCD167B6, 0x906D54535C973D86, 0xDE583F6D88C6698B, 0x29BA705B24667A1E,
    0x6E90764F07D0BF51, 0x688CC54F706A45F7, 0x05F57C2A638240C4, 0x224758CEEF718B15,
    0xA8A50187B085ED91, 0xB4539B2FD2B7A344, 0xE88DCFF666DDFD4C, 0x71E1F3EA631EE3F9,
    0xE8AF81559A56C168, 0x9DFA5653858233EE, 0x67CEEF08E43AE36C, 0xB2DC258F879577F5,
    0x39328430B9C31D77, 0x1A5341EEF3EDCFDB, 0x94115076DB5F98C7, 0x7AB9430872FF162A,
    0x9AF012DC0C078DBF, 0x98F88158D9403045, 0xDCE339253DEBD179, 0x2FB307C70A0A255A,
    0xBF8C7B0A7E45EF7C, 0x0048711B01CD09BD, 0x010CC4B54424949A, 0xAA88826020C6AE0C,
    0x796305F0E1A5CD4E, 0x759BD1E6A6FD635A, 0x9A8F8FE6685C7B94, 0x14389722E09FD0A5,
    0x81E8251A51778F21, 0x1741F01F27B3CBFD, 0x62730D96A1C0CE82, 0x9DC8EF4ED007153F,
    0xC8551AA9810B14A5, 0x961D529EABBCE9E9, 0x1B7D97AA9423D424, 0x242FC7211D26A5B4,
    0x8EA7213871870B5F, 0x4BD81D42C8E08564, 0xC88C49387D287579, 0xA8C7DEDE15A64660,
    0x64D3C54F41F0E78E, 0x53A7180CB73EFD76, 0x3D8614E7B596800F, 0xFAA8AA7A34CD795C,
    0xE429BF99E2486DDA, 0x83DA2E9CF317BE31, 0x9E7685D4B63FF9E0, 0x778003BFBF86A7CA,
    0x8424950C1173EEE3, 0x5DA10B28A166FAC6, 0x8574F184107F3CEF, 0x1CC4C0BD261DFCCC,
    0xFEAFB8CA85B2519F, 0xDCE291F144702604, 0x4BF6D7889DB9D5A0, 0x20C7DDBE4D3EE653,
    0x19C40C809AC7A5DC, 0xD4389D02048AC2E9, 0xDE013967FD5D4742, 0xB2948EEA1A227ABC,
    0xB5CBF76567E13ACD, 0xA2655D95DF24F70B, 0x16466D64F61DBCF5, 0x42EFE79C13D49249,
    0x77134F2C835F77B3, 0xF0836845220BC356, 0x15AC6B4CB23E3025, 0x8FB58E5727164B71,
    0x1CCA375B2EFC62DE, 0x4A7F3962E148EB7B, 0x85EE69B823ACFB82, 0xBD6304F91CAD223B,
    0x2406887E1775950A, 0x0F4F1CAAA9757D82, 0x170653C6AE52C652, 0xBFBA95A52A214E27,
    0x074B4AEFC0CC0136, 0x9497D63E5AA99427, 0xAA0D9EDC41C0FBFF, 0x619F9BE17EF215F7,
    0x5ED732DF1F3150E3, 0x60265647C5CE5152, 0x9B1240D07C5C91E4, 0x1F4625D8AE9ACEC7,
    0xAC087A1B985C0D04, 0x537735369EC9BADC, 0xA1E9DAB97F8AB6DB, 0x150D152B7D587085,
    0xCB06E1300D5D514C, 0x39F0600C5CB508BA, 0x1E7797872CD1D700, 0x5F7916FD9E8A9B67,
    0x39E56FE71831F125, 0x618D047693F5047E, 0xD560B814B51A784B, 0xEB873FD0E6E424E3,
    0x61F5C1E756B5C230, 0xDAB9A81530DCA331, 0x7704C04ED4B39408, 0x70D4451CBB960D1E,
    0x9BE6AAAC2CDEFCF3, 0x7B31990E2F27EC27, 0x522D8E080A85BA34, 0x6572775C88DEAF8D,
    0xF60820165ED569F1, 0x09194A4B2B0B09EC, 0xB34FC5D33A494C20, 0x8BE1E41DF7C8E0CE,
    0x6CB422A7989DAD88, 0x3D63974B6EEEA805, 0x91CC05F625EB7F13, 0x4D4FBA5A77A35F4F,
    0xACA35AB67B0E19CD, 0x6D73768EBD6631C2, 0x3404D9D51FB5F1DB, 0x54FB1BF58EF5FAD2,
    0x67A05B2B6D050C31, 0xE9233CD8CABDCF9F, 0x258C6C2AA64E937F, 0x171223DD7B09E221,
    0x418A55FA57A7AEAB, 0x23C6818F63FEF4F1, 0x45342F17854A3904, 0xCFDCC656193F5341,
    0x16D1D6788674AEA3, 0x7E46ED0ECEE30009, 0x52736C95366817ED, 0x235F23064A2D56AB,
    0xF924BAE84FFA7D87, 0x32BCCF0B028EEB18, 0x1747C514734A26D7, 0x02CF727279ED2FC5,
    0x29B5A1B144A2B6F6, 0xD83302D527F6BBF0, 0x864AD0F7C2323C83, 0xACFC388FA8C0B3BC,
    0x00BAB0B1DCD22676, 0x913ABFBA0FA94E09, 0x3BB74CE7D6E8EB1C, 0x7075E0215616B1C2,
    0xCD14ABEDFD41019B, 0xB1A09E6EC02CA8C3, 0xC793C1123469A35F, 0x5859E4FD74A6FE76,
    0xF0AE029E921D9FBB, 0x586BD73213FAFB89, 0xC2B0BCA9B4635FC9, 0x433C2D7AA897C02F,
    0x1761F6DD291251CA, 0xA5321E961DFA6F13, 0x3E7936B0253F3BA5, 0x6EE4D5BD0D7AC34C,
    0x39BA3D6F45D5269A, 0x785E863B9C82C8D1, 0x8E1FA6B79790C98E, 0x1808219076F81108,
    0x6BD007050D1AACB3, 0x29988A2D5FE77076, 0xCD312D3FE6B594D3, 0x52733E14973A4056,
    0x3F68E1DBEB744939, 0x7A7094BA453E5777, 0x5ABA842D30E68C7B, 0xB0901CAD817E5F28,
    0xB63DA1A738369CB5, 0x921C7AEAD5600B2A, 0x6306E4EBCE486606, 0xB9CBAAC26D91338E,
    0xFEE08C7B1A8837AD, 0xD66BA93246CE432D, 0xFC818878DF99411E, 0x61C16F3590827358,
    0x7DFF70065D823D18, 0xA750F3E4B7FEDE9B, 0x7E62B1F36B834522, 0x4F2DF8B91AEDF01F,
    0xEE35F40AABCCC264, 0xDEE988C029225691, 0xE84486B80EF945DF, 0x75DDCA173369F4E0,
    0x95B367353691FF9F, 0x1F77D23F5DF1B308, 0x2B9903AE5B9ED2B0, 0xC7B5196589B9246F,
    0x456CEE2193045D80, 0x4BFF7A43733D7B83, 0xF5B8F652FAB6200F, 0x68793B7A0ED0F79D,
    0x5123EF7EF602A56B, 0xAE2A6E61F58A6CF0, 0x5B9CB204EEEEA88F, 0x33D4B27F10D1E8A6,
    0x72F6754B29914833, 0x1820B66279B33386, 0x55A63486F88017C1, 0x3338FDF3C7978FF2,
    0x60578EB221A313FF, 0x59035C38DB161D40, 0x031D167625CF213A, 0xE30644C6F8541D4E,
    0xA87D6521FC277B09, 0x7A279646447F68F5, 0x0F66FC2A91B656F9, 0x3A18B04B98163B38,
    0xFEF4D04DE66174B6, 0xB7DC4069DB1D484F, 0x3375EF9F9B07EF5D, 0x131AAEF1EEEBFE34,
    0xF65B22576E91D908, 0x868B68B8C0D57D99, 0x15B6F67F94FEA816, 0xF8325F120F4304F6,
    0x83951AF07CE062E6, 0x9C450B161AA1D50C, 0xBD26D0D5ACBC439B, 0x41EBFBF5687571E8,
    0x86D6113C636B6F29, 0x4C532A8DB8D2B468,
]
