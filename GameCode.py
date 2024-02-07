import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

# Load an image
ship_image = pygame.image.load("blue.png")
scaled_ship_image = pygame.transform.scale(ship_image, (screen_width, screen_height))
screen.blit(scaled_ship_image, (0, 0))

# Close button image
close_button_image = pygame.Surface((20, 20))
close_button_image.fill((255, 0, 0))  # Red button, you can customize the color
pygame.draw.line(close_button_image, (255, 255, 255), (5, 5), (15, 15), 2)
pygame.draw.line(close_button_image, (255, 255, 255), (15, 5), (5, 15), 2)

# Create a close button
close_button_rect = close_button_image.get_rect(topleft=(0, 0))

# Load an image for the squares
square_image = pygame.image.load("Square.png")
square_size = square_image.get_size()

# Calculate the position to center the board
board_width = square_size[0] * 10  # Assuming a 10x10 board
board_height = square_size[1] * 10
board_x = (screen_width - board_width) // 2
board_y = (screen_height - board_height) // 2

# Draw the board
for y in range(10):
    for x in range(10):
        screen.blit(square_image, (board_x + x * square_size[0], board_y + y * square_size[1]))

# Main game loop
GameComplete = False
last_click_time = time.time()  # Initialize last click time
while not GameComplete:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameComplete = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Added ESC key to exit
                GameComplete = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
            if close_button_rect.collidepoint(mouse_x, mouse_y):
                GameComplete = True

            # Check if the mouse is within any square on the board
            for y in range(10):
                for x in range(10):
                    # Calculate the position of the current square
                    square_x = board_x + x * square_size[0]
                    square_y = board_y + y * square_size[1]
                    # Check if the mouse position is within the current square
                    if square_x <= mouse_x <= square_x + square_size[0] and \
                       square_y <= mouse_y <= square_y + square_size[1]:
                        # Output the coordinates of the current square
                        print("Clicked on square at position:", x, y)
                        current_time = time.time()
                        if current_time - last_click_time > 1:
                            # Get the X and Y coordinates of the mouse pointer or cursor
                            position = pygame.mouse.get_pos()
                            print(position)
                        last_click_time = current_time

    # Draw the close button
    screen.blit(close_button_image, close_button_rect)

    pygame.display.update()

# Global variable for ship positions
ship_positions = []
# Global variable for number of ships sunk
num_of_ships_sunk = 0

# Define ship lengths
ship_lengths = [1, 2, 3]

# Function to initialize ship positions
def initialize_ship_positions():
    global ship_positions
    ship_positions = []
    for length in ship_lengths:
        while True:
            orientation = random.choice(["horizontal", "vertical"])
            if orientation == "horizontal":
                start_x = random.randint(0, 9)
                start_y = random.randint(0, 9)
                ship_positions.append([(start_x + x, start_y) for x in range(length)])
                break
            else:
                start_x = random.randint(0, 9)
                start_y = random.randint(0, 9)
                ship_positions.append([(start_x, start_y + y) for y in range(length)])
                pygame.display.update()
                break

initialize_ship_positions()

# Define grid as a global variable
grid = [[0] * 10 for _ in range(10)]

ship_images = {
    1: pygame.image.load("Ship1.png"),
    2: pygame.image.load("Ship2.png"),
    3: pygame.image.load("Ship3.png"),
}

# Function to check if a shot hits a ship
def check_shot(x, y):
    for ship in ship_positions:
        if (x, y) in ship:
            return True
    return False

# Function to update game state after a shot
def update_game_state(x, y):
    global num_of_ships_sunk
    for ship in ship_positions:
        if (x, y) in ship:
            ship.remove((x, y))
            if len(ship) == 0:
                num_of_ships_sunk += 1
                print("You sunk a ship!")
                pygame.display.update()
            return

def place_ship(x, y, length):
    global grid  # Declare grid as global
    if x + length <= 10:
        if all(grid[y][x + i] == 0 for i in range(length)):
            for i in range(length):
                grid[y][x + i] = 1
            ship_positions.append([(x + i, y) for i in range(length)])
            return True
    elif y + length <= 10:
        if all(grid[y + i][x] == 0 for i in range(length)):
            for i in range(length):
                grid[y + i][x] = 1
            ship_positions.append([(x, y + i) for i in range(length)])
            return True
    return False


x = 0  # Example x coordinate
y = 0  # Example y coordinate
length = 4
if place_ship(x, y, length):
    print("Ship placed successfully!")
    pygame.display.update()

# Main game loop
# Load ship images for selection buttons
ship_selection_images = {
    1: pygame.image.load("Ship1.png"),
    3: pygame.image.load("Ship3.png"),
    2: pygame.image.load("Ship2.png"),

}

# Define ship selection button dimensions
button_width = 100
button_height = 50
button_gap = 10  # Gap between buttons

# Calculate button positions
button_x = 20
button_y = screen_height - button_height - 20
button_positions = [(button_x + (button_width + button_gap) * i, button_y) for i in range(len(ship_lengths))]

# Function to draw ship selection buttons
def draw_ship_selection_buttons():
    for i, length in enumerate(ship_lengths):
        button_rect = pygame.Rect(button_positions[i], (button_width, button_height))
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)  # Draw button outline
        button_image = pygame.transform.scale(ship_selection_images[length], (button_width, button_height))
        screen.blit(button_image, button_positions[i])


# Function to check if a ship selection button is clicked
def check_button_click(mouse_x, mouse_y):
    global selected_ship_length
    for i, position in enumerate(button_positions):
        button_rect = pygame.Rect(position, (button_width, button_height))
        if button_rect.collidepoint(mouse_x, mouse_y):
            selected_ship_length = ship_lengths[i]

            break

# Initialize selected ship length
selected_ship_length = 0

# Function to check if a ship selection button is clicked
def check_button_click(mouse_x, mouse_y):
    global selected_ship_length
    for i, position in enumerate(button_positions):
        button_rect = pygame.Rect(position, (button_width, button_height))
        if button_rect.collidepoint(mouse_x, mouse_y):
            selected_ship_length = ship_lengths[i]


# Initialize orientation variables
vertical_orientation = False

# Load orientation button images
orientation_button_images = {
    True: pygame.image.load("uparrow.png"),  # Image for vertical orientation
    False: pygame.image.load("sidewaysarrow.jfif")  # Image for horizontal orientation
}

# Define orientation button dimensions
orientation_button_width = 100
orientation_button_height = 50
orientation_button_x = 20
orientation_button_y = screen_height - orientation_button_height - 80

# Function to draw orientation button
def draw_orientation_button():
    orientation_button_rect = pygame.Rect((orientation_button_x, orientation_button_y),
                                          (orientation_button_width, orientation_button_height))
    pygame.draw.rect(screen, (255, 255, 255), orientation_button_rect, 2)  # Draw button outline
    button_image = pygame.transform.scale(orientation_button_images[vertical_orientation],
                                           (orientation_button_width, orientation_button_height))
    screen.blit(button_image, (orientation_button_x, orientation_button_y))

# Function to check if orientation button is clicked
def check_orientation_button_click(mouse_x, mouse_y):
    global vertical_orientation, selected_ship_length
    orientation_button_rect = pygame.Rect((orientation_button_x, orientation_button_y),
                                          (orientation_button_width, orientation_button_height))
    if orientation_button_rect.collidepoint(mouse_x, mouse_y):
        vertical_orientation = not vertical_orientation  # Toggle orientation
        selected_ship_length = 0  # Reset selected ship length

# Modify ship placement function to consider orientation
def place_ship(x, y, length):
    global grid, vertical_orientation
    if vertical_orientation:
        if y + length <= 10:
            if all(grid[y + i][x] == 0 for i in range(length)):
                for i in range(length):
                    grid[y + i][x] = 1
                ship_positions.append([(x, y + i) for i in range(length)])
                return True
    else:
        if x + length <= 10:
            if all(grid[y][x + i] == 0 for i in range(length)):
                for i in range(length):
                    grid[y][x + i] = 1
                ship_positions.append([(x + i, y) for i in range(length)])
                return True
    return False

# Reset ship positions and grid
ship_positions = []
grid = [[0] * 10 for _ in range(10)]

# Main game loop for ship placement phase
while len(ship_positions) < 5:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if orientation button is clicked
            check_orientation_button_click(mouse_x, mouse_y)
            # Check if ship selection button is clicked
            check_button_click(mouse_x, mouse_y)
            # Check if the click is within the board boundaries
            if board_x <= mouse_x <= board_x + board_width and \
               board_y <= mouse_y <= board_y + board_height:
                # Calculate grid position from mouse click
                grid_x = (mouse_x - board_x) // square_size[0]
                grid_y = (mouse_y - board_y) // square_size[1]
                # Place a ship starting from this position
                if selected_ship_length != 0:
                    if place_ship(grid_x, grid_y, selected_ship_length):
                        print(f"Ship of length {selected_ship_length} placed successfully!")

    # Redraw the board
    screen.fill((0, 0, 0))  # Clear the screen
    for y in range(10):
        for x in range(10):
            # Draw the square
            screen.blit(square_image, (board_x + x * square_size[0], board_y + y * square_size[1]))
            # Draw grid lines
            pygame.draw.rect(screen, (255, 255, 255),
                             (board_x + x * square_size[0], board_y + y * square_size[1], square_size[0],
                              square_size[1]), 1)

    # Draw ships on the board
    for ship in ship_positions:
        ship_length = len(ship)
        ship_image = ship_images.get(ship_length)
        if ship_image:
            for x, y in ship:
                # Calculate the position to draw the ship image
                ship_x = board_x + x * square_size[0]
                ship_y = board_y + y * square_size[1]
                if vertical_orientation:
                    # Rotate ship image by 90 degrees
                    ship_image_rotated = pygame.transform.rotate(ship_image, 90)
                    # Scale ship image to fit into the square vertically
                    ship_height = square_size[0] * ship_length
                    ship_width = square_size[1]
                    ship_image_scaled = pygame.transform.scale(ship_image_rotated, (ship_width, ship_height))
                    # Calculate adjusted position for rotated image
                    adjusted_x = ship_x + (square_size[0] - ship_width) / 2
                    adjusted_y = ship_y + (square_size[1] - ship_height) / 2
                    # Draw rotated ship image on the board
                    screen.blit(ship_image_scaled, (adjusted_x, adjusted_y))
                else:
                    # Scale ship image to fit into the square horizontally
                    ship_width = square_size[0] * ship_length
                    ship_height = square_size[1]
                    ship_image_scaled = pygame.transform.scale(ship_image, (ship_width, ship_height))
                    # Draw the scaled ship image on the board
                    screen.blit(ship_image_scaled, (ship_x, ship_y))

    # Draw ship selection buttons
    draw_ship_selection_buttons()

    # Draw orientation button
    draw_orientation_button()

    # Update the display
    pygame.display.flip()

# Next phase of the game
print("Transitioning to the next phase of the game...")
