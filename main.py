import pygame as pg
import sqlite3
from random import randrange

# ================== INITIALIZATION ==================
pg.init()
pg.mixer.init()
bite_sound = pg.mixer.Sound('360685__herrabilbo__eating-v2 (1).mp3')

# ================== CONSTANTS ==================
WINDOW = 800
TILE_SIZE = 40
RANGE = (0, WINDOW // TILE_SIZE - 1)
SPEED_INCREMENT = 1
rainbow_mode = False
power_up = None
power_up_timer = None



import random

MAZE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]



# Add random '1's in the middle or sides of each maze line
# for row in MAZE:
#     num_random_ones = random.randint(0, 3)
#     for _ in range(num_random_ones):
#         index = random.randint(1, len(row) - 2)
#         row[index] = 1

# Print the modified maze
for row in MAZE:
    print(row)




POWER_UP_DURATION = 5000  # 5 seconds in milliseconds
DOUBLE_SCORE_DURATION = 10000  # 10 seconds in milliseconds
power_up = None
power_up_timer = None
double_score_timer = None
last_power_up_spawn_time = 0




# ================== DATABASE SETUP & FUNCTIONS ==================
def init_db():
    conn = sqlite3.connect('highscores.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS highscores (name TEXT, score INTEGER)''')
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

def get_top_scores(limit=5):
    cursor.execute('SELECT name, score FROM highscores ORDER BY score DESC LIMIT ?', (limit,))
    return cursor.fetchall()

def get_highscore():
    cursor.execute('SELECT MAX(score) FROM highscores')
    return cursor.fetchone()[0] or 0

def save_highscore(name, score):
    cursor.execute('INSERT INTO highscores (name, score) VALUES (?, ?)', (name, score))
    conn.commit()

def delete_highscore(name):
    cursor.execute('DELETE FROM highscores WHERE name = ?', (name,))
    conn.commit()


def spawn_power_up():
    global power_up, power_up_timer
    power_up = pg.rect.Rect(get_random_position() + [TILE_SIZE, TILE_SIZE])
    power_up_timer = pg.time.get_ticks() + POWER_UP_DURATION


def check_power_up_collision(snake):
    global score, power_up, power_up_timer, double_score_timer
    if snake[0].colliderect(power_up):
        power_up = None
        power_up_timer = None
        double_score_timer = pg.time.get_ticks() + DOUBLE_SCORE_DURATION
        bite_sound.play()

# ================== GAME HELPER FUNCTIONS ==================
get_random_position = lambda: [randrange(*RANGE) * TILE_SIZE for _ in range(2)]

def draw_grid():
    for x in range(0, WINDOW, TILE_SIZE):
        color = (x * 255 // WINDOW, 0, 255 - x * 255 // WINDOW)
        pg.draw.line(screen, color, (x, 0), (x, WINDOW))
    for y in range(0, WINDOW, TILE_SIZE):
        color = (y * 255 // WINDOW, 255 - y * 255 // WINDOW, 0)
        pg.draw.line(screen, color, (0, y), (WINDOW, y))



def draw_maze():
    screen.fill((0, 0, 0))  # Fill the screen with black color
    for y, row in enumerate(MAZE):
        for x, cell in enumerate(row):
            cell_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pg.draw.rect(screen, 'blue' if cell == 1 else 'black', cell_rect)
            if cell == 0:
                pg.draw.rect(screen, 'gray', cell_rect, 1)  # Draw a gray border for empty cells

    for x in range(0, WINDOW, TILE_SIZE):
        pg.draw.line(screen, (50, 50, 50), (x, 0), (x, WINDOW))
    for y in range(0, WINDOW, TILE_SIZE):
        pg.draw.line(screen, (50, 50, 50), (0, y), (WINDOW, y))

def display_and_manage_highscores(current_score):
    print("Game Over!")

    if current_score > get_highscore():
        user_name = input("Enter your name for the highscore: ")
        save_highscore(user_name, current_score)
        print(f"New highscore saved for {user_name}!")

    # Display the title
    title_text = font.render("Highscores", True, (255, 255, 255))
    screen.blit(title_text, (WINDOW // 2 - title_text.get_width() // 2, WINDOW // 4))

    # Display top scores
    top_scores = get_top_scores()
    for index, (name, score) in enumerate(top_scores):
        score_text = font.render(f"{index + 1}. {name}: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WINDOW // 4, WINDOW // 4 + index * 40))
    pg.display.flip()
    pg.time.wait(5000)

    def pause_menu():
        paused = True
        selected = 0
        options = ["Resume", "Restart", "Exit"]

        while paused:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return "exit"
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_DOWN:
                            selected = (selected + 1) % len(options)
                        elif event.key == pg.K_UP:
                            selected = (selected - 1) % len(options)
                        elif event.key == pg.K_RETURN:
                            if selected == 0:  # Resume
                                return "resume"
                            elif selected == 1:  # Restart
                                return "restart"
                            elif selected == 2:  # Exit
                                return "exit"


        screen.fill((0, 0, 0))
        for index, option in enumerate(options):
            color = (255, 255, 255) if index == selected else (100, 100, 100)
            text = font.render(option, True, color)
            screen.blit(text, (WINDOW // 2 - text.get_width() // 2, WINDOW // 2 + index * 40))
        pg.display.flip()
        clock.tick(60)


    # Ask if user wants to delete a highscore
    option = input("Do you want to delete a highscore? (yes/no): ")
    if option.lower() == 'yes':
        name_to_delete = input("Enter the name of the player whose highscore you want to delete: ")
        delete_highscore(name_to_delete)
        print(f"Highscore for {name_to_delete} has been deleted.")
    

# ================== ORIGINAL GAME ==================
def original_game():
    global power_up, power_up_timer, double_score_timer, rainbow_mode, rainbow_mode_timer

    snake = [pg.rect.Rect([0, 0, TILE_SIZE, TILE_SIZE])]
    food = pg.rect.Rect(get_random_position() + [TILE_SIZE, TILE_SIZE])
    direction = (TILE_SIZE, 0)
    score = 0
    speed = 10
    last_power_up_spawn_time = 0
    rainbow_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0),
                      (0, 255, 0), (0, 0, 255), (75, 0, 130),
                      (238, 130, 238)]
    rainbow_mode = False
    rainbow_mode_timer = 0

    def pause_menu():
        paused = True
        selected = 0
        options = ["Resume", "Restart", "Exit"]

        while paused:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "exit"
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pg.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pg.K_RETURN:
                        if selected == 0:  # Resume
                            paused = False
                        elif selected == 1:  # Restart
                            return "restart"
                        elif selected == 2:  # Exit
                            return "exit"

            screen.fill((0, 0, 0))
            for index, option in enumerate(options):
                color = (255, 255, 255) if index == selected else (100, 100, 100)
                text = font.render(option, True, color)
                screen.blit(text, (WINDOW // 2 - text.get_width() // 2, WINDOW // 2 + index * 40))
            pg.display.flip()
            clock.tick(60)

        return "resume"

    while True:
        current_time = pg.time.get_ticks()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    result = pause_menu()
                    if result == "exit":
                        exit()
                    elif result == "restart":
                        return original_game()
                elif event.key == pg.K_UP and direction != (0, TILE_SIZE):
                    direction = (0, -TILE_SIZE)
                elif event.key == pg.K_DOWN and direction != (0, -TILE_SIZE):
                    direction = (0, TILE_SIZE)
                elif event.key == pg.K_LEFT and direction != (TILE_SIZE, 0):
                    direction = (-TILE_SIZE, 0)
                elif event.key == pg.K_RIGHT and direction != (-TILE_SIZE, 0):
                    direction = (TILE_SIZE, 0)

        head = snake[0].copy()
        head.move_ip(direction)
        snake.insert(0, head)

        if power_up and snake[0].colliderect(power_up):
            power_up = None
            power_up_timer = None
            double_score_timer = current_time + DOUBLE_SCORE_DURATION
            rainbow_mode = True
            rainbow_mode_timer = current_time + 5000
            bite_sound.play()

        if power_up is None and current_time - last_power_up_spawn_time >= 5000:
            spawn_power_up()
            last_power_up_spawn_time = current_time
        if power_up:
            check_power_up_collision(snake)

        if power_up_timer and current_time >= power_up_timer:
            power_up = None
            power_up_timer = None

        if snake[0].colliderect(food):
            food.topleft = get_random_position()
            score_increment = 2 if double_score_timer and pg.time.get_ticks() < double_score_timer else 1
            score += score_increment
            speed += SPEED_INCREMENT
            bite_sound.play()
        else:
            snake.pop()

        if (snake[0].left < 0 or snake[0].right > WINDOW or
                snake[0].top < 0 or snake[0].bottom > WINDOW or
                snake[0] in snake[1:]):
            break

        screen.fill((0, 0, 0))
        draw_grid()

        for index, segment in enumerate(snake):
            if rainbow_mode and current_time < rainbow_mode_timer:
                color_index = (current_time // 100) % len(rainbow_colors)
                color = rainbow_colors[color_index]
            else:
                color = (0, 255, 0)
            pg.draw.rect(screen, color, segment)

        pg.draw.rect(screen, 'red', food)
        if power_up:
            pg.draw.ellipse(screen, 'purple', power_up)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if double_score_timer and pg.time.get_ticks() < double_score_timer:
            double_score_text = font.render('Double Score Active!', True, (255, 0, 255))
            screen.blit(double_score_text, (WINDOW - double_score_text.get_width() - 10, 10))

        pg.display.flip()
        clock.tick(speed)

    display_and_manage_highscores(score)

# ================== MAZE GAME ==================

def maze_game():
    snake = [pg.rect.Rect([TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE])]  # Start at a valid position in the maze
    direction = (TILE_SIZE, 0)
    score = 0
    speed = 10
    food_position = get_random_position()
    food = pg.rect.Rect(food_position + [TILE_SIZE, TILE_SIZE])

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and direction != (0, TILE_SIZE):
                    direction = (0, -TILE_SIZE)
                elif event.key == pg.K_DOWN and direction != (0, -TILE_SIZE):
                    direction = (0, TILE_SIZE)
                elif event.key == pg.K_LEFT and direction != (TILE_SIZE, 0):
                    direction = (-TILE_SIZE, 0)
                elif event.key == pg.K_RIGHT and direction != (-TILE_SIZE, 0):
                    direction = (TILE_SIZE, 0)

        head = snake[0].copy()
        head.move_ip(direction)
        snake.insert(0, head)

        # Check for maze collisions
        maze_x, maze_y = head.topleft[0] // TILE_SIZE, head.topleft[1] // TILE_SIZE
        if maze_y < 0 or maze_y >= len(MAZE) or maze_x < 0 or maze_x >= len(MAZE[0]) or MAZE[maze_y][maze_x] == 1:
            break

        if snake[0].colliderect(food):
            food_position = get_random_position()
            while MAZE[food_position[1] // TILE_SIZE][food_position[0] // TILE_SIZE] == 1:
                food_position = get_random_position()
            food.topleft = food_position
            score += 1
            speed += SPEED_INCREMENT
            bite_sound.play()
        else:
            snake.pop()

        if (snake[0].left < 0 or snake[0].right > WINDOW or
                snake[0].top < 0 or snake[0].bottom > WINDOW or
                snake[0] in snake[1:]):
                
            break

        food_maze_x, food_maze_y = food.topleft[0] // TILE_SIZE, food.topleft[1] // TILE_SIZE
        if MAZE[food_maze_y][food_maze_x] == 1:
            continue 

        screen.fill((0, 0, 0))
        draw_grid()
        draw_maze()
        [pg.draw.rect(screen, 'green', segment) for segment in snake]
        pg.draw.rect(screen, 'red', food)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        if double_score_timer and pg.time.get_ticks() < double_score_timer:
            double_score_text = font.render('Double Score Active!', True, (255, 0, 255))
            screen.blit(double_score_text, (WINDOW - double_score_text.get_width() - 10, 10))

        screen.blit(score_text, (10, 10))
        pg.display.flip()
        clock.tick(speed)

    display_and_manage_highscores(score)


    # This function will be similar to the original_game function but will include the maze drawing and logic.

# ================== MAIN MENU ==================
def main_menu():
    selected = 0
    options = ["Play Original Game", "Play Maze Game"]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    selected = (selected + 1) % 2
                elif event.key == pg.K_UP:
                    selected = (selected - 1) % 2
                elif event.key == pg.K_RETURN:
                    if selected == 0:
                        original_game()
                    else:
                        maze_game()
                    return

        screen.fill((0, 0, 0))
        for index, option in enumerate(options):
            color = (255, 255, 255) if index == selected else (100, 100, 100)
            text = font.render(option, True, color)
            screen.blit(text, (WINDOW // 2 - text.get_width() // 2, WINDOW // 2 + index * 40))
        pg.display.flip()
        clock.tick(60)

# ================== GAME INITIALIZATION ==================
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
font = pg.font.SysFont(None, 36)
 
# ================== START THE GAME ==================
main_menu()
