import mlchess
import chess

if __name__ == '__main__':
    cb = chess.Board()
    # cb.set_board_fen('rnbqkb1r/pppppppp/5n2/4P3/8/8/PPPP1PPP/RNBQKBNR')
    # cb.turn = chess.BLACK
    while not cb.is_checkmate():
        print(cb.unicode(borders=True))
        if cb.turn == chess.WHITE:
            user_input = input('Enter Move: ')
            try:
                cb.push_uci(user_input)
            except Exception:
                continue
        else:
            cb.push(mlchess.compute_best_move(cb, depth=9, cores=100))

