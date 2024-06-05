import pygame
import random
import math
import csv
import os

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DRDO-P1-CircleTest")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game settings
CENTER = (WIDTH // 2, HEIGHT // 2)
BIG_RADIUS = 250
SMALL_RADIUS = 30
NUM_CIRCLES = 12

# Circle positions
circle_positions = []
for i in range(NUM_CIRCLES):
    angle = i * (2 * math.pi / NUM_CIRCLES)
    x = CENTER[0] + BIG_RADIUS * math.cos(angle)
    y = CENTER[1] + BIG_RADIUS * math.sin(angle)
    circle_positions.append((x, y))

# Game variables
current_circle = 0
score = 0
skip_next = False
waiting_for_press = False
font = pygame.font.SysFont(None, 36)

# Lists to track correct and incorrect presses
correct_presses = []
incorrect_presses = []

# Function to get player name
def get_player_name():
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        win.fill(BLACK)
        prompt_text = font.render("Enter your name: ", True, WHITE)
        name_text = font.render(name, True, WHITE)
        win.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 20))
        win.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.update()

    return name

def save_results(player_name, score, correct_presses, incorrect_presses):
    csv_file = 'game_results_clockwise.csv'
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Player Name', 'Score', 'Correct Presses', 'Incorrect Presses'])
        writer.writerow([player_name, score, correct_presses, incorrect_presses])

def draw_retry_button():
    retry_button_text = font.render("Retry", True, BLACK)
    retry_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
    pygame.draw.rect(win, WHITE, retry_button_rect)
    win.blit(retry_button_text, (retry_button_rect.x + (retry_button_rect.width - retry_button_text.get_width()) // 2,
                                 retry_button_rect.y + (retry_button_rect.height - retry_button_text.get_height()) // 2))
    return retry_button_rect

def game_loop():
    global current_circle, score, skip_next, waiting_for_press, correct_presses, incorrect_presses

    running = True
    clock = pygame.time.Clock()
    while running:
        win.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if waiting_for_press:
                        score += 1  # Reward point for correct press
                        correct_presses.append((random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)))  # Log correct press position
                        waiting_for_press = False  # Reset waiting_for_press after correct press
                    elif skip_next:
                        score -= 1  # Deduct point for incorrect press after skip
                        incorrect_presses.append((random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)))  # Log incorrect press position
                        running = False  # Stop the game if spacebar pressed at wrong time
                    else:
                        incorrect_presses.append((random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)))  # Log incorrect press position
                        running = False  # Stop the game if spacebar pressed when no skip pending

        # Draw circles
        for i in range(NUM_CIRCLES):
            color = YELLOW if i == current_circle else WHITE
            pygame.draw.circle(win, color, (int(circle_positions[i][0]), int(circle_positions[i][1])), SMALL_RADIUS)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))

        # Update circle
                # Update circle
        if skip_next:
            current_circle = (current_circle + 2) % NUM_CIRCLES
            waiting_for_press = True  # Now wait for user press
            skip_next = False
        else:
            if random.random() < 0.1:  # 10% chance to skip the next circle
                skip_next = True
            else:
                current_circle = (current_circle + 1) % NUM_CIRCLES  # Increment to move clockwise


        pygame.display.update()
        clock.tick(1)  # Slower circle movement

    return score, correct_presses, incorrect_presses

def main():
    global current_circle, score, skip_next, waiting_for_press, correct_presses, incorrect_presses

    # Get player name
    player_name = get_player_name()
    if not player_name:
        pygame.quit()
        exit()

    retry = True
    while retry:
        # Reset game variables
        current_circle = 0
        score = 0
        skip_next = False
        waiting_for_press = False
        correct_presses = []
        incorrect_presses = []

        # Run the game loop
        score, correct_presses, incorrect_presses = game_loop()

        # Game over screen
        win.fill(BLACK)
        game_over_text = font.render("Game Over", True, RED)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        win.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 20))
        retry_button_rect = draw_retry_button()
        pygame.display.update()

        # Save results to CSV file
        save_results(player_name, score, correct_presses, incorrect_presses)

        retry = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    retry = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button_rect.collidepoint(event.pos):
                        retry = True
                        break

if __name__ == "__main__":
    main()
