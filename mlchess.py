import chess
import math


        


class ChessNode:
    '''!
    This class will represent a single position within the MLChess tree. It needs parents and children
    upon instantiation. (Its children can just be an empty list.)
    '''
    __center_pieces = [chess.D4, chess.E4, chess.D5, chess.E5]
    def __init__(self, board: chess.Board, parent: 'ChessNode', children: ['ChessNode']):
        self.board = board
        self.score = ChessNode.__score_board(board)
        self.takes_piece = ChessNode.__takes_piece(board)
        self.parent = parent
        self.children = children
        
    
    @staticmethod
    def __score_board(board: chess.Board) -> int:
        # Check for checkmate
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return -1200
            elif board.turn == chess.BLACK:
                return 1200
        
        score = 0
        # How far forward pawns are advanced
        for square in board.pieces(chess.PAWN, chess.WHITE):
            score += ChessNode.__pawn_advance_score(square, chess.WHITE)
        for square in board.pieces(chess.PAWN, chess.BLACK):
            score += ChessNode.__pawn_advance_score(square, chess.BLACK)
        
        # How close pieces are to the center, and Material Difference
        for piece_type in chess.PIECE_TYPES[:5]:
            for color in chess.COLORS:
                for square in board.pieces(piece_type, color):
                    piece_score = 0
                    match piece_type:
                        case chess.PAWN:
                            piece_score = 100
                        case chess.ROOK:
                            piece_score = 500
                        case chess.KNIGHT:
                            piece_score = 280
                        case chess.BISHOP:
                            piece_score = 300
                        case chess.QUEEN:
                            piece_score = 800
                    if color == chess.WHITE:
                        score -= 2 * min([chess.square_distance(square, s) for s in ChessNode.__center_pieces])
                        score += piece_score
                    elif color == chess.BLACK:
                        score += 2 * min([chess.square_distance(square, s) for s in ChessNode.__center_pieces])
                        score -= piece_score
        
        # If there is a check
        if board.is_check():
            if board.turn == chess.WHITE:
                score -= 50
            elif board.turn == chess.BLACK:
                score += 50
        return score
    
    @staticmethod
    def __pawn_advance_score(square: chess.Square, color: chess.Color) -> int:
        if color == chess.WHITE:
            return chess.square_rank(square)
        elif color == chess.BLACK:
            return -9 + chess.square_rank(square)
        else:
            return 0
    
    @staticmethod
    def __takes_piece(board: chess.Board) -> bool:
        move = board.pop()
        if board.piece_at(move.to_square) != None:
            board.push(move)
            return True
        if (board.piece_at(move.from_square) == chess.PAWN and
            chess.square_file(move.from_square) != chess.square_file(move.to_square)):
            board.push(move)
            return True
        return False
        

class MLChess:
    CHECK_DEPTH = 3
    NUM_BEST = 5
    NUM_LEAST_DEPTH = 5
    def __init__(self, board: chess.Board = chess.Board()):
        self.root = ChessNode(board, None, [])
    
    def __get_average_leaf_node_score(node: ChessNode):
    