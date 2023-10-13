import tkinter as tk
from tkinter import simpledialog  # Import the simpledialog module separately
import random

# Global constants
GAME_WIDTH = 1500
GAME_HEIGHT = 1000
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Initialize the main window
window = tk.Tk()
window.title("Snake Game")

# Center the window on the screen
window_width = window.winfo_reqwidth()
window_height = window.winfo_reqheight()
position_x = int((window.winfo_screenwidth() / 2) - (window_width / 2))
position_y = int((window.winfo_screenheight() / 2) - (window_height / 2))
window.geometry("+{}+{}".format(position_x, position_y))

# Create global variables for the game
snake = None
food = None
score = 0
direction = 'right'

# Create the leaderboard
leaderboard = []

# Create the game canvas
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR,
                   height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Create the game label
label = tk.Label(window, text="Score: {}".format(score), font=('consolas', 20))
label.pack()


# Define the Snake class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


# Define the Food class
class Food:
    def __init__(self):
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y +
                           SPACE_SIZE, fill=FOOD_COLOR, tag="food")


# Function to start the game
def start_game():
    global snake, food, score, direction

    # Reset game variables
    score = 0
    direction = 'right'
    label.config(text="Score: {}".format(score))
    canvas.delete("all")

    # Create a new snake and food
    snake = Snake()
    food = Food()

    # Start the game loop
    next_turn(snake, food)


# Function to display the leaderboard
def show_leaderboard():
    # Create a new window for the leaderboard
    leaderboard_window = tk.Toplevel(window)
    leaderboard_window.title("Leaderboard")

    # Read the leaderboard file and display the scores
    with open("leaderboard.txt", "r") as leaderboard_file:
        leaderboard_data = leaderboard_file.readlines()

    leaderboard_data.sort(
        key=lambda x: int(x.split(":")[1]), reverse=True)  # Sort by scores

    leaderboard_text = "\n".join(leaderboard_data)

    leaderboard_label = tk.Label(
        leaderboard_window, text="Leaderboard", font=('consolas', 20))
    leaderboard_label.pack()

    leaderboard_text_widget = tk.Text(
        leaderboard_window, font=('consolas', 12), height=10, width=30)
    leaderboard_text_widget.insert(tk.END, leaderboard_text)
    leaderboard_text_widget.pack()

    # Create a button to go back to the main menu
    back_button = tk.Button(
        leaderboard_window, text="Back to Main Menu", command=leaderboard_window.destroy)
    back_button.pack()


# Function to handle game over
def game_over():
    canvas.delete("all")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2,
                       font=('consolas', 30), text="GAME OVER", fill="red")

    # Ask the player for their name
    player_name = simpledialog.askstring(
        "Enter your name", "Enter your name:")
    if player_name:
        # Open the leaderboard file in append mode and write the player's name and score
        with open("leaderboard.txt", "a") as leaderboard_file:
            leaderboard_file.write(f"{player_name}: {score}\n")

        # Display the updated leaderboard
        show_leaderboard()


# Function to move the snake
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


# Function to change the snake's direction
def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


# Function to check for collisions
def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


# Function to handle keyboard input
def on_arrow_key(event):
    if event.keysym == "Up":
        change_direction("up")
    elif event.keysym == "Down":
        change_direction("down")
    elif event.keysym == "Left":
        change_direction("left")
    elif event.keysym == "Right":
        change_direction("right")


# Bind arrow keys to the on_arrow_key function
window.bind("<Up>", on_arrow_key)
window.bind("<Down>", on_arrow_key)
window.bind("<Left>", on_arrow_key)
window.bind("<Right>", on_arrow_key)


# Function to show the settings
def show_settings():
    global settings_window  # Make settings_window a global variable
    settings_window = tk.Toplevel(window)
    settings_window.title("Settings")

    speed_label = tk.Label(
        settings_window, text="Speed (ms):", font=('consolas', 14))
    speed_label.pack()

    speed_slider = tk.Scale(settings_window, from_=50, to=300, orient="horizontal")
    speed_slider.set(SPEED)
    speed_slider.pack()

    apply_button = tk.Button(settings_window, text="Apply", command=lambda: apply_settings(speed_slider.get()))
    apply_button.pack()

# Function to apply the settings
def apply_settings(new_speed):
    global SPEED
    SPEED = new_speed
    settings_window.destroy()
    start_game()

# Create a button to start the game
start_button = tk.Button(window, text="Start", command=start_game)
start_button.pack(pady=10)

# Create a button to show the leaderboard
leaderboard_button = tk.Button(
    window, text="Leaderboard", command=show_leaderboard)
leaderboard_button.pack(pady=10)

# Create a button to show the settings
settings_button = tk.Button(window, text="Settings", command=show_settings)
settings_button.pack(pady=10)

# Start the tkinter main loop
window.mainloop()
