""" Author: Justin Galvez
    Name: board.py
    Description:
"""


class Piece:
    def __init__(self, name, move_list, pawn=False):
        self._name = name
        self._moves = move_list
        self._team = name[0]
        self._position = None
        self._still = True
        self._valid_moves = []
        if pawn:

            x = 1

    def __str__(self):
        return self._name

    def update_position(self, x, y):
        self._position = (x, y)

    def get_moves(self):
        return self._moves

    def _reset_valid_moves(self):
        self._valid_moves = []

    def get_team(self):
        return self._team

    def add_move(self, move):
        self._valid_moves.append(move)

    def get_position(self):
        return self._position

    def find_moves(self, board, x, y):
        self._reset_valid_moves()
        wid = int(board.get_wid()) - 1
        hei = int(board.get_hei()) - 1

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
        # if 0 <= x + move[0] <= wid and 0 <= y + move[1] <= hei:
        if x + move[0] < 0 or x + move[0] > wid or y + move[1] < 0 or y + move[1] > hei:
            return False
        else:
            square = board.get_square(x + move[0], y + move[1])
            if str(self)[2:] == 'Pwn':
                if square is not None:
                    return False
                return True
            elif square is None:
                return True

            same_team = self.get_team() == square.get_team()
            if not same_team:
                self.add_move((x + move[0], y + move[1]))
                return False
            return not same_team


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
    return Piece(team + ' Pwn', pawn_moves, pawn=True)


def knight(team, moves):
    # print(f'MOVES: {moves["Knight"]}')
    return Piece(team + ' Kni', moves['Knight'])


def king(team, moves):
    return Piece(team + ' Kng', moves['King'])


def rook(team, moves):
    return Piece(team + 'Rook', moves['Rook'])


def bishop(team, moves):
    return Piece(team + ' Bis', moves['Bishop'])


def queen(team, moves):
    return Piece(team + ' Que', moves['Queen'])


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
