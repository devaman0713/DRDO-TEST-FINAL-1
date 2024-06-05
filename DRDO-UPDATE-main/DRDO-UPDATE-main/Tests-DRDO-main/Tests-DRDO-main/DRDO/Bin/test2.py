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
pygame.display.set_caption("Circle Light Up Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

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

        win.fill(WHITE)
        prompt_text = font.render("Enter your name: ", True, BLACK)
        name_text = font.render(name, True, BLACK)
        win.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 20))
        win.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.update()

    return name

# Function to draw a button
def draw_button(text, rect, color, font, text_color):
    pygame.draw.rect(win, color, rect)
    button_text = font.render(text, True, text_color)
    win.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2, rect.y + (rect.height - button_text.get_height()) // 2))

# Function to check if a point is inside a rectangle
def is_point_in_rect(point, rect):
    return rect.collidepoint(point)

# Main game loop function
def main_game_loop():
    global current_circle, score, skip_next, waiting_for_press, correct_presses, incorrect_presses
    
    # Game variables
    current_circle = 0
    score = 0
    skip_next = False
    waiting_for_press = False
    
    # Reset press lists
    correct_presses = []
    incorrect_presses = []

    # Get player name
    player_name = get_player_name()
    if not player_name:
        pygame.quit()
        exit()

    # Game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        win.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if waiting_for_press:
                        score += 1  # Reward point for correct press
                        correct_presses.append(circle_positions[current_circle])  # Log correct press position
                        waiting_for_press = False  # Reset waiting_for_press after correct press
                    elif skip_next:
                        score -= 1  # Deduct point for incorrect press after skip
                        incorrect_presses.append(circle_positions[current_circle])  # Log incorrect press position
                        running = False  # Stop the game if spacebar pressed at wrong time
                    else:
                        incorrect_presses.append(circle_positions[current_circle])  # Log incorrect press position
                        running = False  # Stop the game if spacebar pressed when no skip pending

        # Draw circles
        for i in range(NUM_CIRCLES):
            color = GREEN if i == current_circle else BLUE
            pygame.draw.circle(win, color, (int(circle_positions[i][0]), int(circle_positions[i][1])), SMALL_RADIUS)

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        win.blit(score_text, (10, 10))

        # Update circle
        if skip_next:
            current_circle = (current_circle + 2) % NUM_CIRCLES
            waiting_for_press = True  # Now wait for user press
            skip_next = False
        else:
            if random.random() < 0.1:  # 10% chance to skip the next circle
                skip_next = True
            else:
                current_circle = (current_circle + 1) % NUM_CIRCLES

        pygame.display.update()
        clock.tick(1)  # Slower circle movement

    # Save results to CSV file
    csv_file = 'game_results.csv'
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Player Name', 'Score', 'Correct Presses', 'Incorrect Presses'])
        writer.writerow([player_name, score, correct_presses, incorrect_presses])

    return player_name, score

# Main function
def main():
    while True:
        player_name, score = main_game_loop()
        
        # Game over screen
        win.fill(WHITE)
        game_over_text = font.render("Game Over", True, RED)
        final_score_text = font.render(f"Final Score: {score}", True, BLACK)
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        win.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 20))

        # Draw restart button
        restart_button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50)
        draw_button("Restart", restart_button_rect, GRAY, font, BLACK)
        pygame.display.update()

        # Wait for restart
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if is_point_in_rect(event.pos, restart_button_rect):
                        waiting_for_restart = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting_for_restart = False

        pygame.time.delay(500)  # Add a small delay to avoid accidental double-clicks

if __name__ == "__main__":
    main()
