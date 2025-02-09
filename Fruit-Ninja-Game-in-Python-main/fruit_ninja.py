import pygame, sys, os, random

# Game variables
player_lives = 3
score = 0
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 500
FPS = 5
pygame.display.set_caption('Fruit Ninja Game')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)

# Load assets safely
base_path = os.path.dirname(__file__)  # Get script directory
background_path = os.path.join(base_path, 'back.jpg')
if not os.path.exists(background_path):
    print("Error: 'back.jpg' not found. Please add the background image.")
    pygame.quit()
    sys.exit()

background = pygame.image.load(background_path)

font = pygame.font.Font(None, 42)  # Use default font if 'comic.ttf' is missing
score_text = font.render(f'Score : {score}', True, WHITE)

# Load life icon
lives_icon_path = os.path.join(base_path, 'images', 'white_lives.png')
if os.path.exists(lives_icon_path):
    lives_icon = pygame.image.load(lives_icon_path)
else:
    print("Error: 'white_lives.png' not found. Please add the life icon.")
    pygame.quit()
    sys.exit()

# Function to generate fruits
def generate_random_fruits(fruit):
    fruit_path = os.path.join(base_path, 'images', f'{fruit}.png')
    if not os.path.exists(fruit_path):
        print(f"Error: '{fruit}.png' not found. Skipping {fruit}.")
        return

    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x': random.randint(100, 500),
        'y': 800,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-80, -60),
        'throw': random.random() >= 0.75,
        't': 0,
        'hit': False,
    }

# Initialize fruit dictionary
data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

# Function to draw text
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    display.blit(text_surface, text_rect)

# Function to draw lives
def draw_lives(display, x, y, lives, image_path):
    if not os.path.exists(image_path):
        print("Error: Life image missing.")
        return
    img = pygame.image.load(image_path)
    for i in range(lives):
        display.blit(img, (x + 35 * i, y))

# Game Over screen
def show_gameover_screen():
    gameDisplay.blit(background, (0, 0))
    draw_text(gameDisplay, "FRUIT NINJA!", 90, WIDTH // 2, HEIGHT // 4)
    draw_text(gameDisplay, f"Score : {score}", 50, WIDTH // 2, HEIGHT // 2)
    draw_text(gameDisplay, "Press a key to begin!", 64, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Game Loop
first_round = True
game_over = True
game_running = True

while game_running:
    if game_over:
        if first_round:
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(gameDisplay, 690, 5, player_lives, lives_icon_path)
        score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    score_text = font.render(f'Score : {score}', True, WHITE)
    gameDisplay.blit(score_text, (10, 10))
    draw_lives(gameDisplay, 690, 5, player_lives, lives_icon_path)

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()
            if (not value['hit'] and value['x'] < current_position[0] < value['x'] + 60
                    and value['y'] < current_position[1] < value['y'] + 60):
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:
                        show_gameover_screen()
                        game_over = True
                    half_fruit_path = os.path.join(base_path, 'images', 'explosion.png')
                else:
                    half_fruit_path = os.path.join(base_path, 'images', f'half_{key}.png')
                    score += 1

                if os.path.exists(half_fruit_path):
                    value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                value['hit'] = True
        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
