import pygame as py
import sys, json

from utils.objects import EntityManager, World, create_plant, create_prey, update_display
from utils.functions import draw_grid

# Initialize the simulation
entity_manager = EntityManager()
world = World()

# Get map
with open("map.json", "r") as file:
    map_data = json.load(file)

grid_width, grid_height = map_data[0]
map_data.pop(0)

# Initialize pygame
py.init()

# Screen settings
scale_factor = 0.75
WIDTH, HEIGHT = 1920 * scale_factor, 1080 * scale_factor
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("My Pygame Window")

grid_cell_size = int(WIDTH / grid_width)

# Clock for controlling FPS
clock = py.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

create_plant(world, entity_manager.get_next_eid(), 10, 10)
create_plant(world, entity_manager.get_next_eid(), 15, 12)
create_plant(world, entity_manager.get_next_eid(), 32, 18)

world.print_info()

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # Fill screen
    screen.fill(BLACK)

    """ ALL LOGIC """
    draw_grid(screen, map_data, grid_width, WIDTH, HEIGHT, True)

    update_display(world, screen, grid_cell_size)

    # Update display
    py.display.flip()

py.quit()
sys.exit()