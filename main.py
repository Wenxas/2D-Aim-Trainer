import pygame
import random
import sys

pygame.init()

TARGET_RADIUS = 20
TARGET_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
TARGET_DELAY = 1000
SCORE_FONT_SIZE = 36
TARGET_COUNT = 10

targets = []
score = 0
font = pygame.font.Font(None, SCORE_FONT_SIZE)
screen = None

def start_game(last_target_time):
    global targets, score
    targets = []
    score = 0
    return pygame.time.get_ticks() - TARGET_DELAY

def main_menu():
    global score
    menu = True
    last_target_time = pygame.time.get_ticks() - TARGET_DELAY
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BACKGROUND_COLOR)

        title_text = font.render("Aim Trainer", True, (255, 255, 255))
        play_text = font.render("Play", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

        screen.blit(title_text, title_rect)
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if play_rect.collidepoint(mouse_x, mouse_y) and click[0]:
            menu = False
            last_target_time = start_game(last_target_time)
            game_loop(last_target_time)
        elif quit_rect.collidepoint(mouse_x, mouse_y) and click[0]:
            pygame.quit()
            sys.exit()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("2D Aim Trainer")

def game_loop(last_target_time):
    global score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                global screen
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    for target in list(targets):
                        tx, ty, _ = target
                        if (x - tx) ** 2 + (y - ty) ** 2 <= TARGET_RADIUS ** 2:
                            targets.remove(target)
                            score += 1

        current_time = pygame.time.get_ticks()
        if current_time - last_target_time >= TARGET_DELAY and len(targets) < TARGET_COUNT:
            x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
            y = random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)
            targets.append((x, y, current_time))
            last_target_time = current_time

        screen.fill(BACKGROUND_COLOR)

        for target in targets:
            x, y, _ = target
            pygame.draw.circle(screen, TARGET_COLOR, (x, y), TARGET_RADIUS)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

main_menu()
