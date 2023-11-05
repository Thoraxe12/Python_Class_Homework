import tkinter as tk
import turtle

import PIL.Image
import pygame.image
from pygame import Color


# Changed the draw method to pygame only.
# This fixed the world coordinates starting at center screen
def draw_path_V2(path: list[tuple[int, int]], image_name: str, image: PIL.Image.Image) -> None:
    """
    :param path: List of X,Y coordinates
    :param image_name: File name without extension
    :param image: A PIL Image. Used for Width and Height
    :return: None
    """
    pygame.init()
    screen = pygame.display.set_mode((image.width, image.height))
    pygame_image = pygame.image.load(image_name + ".png")
    screen.blit(pygame_image, (0, 0))
    pygame.display.flip()

    for pixel in path:
        screen.set_at(pixel, Color(255, 0, 0, 255))
        pygame.display.flip()


def draw_path(path: list[tuple[int, int]], image_name: str, image: PIL.Image.Image) -> None:
    my_turtle = turtle.Turtle()
    screen = turtle.Screen()
    screen.reset()
    screen.setup(image.width + 100, image.height + 100)
    screen.setworldcoordinates(-100, image.height, image.width, -100)

    canvas = turtle.getcanvas()
    background_image = tk.PhotoImage(file=image_name + ".png")
    background_image_id = canvas.create_image(-100, -100, image=background_image)
    canvas.itemconfig(background_image_id, anchor="nw")

    my_turtle.penup()
    my_turtle.goto(path[0][0] - 100, path[0][1] - 100)
    my_turtle.pendown()

    for location in path:
        if location == path[0]:
            continue

        my_turtle.goto(location[0] - 100, location[1] - 100)
