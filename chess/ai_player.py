import chess
import random

piece_value = {
    chess.PAWN: 1,
    chess.KNIGHT: 3.2,
    chess.BISHOP: 3.3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def evaluate_board(board):
    value = 0
    for piece_type in piece_value:
        value += len(board.pieces(piece_type, chess.WHITE)) * piece_value[piece_type]
        value -= len(board.pieces(piece_type, chess.BLACK)) * piece_value[piece_type]
    value += random.uniform(-0.05, 0.05)  # thêm chút randomness cho AI thông minh hơn
    return value

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None

    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def ai_move(board, level="easy"):
    if level == "random":
        return random.choice(list(board.legal_moves))
    elif level == "easy":
        _, move = minimax(board, 1, float('-inf'), float('inf'), board.turn)
        return move
    elif level == "medium":
        _, move = minimax(board, 2, float('-inf'), float('inf'), board.turn)
        return move
    elif level == "hard":
        _, move = minimax(board, 3, float('-inf'), float('inf'), board.turn)
        return move
    return random.choice(list(board.legal_moves))