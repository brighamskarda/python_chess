from mlchess import MLChess
import chess

board = MLChess()

while not board.root.board.is_checkmate():
    print()
    print(board.root.board)
    if board.root.board.turn == chess.WHITE:
        board.user_move(input('Enter Move: '))
    else:
        board.computer_move_tick(4)

    