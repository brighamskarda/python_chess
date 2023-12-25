import chess
import math
import multiprocessing
import time

def distance_from_center(square: chess.Square) -> int:
    x = 0
    y = 0
    match chess.square_file(square):
        case 0: x = 3
        case 1: x = 2
        case 2: x = 1
        case 5: x = 1
        case 6: x = 2
        case 7: x = 3
    match chess.square_rank(square):
        case 0: y = 3
        case 1: y = 2
        case 2: y = 1
        case 5: y = 1
        case 6: y = 2
        case 7: y = 3
    return int(math.sqrt(x**2 + y**2))

def all_piece_distance(b: chess.Board, side: chess.Color) -> int:
    total_dis = 0
    for s in chess.SQUARES:
        if b.piece_at(s) != None and b.piece_at(s).color == side:
            total_dis = total_dis + distance_from_center(s)
    return total_dis

def position_score(board: chess.Board) -> int:
    score = 0
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -1200
        else:
            return 1200
    # Count up piece values
    for s in chess.SQUARES:
        match board.piece_type_at(s):
            case chess.PAWN:
                if board.color_at(s) == chess.WHITE:
                    score = score + 100
                else:
                    score = score - 100
            case chess.KNIGHT:
                if board.color_at(s) == chess.WHITE:
                    score = score + 280
                else:
                    score = score - 280
            case chess.BISHOP:
                if board.color_at(s) == chess.WHITE:
                    score = score + 320
                else:
                    score = score - 320
            case chess.ROOK:
                if board.color_at(s) == chess.WHITE:
                    score = score + 500
                else:
                    score = score - 500
            case chess.QUEEN:
                if board.color_at(s) == chess.WHITE:
                    score = score + 900
                else:
                    score = score - 900
            case chess.KING:
                if board.color_at(s) == chess.WHITE:
                    score += distance_from_center(s)
                else:
                    score -= distance_from_center(s)
 
    score -= all_piece_distance(board, chess.WHITE)
    score += all_piece_distance(board, chess.BLACK)
    if board.is_check:
        if board.turn == chess.WHITE:
            score -= 150
        else:
            score += 150
    
    return score

def compute_best_move_depth(board: chess.Board, depth: int, position_scores: list[int], side: chess.Color):
    if depth > 0:
        temp_scores = []
        for m in board.legal_moves:
            board.push(m)
            temp_scores.append([m, position_score(board)])
            board.pop()
        if board.turn != side:
            temp_scores.sort(key=lambda e: e[1])
        else:
            temp_scores.sort(key=lambda e: e[1], reverse=True)
        if len(temp_scores) >= math.ceil(depth / 2):
            for m in range(math.ceil(depth / 2)):
                board.push(temp_scores[m][0])
                if depth ==  1 or board.is_checkmate():
                    position_scores.append(temp_scores[m][1])
                elif not board.is_checkmate():
                    compute_best_move_depth(board, depth-1, position_scores, side)
                board.pop()
        else:
            for m in range(len(temp_scores)):
                board.push(temp_scores[m][0])
                if depth == 1 or board.is_checkmate():
                    position_scores.append(temp_scores[m][1])
                elif not board.is_checkmate():
                    compute_best_move_depth(board, depth-1, position_scores, side)
                board.pop()

    
    

def compute_best_move(board: chess.Board, depth: int = 3, cores: int = 1) -> chess.Move:
    manager = multiprocessing.Manager()
    moves = []
    processes = []
    k = 0
    for m in board.legal_moves:
        board.push(m)
        moves.append([m, manager.list([])])
        if not board.is_checkmate():
            p = multiprocessing.Process(target=compute_best_move_depth, args=(board, depth-1, moves[-1][1], board.turn))
            processes.append(p)
            p.start()
        board.pop()
        if len(processes) == cores:
            processes[0].join()
            k = k + 1
            print(f'{k}/{board.legal_moves.count()} moves analyzed')
            processes = processes[1:]
    for p in processes:
        p.join()
        k = k + 1
        print(f'{k}/{board.legal_moves.count()} moves analyzed')

    best_move = [0, -1_000_000]
    if board.turn == chess.BLACK:
        best_move = [0, 1_000_000]
    for m in moves:
        if board.turn == chess.WHITE:
            if sum(m[1])/len(m[1]) > best_move[1]:
                best_move = [m[0], sum(m[1])/len(m[1])]
        if board.turn == chess.BLACK:
            if sum(m[1])/len(m[1]) < best_move[1]:
                best_move = [m[0], sum(m[1])/len(m[1])]
    return best_move[0]
