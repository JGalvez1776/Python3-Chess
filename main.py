""" Author: Justin Galvez
    Name: main.py
    Description:
"""

from board import *
# TODO:
#   Make the while loop more user friendly to use (Catch errors, add back features, etc)
#   Implement pawn move up 2, castling on king, en passant, pawn promotion
#   Add checkmate to allow the game to end. (Requires adding check too)
#   Make a way to display the board using graphics
#

def main():
    board = create_standard_board()

    while True:
        board.print()
        action = input('Select Piece:\n')

        start = [int(x) for x in action.split()]
        piece = board.get_square(start[0], start[1])
        print(f'Selected Piece: {str(piece)}')
        print(f'Moves: {piece._valid_moves}')
        move = input('Select Move:\n')
        move = [int(x) for x in move.split()]
        board.move(start[0], start[1], move[0], move[1])


if __name__ == '__main__':
    main()
