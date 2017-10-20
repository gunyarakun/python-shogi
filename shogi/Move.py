# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# NOTE: In chess we use "file - rank" notation like 'a1',
#       in shogi we use a number for file, an alphabet for rank
#       and opposite direction of files and ranks like '9i'.
#       We use chess style notation internally, but exports it with this table.

from .Piece import *

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
        return not bool(self.from_square is None and self.to_square is None)

    def __nonzero__(self):
        return (self.from_square or self.to_square) is not None

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
        # 7 bit is enough to represent 81 patterns
        if self.drop_piece_type is None:
            return self.to_square | self.from_square << 7 | self.promotion << 14
        else:
            # drop piece
            return self.to_square | (81 + self.drop_piece_type) << 7

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
        return cls(None, None, NONE)
