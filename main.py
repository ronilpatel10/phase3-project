import pygame as pg
import sqlite3
from random import randrange
from config import *
from database import *
from utils import *

# Initialize pygame
pg.init()

# Load sound effect
bite_sound = pg.mixer.Sound('bite.wav')

# Constants
WINDOW = 700
TILE_SIZE = 50
RANGE = (0, WINDOW // TILE_SIZE - 1)
SPEED_INCREMENT = 1

# Database Setup
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

# Game Functions
get_random_position = lambda: [randrange(*RANGE) * TILE_SIZE for _ in range(2)]

def draw_grid():
    for x in range(0, WINDOW, TILE_SIZE):
        pg.draw.line(screen, (50, 50, 50), (x, 0), (x, WINDOW))
    for y in range(0, WINDOW, TILE_SIZE):
        pg.draw.line(screen, (50, 50, 50), (0, y), (WINDOW, y))

# Game setup
snake = [pg.rect.Rect([0, 0, TILE_SIZE, TILE_SIZE])]
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
food = pg.rect.Rect(get_random_position() + [TILE_SIZE, TILE_SIZE])
direction = (TILE_SIZE, 0)
score = 0
speed = 10
font = pg.font.SysFont(None, 36)

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

    if snake[0].colliderect(food):
        bite_sound.play()  # Play the bite sound effect
        food.topleft = get_random_position()
        score += 1
        speed += SPEED_INCREMENT
    else:
        snake.pop()

    if (snake[0].left < 0 or snake[0].right > WINDOW or
            snake[0].top < 0 or snake[0].bottom > WINDOW or
            snake[0] in snake[1:]):
        break

    screen.fill((0, 0, 0))
    draw_grid()
    [pg.draw.rect(screen, 'green', segment) for segment in snake]
    pg.draw.rect(screen, 'red', food)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pg.display.flip()
    clock.tick(speed)

print("Game Over!")

if score > get_highscore():
    user_name = input("Enter your name for the highscore: ")
    save_highscore(user_name, score)
    print(f"New highscore saved for {user_name}!")

# Display top scores
screen.fill((0, 0, 0))
top_scores = get_top_scores()
for index, (name, score) in enumerate(top_scores):
    score_text = font.render(f"{index + 1}. {name}: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WINDOW // 4, WINDOW // 4 + index * 40))
pg.display.flip()
pg.time.wait(5000)

# Ask if user wants to delete a highscore
option = input("Do you want to delete a highscore? (yes/no): ")
if option.lower() == 'yes':
    name_to_delete = input("Enter the name of the player whose highscore you want to delete: ")
    delete_highscore(name_to_delete)
    print(f"Highscore for {name_to_delete} has been deleted.")

conn.close()
