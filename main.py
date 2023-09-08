import pygame as pg
import sqlite3
from random import randrange

# ================== INITIALIZATION ==================
pg.init()

# Get the current display resolution
screen_info = pg.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Create a fullscreen display with a specific resolution
# Create a fullscreen display with a specific resolution
screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN)

# Switch to true fullscreen
pg.display.toggle_fullscreen()



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
    # Set the death zone to be two tiles high at the bottom of the screen



snake_image = pg.image.load('snake img.jpeg')
snake_image = pg.transform.scale(snake_image, (100000, 100000))
snake_head_image = pg.image.load('real snake img.jpeg')
snake_head_image = pg.transform.scale(snake_head_image, (TILE_SIZE, TILE_SIZE))
snake_body_image = pg.image.load('snake_body_segment.jpeg')
snake_body_image = pg.transform.scale(snake_body_image, (TILE_SIZE, TILE_SIZE))



# ================== CONSTANTS ==================





import random

MAZE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,1, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 1 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 1 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 1, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,1, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 1 , 0 , 0 , 0 , 0 , 0 ,0 , 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0 , 0, 0, 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,0 , 1],
    
    
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
DOUBLE_SCORE_DURATION = 6000  # 10 seconds in milliseconds
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
    cursor.execute("SELECT name, score FROM highscores ORDER BY score DESC LIMIT 1")

    return cursor.fetchall()

def get_highscore():
    cursor.execute('SELECT MAX(score) FROM highscores')
    return cursor.fetchone()[0] or 0

def save_highscore(name, score):
    cursor.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()

def delete_highscore(name):
    cursor.execute('DELETE FROM highscores WHERE name = ?', (name,))
    conn.commit()



def spawn_power_up(snake):
    global power_up, power_up_timer
    power_up = pg.rect.Rect(get_random_position(exclude=snake) + [TILE_SIZE, TILE_SIZE])
    power_up_timer = pg.time.get_ticks() + POWER_UP_DURATION

def get_random_position(exclude=[]):
    position = [
        randrange(0, len(MAZE[0]) - 1) * TILE_SIZE, 
        randrange(0, len(MAZE) - 1) * TILE_SIZE
    ]
    while any([pg.rect.Rect(position + [TILE_SIZE, TILE_SIZE]).colliderect(e) for e in exclude]):
        position = [
            randrange(0, len(MAZE[0]) - 1) * TILE_SIZE, 
            randrange(0, len(MAZE) - 1) * TILE_SIZE
        ]
    return position



def check_power_up_collision(snake):
    global score, power_up, power_up_timer, double_score_timer
    if snake[0].colliderect(power_up):
        power_up = None
        power_up_timer = None
        double_score_timer = pg.time.get_ticks() + DOUBLE_SCORE_DURATION
        bite_sound.play()

# ================== GAME HELPER FUNCTIONS ==================




def draw_grid():
    # Fill the screen with sandy color
    screen.fill(BACKGROUND_COLOR)

    # Drawing grid lines
    for x in range(0, screen_width, TILE_SIZE):
        pg.draw.line(screen, GRID_COLOR, (x, 0), (x, screen_height))
    
    # Adjusting the maximum y-value so that the grid ends at the last complete tile
    max_y = (screen_height // TILE_SIZE) * TILE_SIZE
    
    for y in range(0, max_y, TILE_SIZE):
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

    main_menu_text = font.render("Press M for Main Menu", True, (0, 255, 0))
    screen.blit(main_menu_text, (screen_width // 2 - main_menu_text.get_width() // 2, 3 * screen_height // 4 + 40))
    
    pg.display.flip() 

    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    return "restart"  # Restart the game
                elif event.key == pg.K_m:
                    return "main_menu"
                elif event.key == pg.K_ESCAPE:
                    exit()

        clock.tick(60)

    # After the game over loop, check if the current score is a highscore
        if score > get_highscore():
        # This section is pseudo-code because Pygame doesn't support native input boxes. 
        # You would need to use a library like "pgu" or build a custom input box.
            user_name = input("Enter your name for the highscore: ")  # Get player's name using your preferred method
            save_highscore(user_name, score)
            
            # Display the high scores
            display_and_manage_highscores(score)








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
    grass_height = 25
    max_y_position = screen_height - grass_height  # Maximum y position before the grass starts
    rainbow_colors = [
        (255, 0, 0), (255, 165, 0), (255, 255, 0),
        (0, 255, 0), (0, 0, 255), (75, 0, 130),
        (238, 130, 238)
    ]
    rainbow_mode = False
    rainbow_mode_timer = 0
    
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

        current_time = pg.time.get_ticks()
        if not power_up and current_time - last_power_up_spawn_time >= 7000:
            spawn_power_up(snake)
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
            snake[0].top < 0 or snake[0].bottom > screen_height or
            snake[0].bottom > screen_height or
            snake[0] in snake[1:]):
            death_sound.play() 
            game_over_result = game_over_screen(score)
            if game_over_result == "restart":
                return original_game()
            elif game_over_result == "main_menu":
                return main_menu()
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


def maze_game():
    global MAZE  # Referencing the global MAZE to modify it in this function
 

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

       
        maze_x, maze_y = head.topleft[0] // TILE_SIZE, head.topleft[1] // TILE_SIZE
        if maze_y < 0 or maze_y >= len(MAZE) or maze_x < 0 or maze_x >= len(MAZE[0]) or MAZE[maze_y][maze_x] == 1:
            death_sound.play()
            game_over_result = game_over_screen(score)
            if game_over_result == "restart":
                return maze_game()
            elif game_over_result == "main_menu":
                return main_menu()
            else:
                pg.quit()
                exit()

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
                snake[0].top < 0 or snake[0].bottom > screen_height or
                snake[0] in snake[1:]):
            break

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
    pg.init()
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Snake Game")

    font = pg.font.SysFont(None, 42)  # Increase font size
    selected = 0
    options = ["Play Original Game", "Play Maze Game", "Instructions"]  # Added an "Instructions" option
    rect_width = 300  # Increased width of the rectangle for better fit
    rect_height = 60  # Increased height of the rectangle for better fit

    # Colors
    BACKGROUND_COLOR = (245, 222, 179)
    TEXT_COLOR = (84, 51, 24)
    SELECTED_COLOR = (139, 69, 19)
    OPTION_RECT_COLOR = (160, 82, 45)

    # Load the snake image
    snake_image = pg.image.load('snake img.jpeg')
    # Adjust the image size to a proportion that ensures clarity
    img_width = min(snake_image.get_width(), screen_width // 3)
    img_height = min(snake_image.get_height(), screen_height // 3)
    snake_image = pg.transform.scale(snake_image, (img_width, img_height))

    clock = pg.time.Clock()

    while True:
        screen.fill(BACKGROUND_COLOR)

        # Drawing grass at the bottom
        grass_height = 25
        for i in range(0, screen_width, grass_height):
            pg.draw.rect(screen, (101, 67, 33), (i, screen_height - grass_height, grass_height, grass_height))

        # Display title
        title_font = pg.font.SysFont("comicsansms", 72)
        title_text_surface = title_font.render("Serphant Safari", True, TEXT_COLOR)
        title_y_position = screen_height // 6  # Positioned a bit above the center for better spacing
        title_x_position = screen_width // 2 - title_text_surface.get_width() // 2

        # Drawing a decorative border around the title
        border_thickness = 5
        border_color = (160, 82, 45)
        border_rect = pg.Rect(title_x_position - border_thickness,
                              title_y_position - border_thickness,
                              title_text_surface.get_width() + 2 * border_thickness,
                              title_text_surface.get_height() + 2 * border_thickness)
        pg.draw.rect(screen, border_color, border_rect, border_radius=10)
        screen.blit(title_text_surface, (title_x_position, title_y_position))

        # Display snake image below the title
        snake_image_y_position = title_y_position + title_text_surface.get_height() + 20  # Give it some space below the title
        screen.blit(snake_image, (screen_width // 2 - snake_image.get_width() // 2, snake_image_y_position))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    selected = (selected + 1) % len(options)  # Updated to handle variable options length
                elif event.key == pg.K_UP:
                    selected = (selected - 1) % len(options)  # Updated to handle variable options length
                elif event.key == pg.K_RETURN:
                    if selected == 0:
                        original_game()
                    elif selected == 1:
                        maze_game()
                    else:
                        display_instructions()  # Call a new function to display instructions
                    return

        # Displaying menu options
        for index, option in enumerate(options):
            rect_x = screen_width // 2 - rect_width // 2  # Centering the option rectangles
            rect_y = snake_image_y_position + snake_image.get_height() + 40 + index * 80  # Below the snake image with some spacing

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

# Add a function to display instructions
def display_instructions():
    pg.init()
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Instructions")

    font = pg.font.SysFont(None, 36)  # Set the font size for instructions

    INSTRUCTIONS_TEXT = [
        "Welcome to the Serphant Safari!",
        "",
        "Original Game:",
        "Use arrow keys to navigate the snake and eat food to gain points and grow.",
        "Power-ups double your points for 7 seconds.",
        "",
        "Maze Game:",
        "Navigate the maze without touching the blue walls to succeed.",
        "",
        "Now, embark on your safari adventure!",
        "Press the 'B' key to return to the main menu.",
    ]

    BACKGROUND_COLOR = (245, 222, 179)
    TEXT_COLOR = (84, 51, 24)

    clock = pg.time.Clock()

    while True:
        screen.fill(BACKGROUND_COLOR)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return  # Return to the main menu if window is closed
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_b:
                    main_menu()  # Return to the main menu by calling main_menu() function

        # Display instructions text
        text_y = 20
        for line in INSTRUCTIONS_TEXT:
            text_surface = font.render(line, True, TEXT_COLOR)
            text_x = screen_width // 2 - text_surface.get_width() // 2
            screen.blit(text_surface, (text_x, text_y))
            text_y += text_surface.get_height() + 10

        pg.display.flip()
        clock.tick(60)


    while True:
        screen.fill(BACKGROUND_COLOR)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return  # Return to the main menu if window is closed
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_b:
                    return

        # Display instructions text
        text_y = 20
        for line in INSTRUCTIONS_TEXT:
            text_surface = font.render(line, True, TEXT_COLOR)
            text_x = screen_width // 2 - text_surface.get_width() // 2
            screen.blit(text_surface, (text_x, text_y))
            text_y += text_surface.get_height() + 10

        pg.display.flip()
        clock.tick(60)



# You can call main_menu() to start the menu loop.
# main_menu()




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

