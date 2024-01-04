from mlchess import MLChess
import chess

board = MLChess()

# board.root.board.set_board_fen('rnbqkbnr/ppp2ppp/8/4N3/2B1p3/8/PPPP1PPP/RNBQK2R')
# board.root.board.turn = chess.BLACK

# board.computer_move_tick(4)

# print(board.root.board)

while not board.root.board.is_checkmate():
    print()
    print(board.root.board)
    if board.root.board.turn == chess.WHITE:
        board.user_move(input('Enter Move: '))
    else:
        board.computer_move_tick(5)

    