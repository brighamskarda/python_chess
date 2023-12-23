import mlchess
import chess

cb = chess.Board()

while not cb.is_checkmate():
    print(cb.unicode(borders=True))
    if cb.turn == chess.WHITE:
        user_input = input('Enter Move: ')
        try:
            cb.push_uci(user_input)
        except Exception:
            continue
    else:
        cb.push(mlchess.compute_best_move(cb, depth=4))

