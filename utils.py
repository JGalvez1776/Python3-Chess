def handle_move(board, piece, start, move, team):
    # Handles castling
    if piece.get_type() == 'King' and \
            (int(move[0]) == piece.get_position()[0] - 2 or
             int(move[0]) == piece.get_position()[0] + 2):
        if move[0] == 2:
            direction = 'L'
        else:
            direction = 'R'
        castle(board, direction, piece.get_position())
        return
    handle_special_moves(board, piece, start, move)
    board.move(start[0], start[1], move[0], move[1])
    # Checks if a pawn is being promoted
    if piece.get_type() == 'Pawn' and piece.get_position()[1] in [0, 7]:
        print('Choose which piece to promote the pawn to')
        print('Queen, Rook, Bishop, Knight')
        while True:
            choice = input()
            if choice in ['Queen', 'Rook', 'Bishop', 'Knight']:
                print(f'Promoting pawn to {choice}')
                team = piece.get_team()[0]
                pos = piece.get_position()
                piece = generate_piece(team, choice, generate_standard_moves())
                board.place(piece, pos[0], pos[1])
                break
            else:
                print('Only input one from "Queen", "Rook", "Bishop", or "Knight"')
    board.check_en_pasante(piece, start, move)
    board.find_all_moves(team[0])
    piece.reset_special_moves()
    return


def handle_special_moves(board, piece, start, move):
    if piece.get_type() != 'Pawn' or start[0] == move[0]:
        return
    if piece.get_team() == 'W':
        change = -1
    else:
        change = 1
    print('Here is en pasante info')
    print((move[0], move[1] + change))
    captured_piece = board.get_square(move[0], move[1] + change)
    empty_piece = board.get_square(move[0], move[1])
    print(f'Captured: {captured_piece} Empty: {empty_piece}')
    if empty_piece is not None or captured_piece.get_type() != 'Pawn':
        return
    board.place(None, move[0], move[1] + change)
