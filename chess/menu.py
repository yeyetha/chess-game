import pygame
from game import start_game
import os
def get_ip_input(screen):
    import pygame
    input_box = pygame.Rect(180, 250, 280, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    while True:
        screen.fill((40, 40, 40))
        txt_surface = font.render("Enter Host IP: " + text, True, color)
        width = max(300, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        pygame.display.flip()
        clock.tick(30)


        
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