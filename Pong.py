import tkinter as tk
import random

# Game settings
WIDTH = 900
HEIGHT = 600

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

BALL_SIZE = 20

PADDLE_SPEED = 8
BALL_SPEED_X = 6
BALL_SPEED_Y = 4

WINNING_SCORE = 10

# Game variables
player1_score = 0
player2_score = 0

game_over = False

ball_dx = BALL_SPEED_X
ball_dy = BALL_SPEED_Y

# Create window
window = tk.Tk()
window.title("Two Player Pong")
window.resizable(False, False)

# Score display
score_label = tk.Label(
    window,
    text="0       0",
    font=("Arial", 32),
    bg="black",
    fg="white"
)

score_label.pack(fill="x")

# Game canvas
canvas = tk.Canvas(
    window,
    width=WIDTH,
    height=HEIGHT,
    bg="black",
    highlightthickness=0
)

canvas.pack()

# Create paddles
player1 = canvas.create_rectangle(
    30,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    30 + PADDLE_WIDTH,
    HEIGHT // 2 + PADDLE_HEIGHT // 2,
    fill="white"
)

player2 = canvas.create_rectangle(
    WIDTH - 30 - PADDLE_WIDTH,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    WIDTH - 30,
    HEIGHT // 2 + PADDLE_HEIGHT // 2,
    fill="white"
)

# Create ball
ball = canvas.create_oval(
    WIDTH // 2 - BALL_SIZE // 2,
    HEIGHT // 2 - BALL_SIZE // 2,
    WIDTH // 2 + BALL_SIZE // 2,
    HEIGHT // 2 + BALL_SIZE // 2,
    fill="white"
)

# Create center line
for y in range(0, HEIGHT, 30):
    canvas.create_rectangle(
        WIDTH // 2 - 2,
        y,
        WIDTH // 2 + 2,
        y + 15,
        fill="white"
    )

# Keyboard controls
keys = set()


def key_pressed(event):
    keys.add(event.keysym)


def key_released(event):
    keys.discard(event.keysym)


window.bind("<KeyPress>", key_pressed)
window.bind("<KeyRelease>", key_released)


def move_paddles():
    # Player 1 movement
    if "w" in keys or "W" in keys:
        canvas.move(player1, 0, -PADDLE_SPEED)

    if "s" in keys or "S" in keys:
        canvas.move(player1, 0, PADDLE_SPEED)

    # Player 2 movement
    if "Up" in keys:
        canvas.move(player2, 0, -PADDLE_SPEED)

    if "Down" in keys:
        canvas.move(player2, 0, PADDLE_SPEED)

    # Keep paddles inside the screen
    keep_paddle_inside(player1)
    keep_paddle_inside(player2)


def keep_paddle_inside(paddle):
    position = canvas.coords(paddle)

    top = position[1]
    bottom = position[3]

    if top < 0:
        canvas.move(paddle, 0, -top)

    if bottom > HEIGHT:
        canvas.move(paddle, 0, HEIGHT - bottom)


def move_ball():
    global ball_dx, ball_dy

    canvas.move(ball, ball_dx, ball_dy)

    position = canvas.coords(ball)

    ball_left = position[0]
    ball_top = position[1]
    ball_right = position[2]
    ball_bottom = position[3]

    # Bounce off the top and bottom walls
    if ball_top <= 0:
        ball_dy = abs(ball_dy)

    if ball_bottom >= HEIGHT:
        ball_dy = -abs(ball_dy)

    # Check paddle collisions
    ball_position = canvas.coords(ball)

    player1_position = canvas.coords(player1)
    player2_position = canvas.coords(player2)

    # Player 1 collision
    if collision(ball_position, player1_position):
        ball_dx = abs(ball_dx)

        paddle_center = player1_position[1] + PADDLE_HEIGHT / 2
        ball_center = ball_top + BALL_SIZE / 2

        difference = ball_center - paddle_center

        ball_dy = difference / 10

    # Player 2 collision
    if collision(ball_position, player2_position):
        ball_dx = -abs(ball_dx)

        paddle_center = player2_position[1] + PADDLE_HEIGHT / 2
        ball_center = ball_top + BALL_SIZE / 2

        difference = ball_center - paddle_center

        ball_dy = difference / 10

    # Player 2 scores
    if ball_left <= 0:
        score_point(2)

    # Player 1 scores
    if ball_right >= WIDTH:
        score_point(1)


def collision(object1, object2):
    return (
        object1[0] < object2[2]
        and object1[2] > object2[0]
        and object1[1] < object2[3]
        and object1[3] > object2[1]
    )


def score_point(player):
    global player1_score, player2_score

    if player == 1:
        player1_score += 1
    else:
        player2_score += 1

    score_label.config(
        text=f"{player1_score}       {player2_score}"
    )

    # Check for a winner
    if player1_score >= WINNING_SCORE:
        end_game("PLAYER 1 WINS!")

    elif player2_score >= WINNING_SCORE:
        end_game("PLAYER 2 WINS!")

    else:
        reset_ball()


def reset_ball():
    global ball_dx, ball_dy

    canvas.coords(
        ball,
        WIDTH // 2 - BALL_SIZE // 2,
        HEIGHT // 2 - BALL_SIZE // 2,
        WIDTH // 2 + BALL_SIZE // 2,
        HEIGHT // 2 + BALL_SIZE // 2
    )

    # Randomize ball direction
    ball_dx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
    ball_dy = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])


def end_game(message):
    global game_over

    game_over = True

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 - 40,
        text=message,
        fill="white",
        font=("Arial", 40, "bold"),
        tags="game_over"
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 20,
        text="Press R to restart",
        fill="white",
        font=("Arial", 20),
        tags="game_over"
    )


def restart_game(event=None):
    global player1_score, player2_score, game_over

    if not game_over:
        return

    player1_score = 0
    player2_score = 0

    game_over = False

    score_label.config(text="0       0")

    canvas.delete("game_over")

    # Reset paddles
    canvas.coords(
        player1,
        30,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        30 + PADDLE_WIDTH,
        HEIGHT