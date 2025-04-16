import pygame
import chess
from ai_player import ai_move
from network import NetworkServer, NetworkClient
import socket
import threading
import queue
WIDTH, HEIGHT = 640, 720
def draw_board(screen, board, images, selected_square=None):
    colors = [(235, 236, 208), (119, 149, 86)]
    highlight = (186, 202, 68)
    for r in range(8):
        for c in range(8):
            square = (7 - r) * 8 + c
            if selected_square is not None and square in [m.to_square for m in board.legal_moves if m.from_square == selected_square]:
                pygame.draw.rect(screen, highlight, pygame.Rect(c*80, r*80, 80, 80))
            else:
                color = colors[(r + c) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(c*80, r*80, 80, 80))

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - square // 8
            col = square % 8
            key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
            screen.blit(images[key], pygame.Rect(col*80, row*80, 80, 80))

def load_images():
    pieces = ["P", "N", "B", "R", "Q", "K"]
    colors = ["w", "b"]
    images = {}
    for color in colors:
        for piece in pieces:
            name = color + piece
            images[name] = pygame.transform.scale(pygame.image.load(f"assets/pieces/{name}.png"), (80, 80))
    return images

def save_game(board):
    with open("save_game.txt", "w") as f:
        f.write(board.fen())

def load_game():
    with open("save_game.txt", "r") as f:
        return chess.Board(f.read())

def pause_menu(screen):
    font = pygame.font.SysFont("Arial", 28)
    options = ["Continue", "Save and return menu", "Restart"]
    selected = 0
    while True:
        screen.fill((40, 40, 40))
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected else (180, 180, 180)
            text = font.render(option, True, color)
            screen.blit(text, (180, 220 + i * 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return "continue"
                    elif selected == 1:
                        return "save_exit"
                    elif selected == 2:
                        return "restart"

def display_message(screen, message):
    font = pygame.font.SysFont("Arial", 36, bold=True)
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (320 - text.get_width() // 2, 660))

def start_game(vs_ai=True, load_saved_game=False, network=False, ai_level="medium"):
    pygame.init()
    screen = pygame.display.set_mode((640, 720))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()

    board = load_game() if load_saved_game else chess.Board()
    images = load_images()
    selected_square = None
    status_message = ""

    if network == "host":
        net = NetworkServer()
        player_color = chess.WHITE
    elif network == "join":
        net = NetworkClient()
        player_color = chess.BLACK
    else:
        net = None
        player_color = chess.WHITE

    running = True
    connection_lost = False
    move_queue = queue.Queue()

    def receive_loop():
        while True:
            try:
                move = net.receive_move()
                move_queue.put(move)
            except (ConnectionResetError, socket.error):
                move_queue.put("__DISCONNECT__")
                break

    if net:
        threading.Thread(target=receive_loop, daemon=True).start()

    while running:
        draw_board(screen, board, images, selected_square)
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(0, 640, WIDTH, 80))

        if status_message:
            display_message(screen, status_message)

        pygame.display.flip()

        if board.is_game_over() or connection_lost:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            clock.tick(30)
            continue

        if vs_ai and board.turn == chess.BLACK:
            move = ai_move(board, level=ai_level)
            board.push(move)
            save_game(board)
            selected_square = None
            status_message = "Check!" if board.is_check() else ""
            if board.is_checkmate():
                status_message = "Checkmate!"
            elif board.is_stalemate():
                status_message = "Stalemate!"
            continue

        if net and board.turn != player_color:
            if not move_queue.empty():
                move = move_queue.get()
                if move == "__DISCONNECT__":
                    connection_lost = True
                    status_message = "Disconnect!"
                else:
                    board.push(chess.Move.from_uci(move))
                    selected_square = None
                    status_message = "Check!" if board.is_check() else ""
                    if board.is_checkmate():
                        status_message = "Checkmate!"
                    elif board.is_stalemate():
                        status_message = "Stalemate!"
            else:
                pygame.time.delay(10)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = pause_menu(screen)
                    if action == "save_exit":
                        save_game(board)
                        return
                    elif action == "restart":
                        board = chess.Board()
                        selected_square = None
                        status_message = ""
                        continue
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y > 640:
                    continue
                col, row = x // 80, 7 - y // 80
                square = row * 8 + col
                if selected_square is None:
                    if board.piece_at(square) and board.piece_at(square).color == board.turn:
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        if net:
                            try:
                                net.send_move(move.uci())
                            except (ConnectionResetError, socket.error):
                                connection_lost = True
                                status_message = "Disconnect!"
                        save_game(board)
                        status_message = "Check!" if board.is_check() else ""
                        if board.is_checkmate():
                            status_message = "Checkmate!"
                        elif board.is_stalemate():
                            status_message = "Stalemate!"
                        
                    selected_square = None
        clock.tick(30)
