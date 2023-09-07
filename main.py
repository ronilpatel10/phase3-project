import pygame as pg
import sqlite3
from random import randrange

# ================== INITIALIZATION ==================
pg.init()
screen_width, screen_height = pg.display.Info().current_w, pg.display.Info().current_h
screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN)
pg.display.set_caption("Serphant Safari")
pg.mixer.init()

background_music = pg.mixer.music.load('370294__mrthenoronha__tribal-game-theme-loop.wav')
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play(-1)

bite_sound = pg.mixer.Sound('360685__herrabilbo__eating-v2 (1).mp3')
death_sound = pg.mixer.Sound('180350__jorickhoofd__scream-noooh.wav')
powerup_sound = pg.mixer.Sound('523648__matrixxx__powerup-08.wav')

TILE_SIZE = min(screen_width // 25, screen_height // 25)
RANGE = (0, screen_width // TILE_SIZE - 2, 0, screen_height // TILE_SIZE - 2)
SPEED_INCREMENT = 1
rainbow_mode = False
power_up = None
power_up_timer = None
BACKGROUND_COLOR = (245, 222, 179)
GRID_COLOR = (34, 139, 34)

snake_image = pg.image.load('snake img.jpeg')
snake_image = pg.transform.scale(snake_image, (100000, 100000))
snake_head_image = pg.image.load('real snake img.jpeg')
snake_head_image = pg.transform.scale(snake_head_image, (TILE_SIZE, TILE_SIZE))
snake_body_image = pg.image.load('snake_body_segment.jpeg')
snake_body_image = pg.transform.scale(snake_body_image, (TILE_SIZE, TILE_SIZE))



# ================== CONSTANTS ==================





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
get_random_position = lambda: [randrange(RANGE[i], RANGE[i+1]) * TILE_SIZE for i in (0, 2)]



def draw_grid():
    # Fill the screen with sandy color
    screen.fill(BACKGROUND_COLOR)

    # Drawing grid lines
    for x in range(0, screen_width - TILE_SIZE, TILE_SIZE):
        pg.draw.line(screen, GRID_COLOR, (x, 0), (x, screen_height))
    for y in range(0, screen_height, TILE_SIZE):  # Adjusted the loop condition
        pg.draw.line(screen, GRID_COLOR, (0, y), (screen_width, y))
    
    # Drawing grass at the bottom
    for i in range(0, screen_width, 20):  # Draw small rectangles for grass effect
        pg.draw.rect(screen, GRID_COLOR, (i, screen_height - 20, 20, 20))




def draw_maze():
    screen.fill((0, 0, 0))  # Fill the screen with black color
    for y, row in enumerate(MAZE):
        for x, cell in enumerate(row):
            if x * TILE_SIZE < screen_width and y * TILE_SIZE < screen_height:
                cell_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pg.draw.rect(screen, 'blue' if cell == 1 else 'black', cell_rect)
                if cell == 0:
                    pg.draw.rect(screen, 'gray', cell_rect, 1)  # Draw a gray border for empty cells

    for x in range(0, screen_width, TILE_SIZE):
        pg.draw.line(screen, (50, 50, 50), (x, 0), (x, screen_height))
    for y in range(0, screen_height, TILE_SIZE):
        pg.draw.line(screen, (50, 50, 50), (0, y), (screen_width, y))


def game_over_screen(score):
    font = pg.font.SysFont(None, 48)
    screen.fill(BACKGROUND_COLOR)  # Fill the screen with the background color

    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))

    restart_text = font.render("Press R to Restart", True, (0, 255, 0))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 3 * screen_height // 4))


    pg.display.flip()   

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    return True  # Restart the game
                elif event.key == pg.K_ESCAPE:
                    exit()

        clock.tick(60)

def display_and_manage_highscores(current_score):
    print("Game Over!")

    if current_score > get_highscore():
        user_name = input("Enter your name for the highscore: ")
        save_highscore(user_name, current_score)
        print(f"New highscore saved for {user_name}!")

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Display the title
    title_text = font.render("Highscores", True, (255, 255, 255))
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))

    # Display top scores
    top_scores = get_top_scores()
    for index, (name, score) in enumerate(top_scores):
        score_text = font.render(f"{index + 1}. {name}: {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width // 4, screen_height // 4 + index * 40))
    
    # Update the screen
    pg.display.flip()
    pg.time.wait(5000)  # Pause for 5 seconds (adjust this as needed)


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
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 + index * 40))
        pg.display.flip()
        clock.tick(60)



    # Ask if user wants to delete a highscore
    option = input("Do you want to delete a highscore? (yes/no): ")
    if option.lower() == 'yes':
        name_to_delete = input("Enter the name of the player whose highscore you want to delete: ")
        delete_highscore(name_to_delete)
        print(f"Highscore for {name_to_delete} has been deleted.")
    
def draw_snake(snake):
    for index, segment in enumerate(snake):
        if index == 0:  # head
            screen.blit(snake_head_image, segment.topleft)
        else:  # body
            screen.blit(snake_body_image, segment.topleft)
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
                screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_width // 2 + index * 40))
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
                    
                    elif event.key == pg.K_ESCAPE:
                        pg.quit()
                        exit()
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
            powerup_sound.play()

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

        if (snake[0].left < 0 or snake[0].right > screen_width or
                snake[0].top < 0 or snake[0].bottom > screen_width or
                snake[0] in snake[1:]):
            death_sound.play() 
            if game_over_screen(score):
                return original_game()
            else:
                pg.quit()
                exit()

        screen.fill((0, 0, 0))
        draw_grid()
        draw_snake(snake)

        for index, segment in enumerate(snake):
            if rainbow_mode and current_time < rainbow_mode_timer:
                color_index = (current_time // 100) % len(rainbow_colors)
                color = rainbow_colors[color_index]
            else:
                color = (139, 69, 19)  # Lighter shade of brown

            pg.draw.rect(screen, color, segment)

        pg.draw.rect(screen, 'red', food)
        if power_up:
            pg.draw.ellipse(screen, 'purple', power_up)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if double_score_timer and pg.time.get_ticks() < double_score_timer:
            double_score_text = font.render('Double Score Active!', True, (255, 0, 255))
            screen.blit(double_score_text, (screen_width - double_score_text.get_width() - 10, 10))

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
            death_sound.play()
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

        if (snake[0].left < 0 or snake[0].right > screen_width or
                snake[0].top < 0 or snake[0].bottom > screen_width or
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
            screen.blit(double_score_text, (screen_width - double_score_text.get_width() - 10, 10))

        screen.blit(score_text, (10, 10))
        pg.display.flip()
        clock.tick(speed)

    display_and_manage_highscores(score)


    # This function will be similar to the original_game function but will include the maze drawing and logic.

# ================== MAIN MENU ==================
def main_menu():
    font = pg.font.SysFont(None, 48)  # Increase font size
    selected = 0
    options = ["Play Original Game", "Play Maze Game"]
    rect_width = 200  # Width of the rectangle
    rect_height = 50  # Height of the rectangle


    # Colors
    BACKGROUND_COLOR = (245, 222, 179)  # Wheat color for a sandy look
    TEXT_COLOR = (84, 51, 24)  # Dark brown color
    SELECTED_COLOR = (139, 69, 19)  # Saddle brown
    OPTION_RECT_COLOR = (160, 82, 45)  # Sienna color

    # Load the snake image
    snake_image = pg.image.load('snake img.jpeg')
    snake_image = pg.transform.scale(snake_image, (400, 400))  # Adjust the size (400x400) as needed

    while True:
        screen.fill(BACKGROUND_COLOR)

        # Decorative Elements
        # Drawing grass at the bottom
        grass_height = 25
        for i in range(0, screen_width, grass_height):  # Draw smaller rectangles for grass effect
            pg.draw.rect(screen, (101, 67, 33), (i, screen_width - grass_height, grass_height, grass_height))  # Drawing rectangles with dark brown color


        # Display the snake image
        snake_image = pg.transform.scale(snake_image, (screen_width // 3, screen_height // 3))
        screen.blit(snake_image, (screen_width // 3, screen_height // 4 - 150))

         
        title_font = pg.font.SysFont("comicsansms", 72)
        title_text_surface = title_font.render("Serphant Safari", True, TEXT_COLOR)
        title_y_position = screen_height // 4 - title_text_surface.get_height() - 20  # Adjusted position
        title_x_position = screen_width // 2 - title_text_surface.get_width() // 2
  # Adjusted position

        # Drawing a decorative border around the title
        border_thickness = 5
        border_color = (160, 82, 45)  # Sienna color for the border
        border_rect = pg.Rect(title_x_position - border_thickness, 
                            title_y_position - border_thickness, 
                            title_text_surface.get_width() + 2*border_thickness, 
                            title_text_surface.get_height() + 2*border_thickness)
        pg.draw.rect(screen, border_color, border_rect, border_radius=10)  # Drawing the border with a different border radius

        screen.blit(title_text_surface, (title_x_position, title_y_position))

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

        for index, option in enumerate(options):
            rect_x = screen_width // 4
            rect_y = screen_height // 2 + 100 + index * 60


            # Drawing the wooden signboard
            pg.draw.rect(screen, OPTION_RECT_COLOR, (rect_x, rect_y, rect_width, rect_height), border_radius=5)
            if index == selected:
                pg.draw.rect(screen, SELECTED_COLOR, (rect_x + 5, rect_y + 5, rect_width - 10, rect_height - 10), border_radius=5)

            text = font.render(option, True, TEXT_COLOR)
            text_x = screen_width // 2 - text.get_width() // 2
            text_y = rect_y + rect_height // 2 - text.get_height() // 2
            screen.blit(text, (text_x, text_y))

        pg.display.flip()
        clock.tick(60)


# ================== GAME INITIALIZATION ==================

# Get the screen resolution
info_object = pg.display.Info()
screen_width = info_object.current_w
screen_height = info_object.current_h

# Initialize the game window in full screen mode
screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN)


clock = pg.time.Clock()
font = pg.font.SysFont(None, 36)
 
# ================== START THE GAME ==================
main_menu()
