""" Author: Justin Galvez
    Name: main.py
    Description:
"""

from board import *


# TODO:
#   Make the while loop more user friendly to use (Add "back", "help", etc)
#   Add checkmate to allow the game to end. (Requires adding check too)
#   Make a way to display the board using graphics


def main():
    board = create_standard_board()
    column_string = 'abcdefghijklmnopqrstuvwxyz'[:board.get_wid()]
    numbers = range(1, board.get_hei() + 1)
    team = 'White'
    kings = [board.get_square(4, 0), board.get_square(4, 7)]
    while True:
        for piece in kings:
            piece.determine_check(board)
            if piece.get_check_status():
                print('CHECK')

        print(f'Current Player: {team}')
        board.print()
        action = input('Select Piece:\n')
        if action == "exit":
            break
        # Checks for potential errors in the input
        if find_error(action, column_string, numbers, board):
            continue

        start = (column_string.index(action[0]), int(action[1]) - 1)
        piece = board.get_square(start[0], start[1])
        if piece is None:
            display_error('No Piece is selected')
            continue
        if piece.get_team() is not team[0]:
            display_error("You don't own this piece.")
            continue

        valid_move = piece.get_valid_moves()

        print(f'Selected Piece: {str(piece)}')
        print(f'Moves: '
              f'{[f"{column_string[move[0]].upper()}{move[1] + 1}" for move in valid_move]}')

        move = input('Select Move:\n')
        if action == "exit":
            break
        if find_error(move, column_string, numbers, board):
            continue

        move = (int(column_string.index(move[0])), int(move[1]) - 1)

        if move not in piece.get_valid_moves():
            display_error('Invalid Move')
            continue

        handle_move(board, piece, start, move)
        board.update_kings_locations()
        if team == 'White':
            team = 'Black'
        else:
            team = 'White'


def find_error(data, column_string, numbers, board):
    if len(data) != 2:
        display_error('Enter only 2 characters')
        return True
    if data[0].isalpha() == False or data[0].lower() not in column_string:
        display_error(f'The first character needs be a letter among \'{column_string}\'')
        return True
    if data[1].isnumeric() == False or int(data[1]) not in numbers:
        display_error(
            f'The second character needs to be an integer between 1 and {board.get_hei()}')
        return True
    return False


def display_error(msg):
    print('-' * 20)
    print('Error:')
    print(msg)
    print('-' * 20)






if __name__ == '__main__':
    main()
