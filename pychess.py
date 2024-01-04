from mlchess import MLChess
import chess
import time

board = MLChess()

# board.root.board.set_board_fen('rnbqk2r/pppp1ppp/3b1n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R')
# board.root.board.turn = chess.BLACK

# board.computer_move_time()

# print(board.root.board)

while not board.root.board.is_checkmate():
    print()
    print(board.root.board)
    if board.root.board.turn == chess.WHITE:
        board.user_move(input('Enter Move: '))
    else:
        time_start = time.time()
        board.computer_move_time()
        print(f'Time Taken: {time.time() - time_start} seconds')

    