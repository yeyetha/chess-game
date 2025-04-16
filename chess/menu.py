import pygame
from game import start_game
import os

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((640, 720))  # Increased height for spacing
    pygame.display.set_caption("Chess Menu")
    font = pygame.font.SysFont("Arial", 36)
    clock = pygame.time.Clock()

    ai_levels = ["random", "easy", "medium", "hard"]
    ai_level = 2
    options = ["New Game (vs AI)", "Continue", "PvP Host", "PvP Join", "Change AI Level", "Quit"]
    selected = 0

    while True:
        screen.fill((50, 50, 50))

        for i, option in enumerate(options):
            label = option
            if option == "Change AI Level":
                label += f" ({ai_levels[ai_level]})"
            color = (255, 255, 255) if i == selected else (180, 180, 180)
            text = font.render(label, True, color)
            screen.blit(text, (80, 100 + i * 60))  # Adjusted vertical offset

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        start_game(vs_ai=True, load_saved_game=False, ai_level=ai_levels[ai_level])
                    elif selected == 1:
                        if os.path.exists("save_game.txt"):
                            start_game(vs_ai=True, load_saved_game=True, ai_level=ai_levels[ai_level])
                    elif selected == 2:
                        start_game(vs_ai=False, load_saved_game=False, network="host")
                    elif selected == 3:
                        start_game(vs_ai=False, load_saved_game=False, network="join")
                    elif selected == 4:
                        ai_level = (ai_level + 1) % len(ai_levels)
                    elif selected == 5:
                        return
        clock.tick(30)