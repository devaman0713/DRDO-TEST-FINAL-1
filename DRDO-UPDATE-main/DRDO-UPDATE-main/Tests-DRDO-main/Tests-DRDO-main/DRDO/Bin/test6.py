import pygame
import random
import csv
import os

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 5, 5  # Grid size
CIRCLE_RADIUS = 30
CIRCLE_MARGIN = 10
GRID_WIDTH = COLS * (2 * CIRCLE_RADIUS + CIRCLE_MARGIN)
GRID_HEIGHT = ROWS * (2 * CIRCLE_RADIUS + CIRCLE_MARGIN)
OFFSET_X = (WIDTH - GRID_WIDTH) // 2
OFFSET_Y = (HEIGHT - GRID_HEIGHT) // 2

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square Detection Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)

# Font
font = pygame.font.SysFont(None, 36)

# Filepath for the CSV
csv_filepath = "game_data_1.csv"

# Function to draw the grid
def draw_grid(grid, win):
    win.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            x = OFFSET_X + col * (2 * CIRCLE_RADIUS + CIRCLE_MARGIN) + CIRCLE_RADIUS
            y = OFFSET_Y + row * (2 * CIRCLE_RADIUS + CIRCLE_MARGIN) + CIRCLE_RADIUS
            color = YELLOW if grid[row][col] else WHITE
            pygame.draw.circle(win, color, (x, y), CIRCLE_RADIUS)

# Function to check for square formation
def check_square(grid):
    for row in range(ROWS - 1):
        for col in range(COLS - 1):
            if grid[row][col] and grid[row][col + 1] and grid[row + 1][col] and grid[row + 1][col + 1]:
                return True
    return False

# Function to save data to CSV
def save_to_csv(player_name, score, correct_presses, incorrect_presses):
    file_exists = os.path.isfile(csv_filepath)
    with open(csv_filepath, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Player Name", "Score", "Correct Presses", "Incorrect Presses"])
        writer.writerow([player_name, score, 
                         ' '.join([f"({x},{y},{z})" for (x, y, z) in correct_presses]), 
                         ' '.join([f"({x},{y},{z})" for (x, y, z) in incorrect_presses])])

# Function to get the player name
def get_player_name():
    name = ""
    getting_name = True
    while getting_name:
        win.fill(BLACK)
        prompt = font.render("Enter your name: ", True, WHITE)
        name_text = font.render(name, True, WHITE)
        win.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 50))
        win.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":
                    getting_name = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

    return name

# Main game loop function
def main_game_loop(player_name):
    grid = [[False for _ in range(COLS)] for _ in range(ROWS)]
    score = 0
    game_over = False
    correct_presses = []
    incorrect_presses = []
    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if check_square(grid):
                    score += 1
                    correct_presses.append((OFFSET_X + col * (2 * CIRCLE_RADIUS + CIRCLE_MARGIN) + CIRCLE_RADIUS, 
                                            OFFSET_Y + row * (2 * CIRCLE_RADIUS + CIRCLE_MARGIN) + CIRCLE_RADIUS, 0))
                else:
                    incorrect_presses.append((OFFSET_X + col * (2 * CIRCLE_RADIUS + CIRCLE_MARGIN) + CIRCLE_RADIUS, 
                                              OFFSET_Y + row * (2 * CIRCLE_RADIUS + CIRCLE_MARGIN) + CIRCLE_RADIUS, 0))
                    game_over = True

        # Randomly light up a circle
        row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        grid[row][col] = not grid[row][col]

        draw_grid(grid, win)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(1)  # Slow down the circle lighting speed

    save_to_csv(player_name, score, correct_presses, incorrect_presses)
    return score

# Main function
def main():
    while True:
        player_name = get_player_name()
        if player_name is None:
            break
        score = main_game_loop(player_name)

        # Game over screen
        win.fill(BLACK)
        game_over_text = font.render("Game Over", True, RED)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        win.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 20))

        # Draw restart button
        restart_button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50)
        pygame.draw.rect(win, LIGHT_BLUE, restart_button_rect)
        restart_text = font.render("Restart", True, BLACK)
        win.blit(restart_text, (restart_button_rect.x + (restart_button_rect.width - restart_text.get_width()) // 2,
                                restart_button_rect.y + (restart_button_rect.height - restart_text.get_height()) // 2))
        pygame.display.update()

        # Wait for restart
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_button_rect.collidepoint(event.pos):
                        waiting_for_restart = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting_for_restart = False

        pygame.time.delay(500)  # Add a small delay to avoid accidental double-clicks

if __name__ == "__main__":
    main()
