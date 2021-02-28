# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .Consts import *

PIECE_SYMBOLS = ['',   'p',  'l',  'n',  's', 'g',  'b',  'r', 'k',
                      '+p', '+l', '+n', '+s',      '+b', '+r']
PIECE_JAPANESE_SYMBOLS = [
    '',
    '歩', '香', '桂', '銀', '金', '角', '飛',
    '玉', 'と', '杏', '圭', '全', '馬', '龍'
]

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
