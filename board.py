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

    def place(self, piece, x, y):
        if piece is not None:
            piece.update_position(x, y)
        self._board[row(y)][x] = piece

    def print(self):
        length = len(self.get_board()) * 6 + 1
        print('-' * length)
        for row in self.get_board():
            print('|', end='')
            for square in row:
                if square is None:
                    print('     ', end='|')
                else:
                    print(str(square), end='|')
            print()
            print('-' * length)

    def move(self, x1, y1, x2, y2):
        '''
        This assumes that a move is valid
        '''
        piece = self.get_square(x1, y1)
        self.place(piece, x2, y2)
        self.place(None, x1, y1)
        #piece.find_moves(self, x2, y2)
        self.find_all_moves()


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
            pawn = generate_piece(team, piece)
            board[y][i] = pawn
            pawn.update_position(i, old_y)

    def find_all_moves(self):
        board = self.get_board()
        for row in board:
            for square in row:
                if square is None:
                    continue
                pos = square.get_position()
                square.find_moves(self, pos[0], pos[1])


def row(y):
    return -(y + 1)


def create_standard_board():
    board = Board(8, 8)
    moves = generate_standard_moves()
    board.fill_row('B', 'Pawn', 6)
    board.place(generate_piece('B', 'Rook', moves), 0, 7)
    board.place(generate_piece('B', 'Rook', moves), 7, 7)
    board.place(generate_piece('B', 'Knight', moves), 1, 7)
    board.place(generate_piece('B', 'Knight', moves), 6, 7)
    board.place(generate_piece('B', 'Bishop', moves), 2, 7)
    board.place(generate_piece('B', 'Bishop', moves), 5, 7)
    board.place(generate_piece('B', 'Queen', moves), 3, 7)
    board.place(generate_piece('B', 'King', moves), 4, 7)

    board.fill_row('W', 'Pawn', 1)
    board.place(generate_piece('W', 'Rook', moves), 0, 0)
    board.place(generate_piece('W', 'Rook', moves), 7, 0)
    board.place(generate_piece('W', 'Knight', moves), 1, 0)
    board.place(generate_piece('W', 'Knight', moves), 6, 0)
    board.place(generate_piece('W', 'Bishop', moves), 2, 0)
    board.place(generate_piece('W', 'Bishop', moves), 5, 0)
    board.place(generate_piece('W', 'Queen', moves), 3, 0)
    board.place(generate_piece('W', 'King', moves), 4, 0)
    board.find_all_moves()
    return board
