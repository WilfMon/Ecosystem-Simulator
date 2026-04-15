import pygame as py

def draw_grid(screen, map_data, num_rect_x, width, height, show=True):
    """ Draws the grid, Number of rectangles along the x axis should be a multiple of 16"""
    CELL_SIZE = int(width / num_rect_x)
    num_rect_y = int(height / CELL_SIZE)

    if False:
        print(CELL_SIZE)
        print(num_rect_x)

    colour = (0, 0, 0)
    if show:
        colour = (255, 255, 255)

    i = 0
    for row in range(num_rect_y):
        for col in range(num_rect_x):
            rect = py.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            py.draw.rect(screen, map_data[i]["colour"], rect, 0)

            i += 1