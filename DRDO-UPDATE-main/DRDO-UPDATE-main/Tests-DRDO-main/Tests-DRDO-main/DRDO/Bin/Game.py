import pygame
import random
import math
import sqlite3

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

# Game settings
CENTER = (WIDTH // 2, HEIGHT // 2)
BIG_RADIUS = 200
SMALL_RADIUS = 20
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

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    win.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and waiting_for_press:
                score += 1  # Reward point for correct press
                waiting_for_press = False  # Reset waiting_for_press after correct press
            elif event.key == pygame.K_SPACE and skip_next:
                score -= 1  # Deduct point for incorrect press after skip
                running = False  # Stop the game if spacebar pressed at wrong time
            elif event.key == pygame.K_SPACE and not skip_next:
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

# Game over
win.fill(WHITE)
game_over_text = font.render("Game Over", True, RED)
final_score_text = font.render(f"Final Score: {score}", True, BLACK)
win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
win.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 20))
pygame.display.update()

# Get player name from user input
player_name = input("Enter your name: ")

# Create database tables if not exists
create_tables()

# Add player to
