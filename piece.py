""" Author: Justin Galvez
    Name: piece.py
    Description:
"""


class Piece:
    def __init__(self, name, move_list, type):
        self._name = name
        self._moves = move_list
        self._team = name[0]
        self._position = None
        self._never_moved = True
        # self._special_moves = special_moves
        self._valid_moves = []
        self._type = type

    def __str__(self):
        return self._name

    def update_position(self, x, y):
        self._position = (x, y)

    def get_moves(self):
        return self._moves

    def get_valid_moves(self):
        return self._valid_moves

    def has_never_moved(self):
        return self._never_moved

    def _reset_valid_moves(self):
        self._valid_moves = []

    def get_team(self):
        return self._team

    def add_move(self, move):
        self._valid_moves.append(move)

    def get_position(self):
        return self._position

    def get_type(self):
        return self._type

    def update_move_status(self):
        self._never_moved = False

    def find_castles(self, board, x, y, wid, hei):
        special_moves = []

        if self.get_type() == 'King':
            y_pos = self.get_position()[1]
            if determine_castle_status(self, board, y_pos, range(1, 4), 0):
                special_moves.append((2, y_pos))
            if determine_castle_status(self, board, y_pos, range(5, 7), 7):
                special_moves.append((6, y_pos))
        return special_moves

    def find_moves(self, board, x, y):
        self._reset_valid_moves()
        wid = int(board.get_wid()) - 1
        hei = int(board.get_hei()) - 1

        if self.get_type() == 'Pawn':
            check_pawn_moves(board, self, x, y, wid, hei)
            return

        castle_moves = self.find_castles(board, x, y, wid, hei)
        if castle_moves:
            for move in castle_moves:
                self.add_move(move)

        for move in self.get_moves():
            if type(move) == list:
                for elem in move:
                    if self.is_valid_move(elem, board, x, y, wid, hei):
                        self.add_move((x + elem[0], y + elem[1]))
                    else:
                        break
            elif self.is_valid_move(move, board, x, y, wid, hei):
                self.add_move((x + move[0], y + move[1]))

    def is_valid_move(self, move, board, x, y, wid, hei):
        if x + move[0] < 0 or x + move[0] > wid or y + move[1] < 0 or y + move[1] > hei:
            return False
        else:
            square = board.get_square(x + move[0], y + move[1])

            if self.get_type() == 'Pawn' and move[0] == 0:
                if square is not None:
                    return False
                return True
            elif self.get_type() == 'Pawn':
                # print('here')
                if square is None:
                    return False
                same_team = self.get_team() == square.get_team()
                return not same_team
                # print(same_team)
            elif square is None:
                return True

            same_team = self.get_team() == square.get_team()
            if not same_team:
                self.add_move((x + move[0], y + move[1]))
                return False
            return not same_team


def check_pawn_moves(board, piece, x, y, wid, hei):
    move = piece.get_moves()[0]
    if piece.is_valid_move(move, board, x, y, wid, hei):
        piece.add_move((x + move[0], y + move[1]))
        new_move = (move[0], move[1] * 2)
        if piece.is_valid_move(new_move, board, x, y, wid, hei) and piece.has_never_moved() == \
                True:
            piece.add_move((x + new_move[0], y + new_move[1]))
    for new_move in [(x_pos, move[1]) for x_pos in [-1, 1]]:
        if piece.is_valid_move(new_move, board, x, y, wid, hei):
            piece.add_move((x + new_move[0], y + new_move[1]))

    # TODO ADD EN PASSANT HERE
    return  # Once this is finished check if this return is even needed


def generate_piece(team, piece, moves=[]):
    if piece == 'Pawn':
        return pawn(team)
    if piece == 'Knight':
        return knight(team, moves)
    if piece == 'King':
        return king(team, moves)
    if piece == 'Bishop':
        return bishop(team, moves)
    if piece == 'Rook':
        return rook(team, moves)
    if piece == 'Queen':
        return queen(team, moves)
    assert False, 'Invalid Piece Entered'


def pawn(team):
    if 'W' == team:
        pawn_moves = [(0, 1)]
    if 'B' == team:
        pawn_moves = [(0, -1)]
    return Piece(team + ' Pwn', pawn_moves, 'Pawn')


def knight(team, moves):
    return Piece(team + ' Kni', moves['Knight'], 'Knight')


def king(team, moves):
    return Piece(team + ' Kng', moves['King'], 'King')


def rook(team, moves):
    return Piece(team + 'Rook', moves['Rook'], 'Rook')


def bishop(team, moves):
    return Piece(team + ' Bis', moves['Bishop'], 'Bishop')


def queen(team, moves):
    return Piece(team + ' Que', moves['Queen'], 'Queen')


def generate_standard_moves():
    # Rook and Bishop are formatted so that each element is an array of moves that form a line
    # So when checking for valid moves, it iterates until a non legal move is found per direction.
    moves = {'Knight': [(x, y) for x in [-1, 1, -2, 2] for y in [-1, 1, -2, 2] if abs(x) != abs(y)],
             'King': [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if x != 0 or y != 0],
             'Rook': [[(x, 0) for x in range(1, 8)],
                      [(x, 0) for x in range(-1, -8, -1)],
                      [(0, y) for y in range(-1, -8, -1)],
                      [(0, y) for y in range(1, 8)]],
             'Bishop': [[(x, x) for x in range(-1, -8, -1)],
                        [(x, x) for x in range(1, 8)],
                        [(x, -x) for x in range(-1, -8, -1)],
                        [(x, -x) for x in range(1, 8)]]}
    moves['Queen'] = moves['Rook'] + moves['Bishop']
    return moves


def determine_castle_status(piece, board, y_pos, range, rook_pos):
    corner_piece = board.get_square(rook_pos, y_pos)
    # Checks that the king and rook are in valid positions and state to castle.
    if type(corner_piece) is not type(piece) or \
            corner_piece.get_type() is not 'Rook' or \
            corner_piece.has_never_moved() == False or \
            piece.has_never_moved() == False:
        return False
    for i in range:
        if type(board.get_square(i, y_pos)) is type(piece):
            return False
    return True


def castle(board, direction, king_location):
    # To call this function the king must be at position x = 4.
    y_level = king_location[1]
    if direction == 'L':
        shift = -2
        rook_x = 0
    else:
        shift = 2
        rook_x = 7
    board.move(4, y_level, 4 + shift, y_level)
    board.move(rook_x, y_level, 4 + (shift // 2), y_level)
