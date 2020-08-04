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

import re
import time
import shogi
import socket
import threading
import collections

DEFAULT_PORT = 4081
PING_SLEEP_DURATION = 1
PING_DURATION = 60
SOCKET_RECV_SIZE = 4096
BLOCK_RECV_SLEEP_DURATION = 0.1

COLOR_SYMBOLS = ['+', '-']
PIECE_SYMBOLS = ['* ', 'FU', 'KY', 'KE', 'GI', 'KI', 'KA', 'HI', 'OU',
                       'TO', 'NY', 'NK', 'NG',       'UM', 'RY']
SQUARE_NAMES = [
    '91', '81', '71', '61', '51', '41', '31', '21', '11',
    '92', '82', '72', '62', '52', '42', '32', '22', '12',
    '93', '83', '73', '63', '53', '43', '33', '23', '13',
    '94', '84', '74', '64', '54', '44', '34', '24', '14',
    '95', '85', '75', '65', '55', '45', '35', '25', '15',
    '96', '86', '76', '66', '56', '46', '36', '26', '16',
    '97', '87', '77', '67', '57', '47', '37', '27', '17',
    '98', '88', '78', '68', '58', '48', '38', '28', '18',
    '99', '89', '79', '69', '59', '49', '39', '29', '19',
]
SERVER_MESSAGE_SYMBOLS = [
    # '#' prefixed
    'WIN', 'LOSE', 'DRAW', 'SENNICHITE', 'OUTE_SENNICHITE',
    'ILLEGAL_MOVE', 'TIME_UP', 'RESIGN', 'JISHOGI', 'CHUDAN',
    'MAX_MOVES', 'CENSORED',
    # '%' prefixed
    'TORYO', 'KACHI'
]
SERVER_MESSAGES = [
    WIN, LOSE, DRAW, SENNICHITE, OUTE_SENNICHITE,
    ILLEGAL_MOVE, TIME_UP, REGISN, JISHOGI, CHUDAN,
    MAX_MOVES, CENSORED,
    TORYO, KACHI
] = range(0, len(SERVER_MESSAGE_SYMBOLS))

class Parser:
    @staticmethod
    def parse_file(path):
        with open(path) as f:
            return Parser.parse_str(f.read())

    @staticmethod
    def parse_str(csa_str):
        line_no = 1

        sfen = None
        board = None
        position_lines = []
        names = [None, None]
        current_turn_str = None
        moves = []
        lose_color = None
        for line in csa_str.split('\n'):
            if line == '':
                pass
            elif line[0] == "'":
                pass
            elif line[0] == 'V':
                # Currently just ignoring version
                pass
            elif line[0] == 'N' and line[1] in COLOR_SYMBOLS:
                names[COLOR_SYMBOLS.index(line[1])] = line[2:]
            elif line[0] == '$':
                # Currently just ignoring information
                pass
            elif line[0] == 'P':
                position_lines.append(line)
            elif line[0] in COLOR_SYMBOLS:
                if len(line) == 1:
                    current_turn_str = line[0]
                else:
                    if not board:
                        raise ValueError('Board infomation is not defined before a move')
                    (color, move) = Parser.parse_move_str(line, board)
                    moves.append(move)
                    board.push(shogi.Move.from_usi(move))
            elif line[0] == 'T':
                # Currently just ignoring consumed time
                pass
            elif line[0] == '%':
                # End of the game
                if not board:
                    raise ValueError('Board infomation is not defined before a special move')
                if line in [
                            '%TORYO', '%TIME_UP', '%ILLEGAL_MOVE'
                        ]:
                    lose_color = board.turn
                elif line == '%+ILLEGAL_ACTION':
                    lose_color = shogi.BLACK
                elif line == '%-ILLEGAL_ACTION':
                    lose_color = shogi.WHITE

                # TODO: Support %MATTA etc.
                break
            elif line == '/':
                raise ValueError('Dont support multiple matches in str')
            else:
                raise ValueError('Invalid line {0}: {1}'.format(line_no, line))
            if board is None and current_turn_str:
                position = Parser.parse_position(position_lines)
                sfen = Exporter.sfen(
                    position['pieces'],
                    position['pieces_in_hand'],
                    current_turn_str,
                    1)
                board = shogi.Board(sfen)
            line_no += 1

        if lose_color == shogi.BLACK:
            win = 'w'
        elif lose_color == shogi.WHITE:
            win = 'b'
        else:
            win = '-'

        summary = {
            'names': names,
            'sfen': sfen,
            'moves': moves,
            'win': win
        }
        # NOTE: for future support of multiple matches
        return [summary]

    @staticmethod
    def parse_move_str(move_str, board):
        color = COLOR_SYMBOLS.index(move_str[0])
        from_str = move_str[1:3]
        to_str = move_str[3:5]
        piece_str = move_str[5:7]

        if from_str == '00':
            from_square = None
        else:
            from_square = SQUARE_NAMES.index(from_str)

        to_square = SQUARE_NAMES.index(to_str)
        piece_type = PIECE_SYMBOLS.index(piece_str)

        if from_square is None:
            return (color, '{0}*{1}'.format(shogi.PIECE_SYMBOLS[piece_type].upper(),
                shogi.SQUARE_NAMES[to_square]))
        else:
            from_piece_type = board.pieces[from_square]
            promotion = (from_piece_type != piece_type)
            return (color, shogi.SQUARE_NAMES[from_square] + shogi.SQUARE_NAMES[to_square] + ('+' if promotion else ''))

    @staticmethod
    def parse_position(position_block_lines):
        # ex.) P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
        # ex.) PI82HI22KA
        position = {
            'pieces': [None for x in range(81)],
            'pieces_in_hand': [
                collections.Counter(),
                collections.Counter(),
            ]
        }
        for line in position_block_lines:
            if line[0] != 'P':
                if line[0] in COLOR_SYMBOLS:
                    color = COLOR_SYMBOLS.index(line[0])
                    if len(line) == 1:
                        # duplicated data
                        position['current_turn'] = color
                    else:
                        # move
                        raise NotImplementedError('TODO: parse moves')
                else:
                    raise ValueError('Invalid position line: {0}'.format(line))
            elif line[1] in COLOR_SYMBOLS:
                index = 2
                color = COLOR_SYMBOLS.index(line[1])
                while index < len(line):
                    file_index = int(line[index:index + 1])
                    index += 1
                    rank_index = int(line[index:index + 1])
                    index += 1
                    piece_type = PIECE_SYMBOLS.index(line[index:index + 2])
                    index += 2
                    if rank_index == 0 and file_index == 0:
                        # piece in hand
                        position['pieces_in_hand'][color][piece_type] += 1
                    else:
                        position['pieces'][
                            (rank_index - 1) * 9 + (9 - file_index)
                        ] = (piece_type, color)
            elif line[1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                rank_index = int(line[1:2]) - 1
                file_index = 0
                for index in range(2, 29, 3):
                    piece_str = line[index:index + 3]
                    piece_type = PIECE_SYMBOLS.index(piece_str[1:3])
                    if piece_type:
                        color = COLOR_SYMBOLS.index(piece_str[0])
                        piece = (piece_type, color)
                    else:
                        piece = None

                    position['pieces'][
                        rank_index * 9 + file_index
                    ] = piece

                    file_index += 1
            elif line[1] == 'I': # PI
                position['pieces'] = [
                        (2, 1), (3, 1), (4, 1), (5, 1), (8, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                          None, (7, 1),   None,   None,   None,   None,   None, (6, 1),   None,
                        (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1),
                          None,   None,   None,   None,   None,   None,   None,   None,   None,
                          None,   None,   None,   None,   None,   None,   None,   None,   None,
                          None,   None,   None,   None,   None,   None,   None,   None,   None,
                        (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                          None, (6, 0),   None,   None,   None,   None,   None, (7, 0),   None,
                        (2, 0), (3, 0), (4, 0), (5, 0), (8, 0), (5, 0), (4, 0), (3, 0), (2, 0),
                    ]
                index = 2
                while index < len(line):
                    file_index = int(line[index:index + 1])
                    index += 1
                    rank_index = int(line[index:index + 1])
                    index += 1
                    piece_type = PIECE_SYMBOLS.index(line[index:index + 2])
                    index += 2
                    if rank_index == 0 and file_index == 0:
                        # piece in hand
                        raise NotImplementedError('TODO: Not implemented komaochi in komadai')
                    piece_index = (rank_index - 1) * 9 + (9 - file_index)
                    if position['pieces'][piece_index] is None or position['pieces'][piece_index][0] != piece_type:
                        raise ValueError('Invalid piece removing on intializing a board'.format(line))
                    position['pieces'][piece_index] = None
            else:
                raise ValueError('Invalid rank/piece in hand: {0}'.format(line))
        position['pieces_in_hand'] = [
            dict(position['pieces_in_hand'][0]),
            dict(position['pieces_in_hand'][1]),
        ]
        return position

class Exporter:
    @staticmethod
    def sfen(pieces, pieces_in_hand, current_turn_char, move_count):
        sfen = []
        empty = 0

        # Position part.
        for square in shogi.SQUARES:
            piece_tuple = pieces[square]
            if piece_tuple is None:
                empty += 1
            else:
                (piece_type, color) = piece_tuple
                piece = shogi.Piece(piece_type, color)

                if empty:
                    sfen.append(str(empty))
                    empty = 0
                sfen.append(piece.symbol())

            if shogi.BB_SQUARES[square] & shogi.BB_FILE_1:
                if empty:
                    sfen.append(str(empty))
                    empty = 0

                if square != shogi.I1:
                    sfen.append('/')

        sfen.append(' ')

        # Side to move.
        current_turn = COLOR_SYMBOLS.index(current_turn_char)
        if current_turn == shogi.WHITE:
            sfen.append('w')
        else:
            sfen.append('b')

        sfen.append(' ')

        # Pieces in hand
        pih_len = 0
        for color in shogi.COLORS:
            p = pieces_in_hand[color]
            pih_len += len(p)
            for piece_type in p.keys():
                if p[piece_type] > 1:
                    sfen.append(str(p[piece_type]))
                elif p[piece_type] >= 1:
                    piece = shogi.Piece(piece_type, color)
                    sfen.append(piece.symbol())
        if pih_len == 0:
            sfen.append('-')

        sfen.append(' ')

        # Move count
        sfen.append(str(move_count))

        sfen_str = ''.join(sfen)

        return sfen_str

class TCPProtocol:
    def __init__(self, host=None, port=0):
        if host:
            self.open(host, port)

    def open(self, host, port=0):
        if not port:
            port = DEFAULT_PORT
        self.host = host
        self.port = port

        self.recv_buf = ''

        self.connect(host, port)

        # Heartbeats
        self.heartbeat_thread = CSAHeartbeat(self, PING_SLEEP_DURATION, PING_DURATION)
        self.heartbeat_thread.start()

    def connect(self, host, port):
        for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.socket = socket.socket(af, socktype, proto)
                self.socket.connect(sa)
            except socket.error as msg:
                self.msg = msg
                if self.socket:
                    self.socket.close()
                self.socket = None
                continue
            break
        if not self.socket:
            raise socket.error(self.msg)

    def command(self, command):
        self.write(command + '\n')
        line = self.read_line()
        return line

    def write(self, buf):
        self.socket.sendall(buf.encode('utf-8'))

    def read(self):
        buf = self.socket.recv(SOCKET_RECV_SIZE).decode('utf-8')
        self.recv_buf += buf
        return len(buf)

    def read_line(self, block=True):
        line = self.read_until('\n', block)
        return line

    def read_until(self, target, block=True):
        while 1:
            if target in self.recv_buf:
                (result, self.recv_buf) = self.recv_buf.split(target, 1)
                return result
            else:
                if self.read() == 0:
                    if block:
                        time.sleep(BLOCK_RECV_SLEEP_DURATION)
                    else:
                        return None

    def ping(self):
        line = self.command('')
        if line != '':
            raise ValueError('Ping return must be empty')

    login_username_re = re.compile(r'\A[-_0-9A-Za-z]+\Z')
    login_response_re = re.compile(r'\ALOGIN:([-_0-9A-Za-z]+)( OK)?\Z')

    def login(self, username, password):
        if not self.login_username_re.match(username):
            raise ValueError('Invalid username.')
        if ' ' in password:
            raise ValueError('Invalid password.')

        line = self.command('LOGIN {0} {1}'.format(username, password))
        line_match = self.login_response_re.match(line)
        if line_match:
            if line_match.group(2) == ' OK':
                if line_match.group(1) == username:
                    return True
            elif line_match.group(1) == 'incorrect':
                raise ValueError('Login failed. Check username and password.')
        raise ValueError('Login response was invalid.')

    def logout(self):
        line = self.command('LOGOUT')
        if line == 'LOGOUT:completed':
            raise ValueError('Logout failed')

    def wait_match(self, block=True):
        while True:
            game_summary_str = self.read_game_summary(block)
            if game_summary_str is not None:
                return self.parse_game_summary(game_summary_str)
            else:
                return None

    def wait_server_message(self, board, block=True):
        while True:
            line = self.read_line(block)
            if line is None:
                return None
            return self.parse_server_message(line, board)

    def parse_server_message(self, line, board):
        if line[0] in COLOR_SYMBOLS:
            move_strs = line.split(',')
            move_str = move_strs[0]
            time_str = move_strs[1] if len(move_strs) > 1 else None
            (color, usi) = Parser.parse_move_str(move_str, board)
            return (color, usi, self.parse_consumed_time_str(time_str), None)
        elif line[0] in ['#', '%']:
            message = SERVER_MESSAGE_SYMBOLS.index(line[1:])
            return (None, None, None, message)
        else:
            raise ValueError('Invalid lines')

    def parse_consumed_time_str(self, time_str):
        # This function always returns float seconds.
        # TODO: refer Time_Unit header.
        if time_str is None:
            return None
        elif time_str[0] != 'T':
            raise ValueError('Invalid consumed time format')
        return float(time_str[1:])

    def read_game_summary(self, block=True):
        return self.read_until('END Game_Summary\n', block)

    def parse_game_summary(self, game_summary_block):
        time_lines = None
        position_lines = None
        names = [None, None]
        position = None
        for line in game_summary_block.split('\n'):
            if line == 'BEGIN Game_Summary' or line == 'END Game_Summary':
                pass
            elif line == 'BEGIN Time':
                time_lines = []
            elif line == 'END Time':
                time_summary = self.parse_time(time_lines)
                time_lines = None
            elif line == 'BEGIN Position':
                position_lines = []
            elif line == 'END Position':
                position = Parser.parse_position(position_lines)
                position_lines = None
            elif time_lines is not None:
                time_lines.append(line)
            elif position_lines is not None:
                position_lines.append(line)
            elif ':' in line:
                (key, value) = line.split(':', 1)
                if key == 'Name+':
                    # sente or shiatte
                    names[shogi.BLACK] = value
                elif key == 'Name-':
                    # sente or shiatte
                    names[shogi.WHITE] = value
                elif key == 'To_Move':
                    to_move_color_str = value
                elif key == 'Your_Turn':
                    my_color = COLOR_SYMBOLS.index(value)
            elif not line:
                # empty line
                pass
            else:
                raise ValueError('Invalid game summary line: {0}'.format(line))

        sfen = Exporter.sfen(
            position['pieces'],
            position['pieces_in_hand'],
            to_move_color_str,
            1)

        summary = {
            'names': names,
            'sfen': sfen,
            'moves': [],
            'time': time_summary,
        }

        return {
            'summary': summary,
            'my_color': my_color,
        }

    def parse_time(self, time_block_lines):
        time = {}
        for line in time_block_lines:
            (key, value) = line.split(':', 1)
            time[key] = value
        return time

    def agree(self):
        # TODO: check START:<GameID>
        self.command('AGREE')

    def reject(self):
        # TODO: check REJECT:<GameID> by <rejector>
        self.command('REJECT')

    def move(self, piece_type, color, move):
        if move.from_square is None:
            from_square = '00'
        else:
            from_square = SQUARE_NAMES[move.from_square]
        command = '{0}{1}{2}{3}'.format(COLOR_SYMBOLS[color],
                from_square,
                SQUARE_NAMES[move.to_square],
                PIECE_SYMBOLS[piece_type])
        return self.command(command)

    def resign(self):
        # TODO: check RESIGN
        self.command('%TORYO')
        match_result = self.read_line()

class CSAHeartbeat(threading.Thread):
    def __init__(self, ping_target, sleep_duration, ping_duration):
        super(CSAHeartbeat, self).__init__()
        self.ping_timer = 0
        self.ping_target = ping_target
        self.sleep_duration = sleep_duration
        self.ping_duration = ping_duration

    def run(self):
        if self.ping_timer >= self.ping_duration:
            self.ping_target.ping()

        self.ping_timer += self.sleep_duration
        time.sleep(self.sleep_duration)
