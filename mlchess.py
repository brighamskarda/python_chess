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
    
    def get_depth(self) -> int:
        current_node = self
        depth = 0
        while current_node.parent != None:
            current_node = current_node.parent
            depth += 1
        return depth
        
    
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
    CHECK_DEPTH = 1
    NUM_BEST = 5
    NUM_LEAST_DEPTH = 20
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
            for child in self.root.children:
                if child.board.is_check():
                    if MLChess.__king_check_moves(child, MLChess.CHECK_DEPTH * (i + 1)):
                        self.root = ChessNode(child.board, None)
                        return self.root.board.peek()
                        
            # Evaluate best performing moves with a bias for moves of a smaller depth
            leaf_nodes = MLChess.__get_all_leaf_nodes(self.root)
            leaf_nodes.sort(key = lambda v: v.get_depth())
            # if self.root.board.turn == chess.WHITE:
            #     leaf_nodes.sort(key = lambda v: v.score + 10000 * v.get_depth())
            # if self.root.board.turn == chess.BLACK:
            #     leaf_nodes.sort(key = lambda v: v.score + 10000 * v.get_depth(), reverse=True)    
            for i in range(MLChess.NUM_LEAST_DEPTH):
                if i < len(leaf_nodes):
                    for move in leaf_nodes[i].board.legal_moves:
                        new_board = leaf_nodes[i].board.copy()
                        new_board.push(move)
                        new_node = ChessNode(new_board, leaf_nodes[i])
                        leaf_nodes[i].children.append(new_node)
                        
            # Evaluate all moves where a piece is taken
            leaf_nodes = MLChess.__get_all_leaf_nodes(self.root)
            for leaf in leaf_nodes:
                if leaf.takes_piece:
                    for move in leaf.board.legal_moves:
                        new_board = leaf.board.copy()
                        new_board.push(move)
                        new_node = ChessNode(new_board, leaf)
                        leaf.children.append(new_node)

        # Score each of the children
        scored_children = [(child, MLChess.__child_scoring(child)) for child in self.root.children]
        
        # Find and return best move
        best_position = None
        if self.root.board.turn == chess.WHITE:
            best_position = max(scored_children, key=lambda a: a[1])[0]
        if self.root.board.turn == chess.BLACK:
            best_position = min(scored_children, key=lambda a: a[1])[0]
        best_position.parent = None
        self.root = best_position
        return self.root.board.peek()
    
    def __initial_scoring(self):
        for m in self.root.board.legal_moves:
            new_board = self.root.board.copy()
            new_board.push(m)
            new_node = ChessNode(new_board, self.root)
            self.root.children.append(new_node)
    
    @staticmethod
    def __child_scoring(child: ChessNode) -> int:
        if len(child.children) == 0:
            return child.score
        scores = []
        for grandchild in child.children:
            scores.append(MLChess.__child_scoring(grandchild))
        if child.board.turn == chess.WHITE:
            return max(scores)
        if child.board.turn == chess.BLACK:
            return min(scores)
    
    @staticmethod
    def __king_check_moves(node: ChessNode, depth: int) -> bool:
        '''!
        @return True if forced checkmate is found
        '''
        if depth == 0:
            return False
        # Make all possible opponent moves
        for m in node.board.legal_moves:
            if not any(m == child.board.peek() for child in node.children):
                new_board = node.board.copy()
                new_board.push(m)
                new_node = ChessNode(new_board, node)
                node.children.append(new_node)
        
        # Make all of your possible moves after opponent moves
        forced_checkmate = True
        for child in node.children:
            for m in child.board.legal_moves:
                if not any(m == grandchild.board.peek() for grandchild in child.children):
                    new_board = child.board.copy()
                    new_board.push(m)
                    new_node = ChessNode(new_board, child)
                    child.children.append(new_node)
            # Continue the chain for grandchildren that put opponent in check
            forced_checkmate = False
            for grandchild in child.children:
                if grandchild.board.is_check() and not grandchild.board.is_checkmate():
                    if MLChess.__king_check_moves(grandchild, depth-1):
                        forced_checkmate = True
                        break
                if grandchild.board.is_checkmate():
                    forced_checkmate = True
                    break
            if not forced_checkmate:
                break
        return forced_checkmate
        
        
    
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