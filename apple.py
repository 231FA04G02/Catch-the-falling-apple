import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Audio error: {e}")

# Screen setup
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Apples")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

# Load helpers
def safe_load_image(filename):
    if not os.path.isfile(filename):
        print(f"[ERROR] Missing image file: {filename}")
        sys.exit()
    return pygame.image.load(filename)

def safe_load_sound(filename):
    if not os.path.isfile(filename):
        print(f"[ERROR] Missing sound file: {filename}")
        return None
    return pygame.mixer.Sound(filename)

# Load assets
background_img = safe_load_image("background.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
basket_img = safe_load_image("basket1.png")
basket_img = pygame.transform.scale(basket_img, (100, 60))

try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Music error: {e}")

catch_sound = safe_load_sound("catch_sound.wav")
game_over_sound = safe_load_sound("game_over.wav")

# High score
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Game logic
def run_game():
    basket_rect = basket_img.get_rect()
    basket_rect.midbottom = (WIDTH // 2, HEIGHT - 30)

    apple_img = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(apple_img, (255, 0, 0), (15, 15), 15)
    apple_rect = apple_img.get_rect()
    apple_rect.topleft = (random.randint(0, WIDTH - 30), -30)

    basket_speed = 10
    apple_speed = 5
    score = 0
    game_over = False
    high_score = load_high_score()

    while True:
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and basket_rect.left > 0:
                basket_rect.x -= basket_speed
            if keys[pygame.K_RIGHT] and basket_rect.right < WIDTH:
                basket_rect.x += basket_speed

            apple_rect.y += apple_speed

            # Missed the apple
            if apple_rect.top > HEIGHT:
                if game_over_sound:
                    game_over_sound.play()
                game_over = True
                if score > high_score:
                    high_score = score
                    save_high_score(score)

            # Caught the apple
            if basket_rect.colliderect(apple_rect):
                score += 1
                if catch_sound:
                    catch_sound.play()
                apple_rect.topleft = (random.randint(0, WIDTH - 30), -30)

                if score % 5 == 0:
                    apple_speed += 1

            # Draw everything
            screen.blit(basket_img, basket_rect)
            screen.blit(apple_img, apple_rect)
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

        else:
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
            high_score_text = small_font.render(f"High Score: {high_score}", True, (0, 100, 0))
            restart_text = small_font.render("Press R to Restart or ESC to Quit", True, (50, 50, 50))

            screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 80))
            screen.blit(final_score_text, (WIDTH // 2 - 130, HEIGHT // 2 - 20))
            screen.blit(high_score_text, (WIDTH // 2 - 130, HEIGHT // 2 + 30))
            screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 80))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                return  # restart
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Start menu
def show_start_menu():
    while True:
        screen.blit(background_img, (0, 0))
        title_text = font.render("Catch the Falling Apples", True, (0, 100, 200))
        start_text = small_font.render("Press ENTER to Start", True, (50, 50, 50))
        screen.blit(title_text, (WIDTH // 2 - 200, HEIGHT // 2 - 60))
        screen.blit(start_text, (WIDTH // 2 - 130, HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return

        pygame.display.flip()
        clock.tick(30)

# Run game loop
while True:
    show_start_menu()
    run_game()
