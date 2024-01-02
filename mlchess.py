import chess
import copy

class ChessNode:
    '''!
    This class will represent a single position within the MLChess tree. It needs parents and children
    upon instantiation. (Its children can just be an empty list.)
    '''
    __center_pieces = [chess.D4, chess.E4, chess.D5, chess.E5]
    def __init__(self, board: chess.Board, parent: 'ChessNode'):
        self.board = board
        self.score = ChessNode.__score_board(board)
        self.takes_piece = ChessNode.__takes_piece(board)
        self.parent = parent
        self.children: list[ChessNode] = []
        
    
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
        if len(board.move_stack) == 0:
            return False
        move = board.pop()
        if board.piece_at(move.to_square) != None:
            board.push(move)
            return True
        if (board.piece_at(move.from_square) == chess.PAWN and
            chess.square_file(move.from_square) != chess.square_file(move.to_square)):
            board.push(move)
            return True
        board.push(move)
        return False
        

class MLChess:
    '''!
    This class will find the best move for the computer to make, and then make it. It also accepts
    user input for moves.
    '''
    CHECK_DEPTH = 2
    NUM_BEST = 5
    NUM_LEAST_DEPTH = 5
    def __init__(self, board: chess.Board = chess.Board()):
        self.root = ChessNode(board, None)
        
    def user_move(self, move: str) -> bool:
        '''!
        @return True if the move was valid and successful. Otherwise false.
        '''
        new_board = self.root.board.copy()
        try:
            new_board.push_uci(move)
        except:
            return False
        self.root = ChessNode(new_board, None)
        return True
    
    def computer_move_tick(self, ticks: int = 3) -> chess.Move:
        '''!
        The computer makes a move, and returns the move in case you want to see what it was.
        '''
        if self.root.board.is_checkmate():
            print('No possible moves')
            return
        
        self.__initial_scoring()
        
        # King Checks
        for i in range(ticks):
            print(f'Working on tick {i+1}/{ticks}')
            # Evaluate moves that put king in check
            leaf_nodes = MLChess.__get_all_leaf_nodes(self.root)
            for leaf in leaf_nodes:
                if leaf.board.is_check():
                    MLChess.__king_check_moves(leaf, MLChess.CHECK_DEPTH - 1)

            # Evaluate all moves where a piece is taken
            leaf_nodes = MLChess.__get_all_leaf_nodes(self.root)
            for leaf in leaf_nodes:
                if leaf.takes_piece:
                    for move in leaf.board.legal_moves:
                        new_board = leaf.board.copy()
                        new_board.push(move)
                        new_node = ChessNode(new_board, leaf)
                        leaf.children.append(new_node)
            
            # Evaluate best performing moves
            leaf_nodes = MLChess.__get_all_leaf_nodes(self.root).sort(key = lambda v: v.score)
            for i in range(MLChess.NUM_BEST):
                for move in leaf.board.legal_moves:
                    new_board = leaf.board.copy()
                    new_board.push(move)
                    new_node = ChessNode(new_board, leaf)
                    leaf.children.append(new_node)
        
        # If any move is checkmate, take that move.
        for child in self.root.children:
            leaf_nodes = MLChess.__get_all_leaf_nodes(child)
            is_checkmate = True
            for leaf in leaf_nodes:
                if not leaf.board.is_checkmate() or leaf.board.turn == self.root.turn:
                    is_checkmate = False
                    break
            if is_checkmate:
                self.root = ChessNode(child.board, None)
                return self.root.board.peek()
        
        # Find and return best move
        best_position = self.root.children[0]
        for child in self.root.children:
            if self.root.board.turn == chess.WHITE and child.score > best_position.score:
                best_position = child
            elif self.root.board.turn == chess.BLACK and child.score < best_position.score:
                best_position = child
        self.root = ChessNode(best_position.board, None)
        return self.root.board.peek()
    
    def __initial_scoring(self):
        for m in self.root.board.legal_moves:
            new_board = self.root.board.copy()
            new_board.push(m)
            new_node = ChessNode(new_board, self.root)
            self.root.children.append(new_node)
    
    @staticmethod
    def __king_check_moves(node: ChessNode, depth: int):
        if depth == 0:
            return
        # Make all possible opponent moves
        for m in node.board.legal_moves:
            new_board = node.board.copy()
            new_board.push(m)
            new_node = ChessNode(new_board, node)
            node.children.append(new_node)
            # Make all moves that put opponent in check again
            for m2 in new_board.legal_moves:
                new_board2 = new_board.copy()
                new_board2.push(m2)
                if new_board2.is_check():
                    new_node2 = ChessNode(new_board2, new_node)
                    new_node.children.append(new_node2)
                    MLChess.__king_check_moves(new_node2, depth - 1)
        
        
    
    @staticmethod
    def __get_all_leaf_nodes(node: ChessNode) -> list[ChessNode]:
        if len(node.children) == 0:
            return [node]
        return_list = []
        for n in node.children:
            for n2 in MLChess.__get_all_leaf_nodes(n):
                return_list.append(n2)
        return return_list
        
        
    @staticmethod
    def __get_average_leaf_node_score(node: ChessNode) -> int:
        if len(node.children) == 0:
            return node.score
        total_score = 0
        for n in node.children:
            total_score += MLChess.__get_average_leaf_node_score(n)
        return total_score / len(node.children)