import chess
from ai_player import ai_move

board = chess.Board()
while not board.is_game_over():
    print(board)
    move = ai_move(board, "hard")
    print(f"AI chọn nước: {move}")
    board.push(move)
