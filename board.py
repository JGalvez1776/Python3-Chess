""" Author: Justin Galvez
    Name: board.py
    Description: 
"""

from piece import *


class Board:
    def __init__(self, wid, hei):
        self._board = [''] * hei
        self._wid = wid
        self._hei = hei
        for i in range(wid):
            self._board[i] = [None] * wid
        # Check if the kings location is even being used.
        self._kings_locations = None

    def copy(self):
        board = self.get_board()
        new_board = Board(self.get_wid(), self.get_hei())
        for y in range(len(board)):
            for x in range(len(board[y])):
                new_board._board[y][x] = board[y][x]
        return new_board

    def print(self):
        board = self.get_board()
        height = self.get_hei()
        wid = self.get_wid()
        length = len(board) * 6 + 1
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'[0:wid]
        print()
        print('  ' + '-' * length)
        for row in board:
            print(f'{height} |', end='')
            for square in row:
                if square is None:
                    print('     ', end='|')
                else:
                    print(str(square), end='|')
            print()
            print('  ' + '-' * length)
            height -= 1
        print('   ', end='')
        for letter in letters:
            print(f'  {letter}   ', end='')
        print()

    def place(self, piece, x, y):
        if piece is not None:
            piece.update_position(x, y)
        self._board[row(y)][x] = piece

    def move(self, x1, y1, x2, y2):
        '''
        Assumes that a move is valid given coordinates
        '''
        piece = self.get_square(x1, y1)
        self.place(piece, x2, y2)
        self.place(None, x1, y1)
        piece.update_move_status()

    def raw_move(self, start, end):
        piece = self.get_square(start[0], start[1])

        self._board[row(start[1])][start[0]] = None
        self._board[row(end[1])][end[0]] = piece

    def get_square(self, x, y):
        return self._board[row(y)][x]

    def get_board(self):
        return self._board

    def get_wid(self):
        return self._wid

    def get_hei(self):
        return self._hei

    def fill_row(self, team, piece, y):
        board = self.get_board()
        old_y = y
        y = row(y)
        for i in range(len(board[y])):
            pawn = generate_piece(team, piece, 'Pawn')
            board[y][i] = pawn
            pawn.update_position(i, old_y)

    def find_all_moves(self, team):
        board = self.get_board()
        for row in board:
            for square in row:
                if square is None or square.get_team() != team:
                    continue
                pos = square.get_position()
                square.find_moves(self, pos[0], pos[1])

    def update_kings_locations(self):
        board = self.get_board()
        locations = []
        for y in range(0, self.get_hei()):
            for x in range(0, self.get_wid()):
                if board[y][x] is not None and board[y][x].get_type() == 'King':
                    locations.append((x, y))
        self.set_kings_locations(locations)

    def check_en_pasante(self, old_piece, start, move):
        if old_piece is None or old_piece.get_type() in ['King', 'Queen', 'Rook', 'Bishop',
                                                         'Knight']:
            return
        if (move[1] - start[1]) % 2 == 0:
            items = [(-1, 0), (1, 0)]
            for elem in items:
                piece = self.get_square(move[0] + elem[0], move[1] + elem[1])
                if piece is None or \
                        piece.get_type() in ['King', 'Queen', 'Rook', 'Bishop', 'Knight']:
                    continue
                if piece.get_team() != old_piece.get_team():
                    new_move = generate_en_pasante_move(self, old_piece, piece)
                    piece.add_special_moves(new_move)

    def set_kings_locations(self, val):
        self._kings_locations = val

    def get_kings_locations(self):
        return self._kings_locations

    def get_piece(self, type, team):
        board = self.get_board()
        for y in range(len(board)):
            for x in range(len(board[y])):
                piece = board[y][x]
                if piece is None:
                    continue
                if piece.get_type() == type and piece.get_team() == team:
                    return piece
        assert False, 'Piece is not found'


def generate_en_pasante_move(board, old_piece, piece):
    piece_team = piece.get_team()
    if piece_team == 'W':
        change = 1
    else:
        change = -1
    old_location = old_piece.get_position()
    location = piece.get_position()
    new_location = (old_location[0], location[1] + change)
    return new_location


def row(y):
    # Exists since my code is jank
    return -(y + 1)


def create_standard_board():
    board = Board(8, 8)
    moves = generate_standard_moves()
    # return test_board(board, moves)
    board.fill_row('B', 'Pawn', 6)
    board.place(generate_piece('B', 'Rook', moves), 0, 7)
    board.place(generate_piece('B', 'Knight', moves), 1, 7)
    board.place(generate_piece('B', 'Bishop', moves), 2, 7)
    board.place(generate_piece('B', 'Queen', moves), 3, 7)
    board.place(generate_piece('B', 'King', moves), 4, 7)
    board.place(generate_piece('B', 'Bishop', moves), 5, 7)
    board.place(generate_piece('B', 'Knight', moves), 6, 7)
    board.place(generate_piece('B', 'Rook', moves), 7, 7)

    board.fill_row('W', 'Pawn', 1)
    board.place(generate_piece('W', 'Rook', moves), 0, 0)
    board.place(generate_piece('W', 'Knight', moves), 1, 0)
    board.place(generate_piece('W', 'Bishop', moves), 2, 0)
    board.place(generate_piece('W', 'Queen', moves), 3, 0)
    board.place(generate_piece('W', 'King', moves), 4, 0)
    board.place(generate_piece('W', 'Bishop', moves), 5, 0)
    board.place(generate_piece('W', 'Knight', moves), 6, 0)
    board.place(generate_piece('W', 'Rook', moves), 7, 0)

    board.find_all_moves('W')
    return board


def test_board(board, moves):
    '''
    This is purely for debugging remove once project is finished
    '''
    board.place(generate_piece('B', 'King', moves), 4, 7)
    board.place(generate_piece('W', 'King', moves), 4, 0)
    board.place(generate_piece('W', 'Queen', moves), 3, 0)
    board.place(generate_piece('W', 'Pawn', moves), 4, 1)
    board.find_all_moves()

    return board
