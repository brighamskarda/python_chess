from mlchess import MLChess
import chess
import time

board = MLChess()

inp = input('Would you like to play white or black? (W or B): ')
user_color = None
match inp:
    case 'W':
        user_color = chess.WHITE
    case 'B':
        user_color = chess.BLACK
    case _:
        print('Invalid option selected defaulting player to white.')
        

while not board.root.board.is_checkmate():
    print()
    print(board.root.board)
    if board.root.board.turn == user_color:
        board.user_move(input('Enter Move: '))
    else:
        time_start = time.time()
        board.computer_move_time()
        print(f'Time Taken: {time.time() - time_start} seconds')

    