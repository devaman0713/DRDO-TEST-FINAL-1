import pygame
import random
import math
import csv
import os
import time
import sys

# Initialize pygame
pygame.init()

# Set up display
pygame.display.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("DRDO-P1-CircleTest")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game settings
CENTER = (WIDTH // 2, HEIGHT // 2)
BIG_RADIUS = 250
SMALL_RADIUS = 7
NUM_CIRCLES = 36
GAME_DURATION = 30  # in seconds

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
font = pygame.font.SysFont(None, min(WIDTH, HEIGHT) // 20)


correct_presses = []
incorrect_presses = []
correct_press_score = 0
incorrect_press_score = 0

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

def save_results(player_name, score, correct_presses, incorrect_presses,correct_press_score,incorrect_press_score):
    csv_file = 'game_results_clockwise.csv'
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Player_Name', 'Score', 'Correct_Presses', 'Incorrect_Presses','Correct_Score','incorrect_Score'])
        writer.writerow([player_name, score, correct_presses, incorrect_presses,correct_press_score,incorrect_press_score])

def draw_buttons():
    retry_button_text = font.render("Retry", True, BLACK)
    retry_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 100, 50)
    pygame.draw.rect(win, WHITE, retry_button_rect)
    win.blit(retry_button_text, (retry_button_rect.x + (retry_button_rect.width - retry_button_text.get_width()) // 2,
                                 retry_button_rect.y + (retry_button_rect.height - retry_button_text.get_height()) // 2))

    close_button_text = font.render("Close", True, BLACK)
    close_button_rect = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 + 50, 100, 50)
    pygame.draw.rect(win, WHITE, close_button_rect)
    win.blit(close_button_text, (close_button_rect.x + (close_button_rect.width - close_button_text.get_width()) // 2,
                                 close_button_rect.y + (close_button_rect.height - close_button_text.get_height()) // 2))

    return retry_button_rect, close_button_rect

def main():
    global current_circle, score, skip_next, waiting_for_press, correct_presses, incorrect_presses ,correct_press_score,incorrect_press_score

    # Get player name
    player_name = get_player_name()
    if not player_name:
        pygame.quit()
        sys.exit()

    # Game loop
    # correct_press_score = 0
    # incorrect_press_score = 0
    start_time = time.time()
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
                        score += 1  
                        correct_presses.append(circle_positions[current_circle])  
                        correct_press_score += 1
                        waiting_for_press = False 
                    elif skip_next:
                        score -= 1  
                        incorrect_presses.append(circle_positions[current_circle]) 
                        incorrect_press_score +=1 
                        waiting_for_press = False  
                    else:
                        incorrect_presses.append(circle_positions[current_circle])  
                        waiting_for_press = False 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    running = False
                elif close_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Draw circles
        for i in range(NUM_CIRCLES):
            color = RED if i == current_circle else WHITE
            pygame.draw.circle(win, color, (int(circle_positions[i][0]), int(circle_positions[i][1])), SMALL_RADIUS)

        # Update circle
        if skip_next:
            current_circle = (current_circle + 2) % NUM_CIRCLES
            waiting_for_press = True 
            skip_next = False
        else:
            if random.random() < .3:  
                skip_next = True
            else:
                current_circle = (current_circle + 1) % NUM_CIRCLES

        pygame.display.update()
        clock.tick(3)  

        
        if time.time() - start_time >= GAME_DURATION:
            running = False

    # Game over
    win.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    # final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    # win.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 20))
    retry_button_rect, close_button_rect = draw_buttons()
    pygame.display.update()

    # Save results to CSV file
    save_results(player_name, score, correct_presses, incorrect_presses,correct_press_score,incorrect_press_score)

    retry = False
    while not retry:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                retry = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    retry = True
                elif close_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    pygame.time.delay(500)  

# Run the game
while True:
    main()
