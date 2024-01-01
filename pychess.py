from mlchess import ChessNode
import timeit
import chess

# myChess = MLChess()
stp = '''
from mlchess import ChessNode
import chess
board = chess.Board('rn2kbn1/pppqppp1/3p4/7r/4P2p/2N5/PPPP1PPP/R1BQKB1R')
'''
print(timeit.timeit(stmt='ChessNode._ChessNode__score_board(board)', setup=stp,number=100_000)/100_000)
