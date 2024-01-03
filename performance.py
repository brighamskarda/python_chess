from mlchess import MLChess
import time

board = MLChess()
move_times = []
i = 0
while not board.root.board.is_checkmate() and not board.root.board.is_stalemate() and not board.root.board.can_claim_draw():
    print(board.root.board)
    time1 = time.time_ns()
    board.computer_move_tick(4)
    time2 = time.time_ns()
    move_times.append((time2 - time1) / 1_000_000)

print()
print('Average Move Time (seconds):', (sum(move_times) / len(move_times)) / 1000)
