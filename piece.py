""" Author: Justin Galvez
    Name: piece.py
    Description:
"""

from utils import *


class Piece:
    def __init__(self, name, move_list, type):
        self._name = name
        self._moves = move_list
        self._team = name[0]
        self._position = None
        self._valid_moves = []
        self._type = type
        if type in ['Pawn', 'Rook', 'King']:
            self._never_moved = True
            if type == 'Pawn':
                self._special_moves = []
            elif type == 'King':
                self._in_check = False
                self._vision = create_vision()

    def __str__(self):
        return self._name

    def update_position(self, x, y):
        self._position = (x, y)

    def reset_special_moves(self):
        '''
        special_moves is where en passante moves gets stored.
        '''
        if self.get_type() != 'Pawn':
            return
        self._special_moves = []

    def get_special_moves(self):
        if self.get_type() != 'Pawn':
            return False
        return self._special_moves

    def add_special_moves(self, move):
        if self.get_type() != 'Pawn':
            return
        self._special_moves.append(move)

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

    # ADD MOVE WAS ORIGINALLY HERE

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
                # Here I want to implement code to prevent the move from being added if the king
                # moves over check or into check.
                self.add_move(move, board)

        for move in self.get_moves():
            if type(move) == list:
                for elem in move:
                    if self.is_valid_move(elem, board, x, y, wid, hei):
                        self.add_move((x + elem[0], y + elem[1]), board)
                    else:
                        break
            elif self.is_valid_move(move, board, x, y, wid, hei):
                self.add_move((x + move[0], y + move[1]), board)

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
                self.add_move((x + move[0], y + move[1]), board)
                return False
            return not same_team

    def get_check_status(self):
        return self._in_check

    def handle_check(self, board):
        if self.get_type() != 'King':
            print('A non king was used')
            return
        status = self.determine_check(board)
        self.change_check_status(status)

    def determine_check(self, board):
        vision = self.get_vision()
        location = self.get_position()
        check_pieces = ['Rook Queen', 'Bishop Queen', 'Knight']
        i = 0
        index = 0
        dimensions = [board.get_wid() - 1, board.get_hei() - 1]

        #if determine_pawn_check(board, self, location):
        #    return True

        for move_set in vision:
            cur_piece = check_pieces[index]
            if type(move_set) == list:
                for move in move_set:
                    status = determine_if_checks(board, self, location, move, cur_piece, dimensions)
                    if status:
                        return True
                    if status is None:
                        continue
                    break
            else:
                assert type(move_set) == tuple, 'The type is not a tuple'
                status = determine_if_checks(board, self, location, move_set, cur_piece, dimensions)
                if status:
                    return True
            i += 1
            if i % 4 == 0 and index < 2:
                index += 1
        return False

    def change_check_status(self, data):
        self._in_check = data

    def get_vision(self):
        return self._vision

    def add_move(self, move, board):
        '''
        Checks that a move does not check oneself before adding it to a pieces legal moves
        '''
        if determine_if_self_checks(board, self, move):
            return
        self._valid_moves.append(move)

# If pawn checks don't work
#def determine_pawn_check(board, piece, location):
#    team = piece.get_team()


def determine_if_self_checks(board, piece, move):
    new_board = board.copy()
    location = piece.get_position()
    team = piece.get_team()[0]

    if piece.get_type() == 'King':
        shadow_king = empty_king(team)
        new_board.place(shadow_king, location[0], location[1])

        new_board.raw_move(location, move)

        shadow_king.update_position(move[0], move[1])

        status = shadow_king.determine_check(new_board)
        return status

    new_board.raw_move(location, move)
    king = board.get_piece('King', team)
    status = king.determine_check(new_board)


    return status


def determine_if_checks(board, king, king_location, move, required_type, dimensions):
    x = king_location[0]
    y = king_location[1]
    wid = dimensions[0]
    hei = dimensions[1]

    if x + move[0] < 0 or x + move[0] > wid or y + move[1] < 0 or y + move[1] > hei:
        return False
    piece = board.get_square(x + move[0], y + move[1])
    team = king.get_team()
    if team == 'W' and abs(move[0]) == 1 and move[1] == 1:
        required_type += ' Pawn'
    if team == 'B' and abs(move[0]) == 1 and move[1] == -1:
        required_type += ' Pawn'
    if piece is None:
        return None
    return piece.get_type() in required_type and piece.get_team() != team


def check_pawn_moves(board, piece, x, y, wid, hei):
    move = piece.get_moves()[0]
    if piece.is_valid_move(move, board, x, y, wid, hei):
        piece.add_move((x + move[0], y + move[1]), board)
        new_move = (move[0], move[1] * 2)
        if piece.is_valid_move(new_move, board, x, y, wid, hei) and piece.has_never_moved() == \
                True:
            piece.add_move((x + new_move[0], y + new_move[1]), board)
    for new_move in [(x_pos, move[1]) for x_pos in [-1, 1]]:
        if piece.is_valid_move(new_move, board, x, y, wid, hei):
            piece.add_move((x + new_move[0], y + new_move[1]), board)
    for move in piece.get_special_moves():
        piece.add_move(move, board)
    return  # TODO: Once this is finished check if this return is even needed


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


def empty_king(team):
    # TODO: When done see if the move list can just be blank
    return Piece(team + ' Kng', [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if x != 0 or y != 0], 'King')


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


def create_vision():
    vision = [[(x, 0) for x in range(1, 8)],
              [(x, 0) for x in range(-1, -8, -1)],
              [(0, y) for y in range(-1, -8, -1)],
              [(0, y) for y in range(1, 8)]] + \
             [[(x, x) for x in range(-1, -8, -1)],
              [(x, x) for x in range(1, 8)],
              [(x, -x) for x in range(-1, -8, -1)],
              [(x, -x) for x in range(1, 8)]] + \
             [(x, y) for x in [-1, 1, -2, 2] for y in [-1, 1, -2, 2] if abs(x) != abs(y)]
    return vision
