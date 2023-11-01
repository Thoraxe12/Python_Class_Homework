import ctypes
import multiprocessing
import pathlib
import sys
import time
import tkinter
import turtle
from ctypes import CDLL, c_int
from ctypes.util import find_library
from typing import Any

import joblib
import numpy as np
from PIL import Image

from joblib import delayed, parallel, Parallel
from numba import jit, njit

# node_dtype = np.dtype([("x", np.int16), ("y", np.int16), ("wall", np.bool_),
#                        ("g_value", np.float64), ("h_value", np.float64), ("f_value", np.float64),
#                        ("parent", np.object_)])

node_dtype = np.dtype([("x", np.int16), ("y", np.int16), ("wall", np.bool_),
                       ("g_value", np.float64), ("h_value", np.float64), ("f_value", np.float64),
                       ("parent", n)])


def create_node(x: int, y: int, parent: object, wall: bool, g: float, h: float, f: float) -> object:
    node = np.empty(1, node_dtype)

    node['x'] = x
    node['y'] = y
    node['parent'] = parent
    node['wall'] = wall
    node['g_value'] = g
    node['h_value'] = h
    node['f_value'] = f

    return node


def heuristic(node: node_dtype, goal: node_dtype) -> float | Any:
    if node['wall']:
        return 1_000_000.0

    return (node['x'] - goal['x']) ** 2 + (node['y'] - goal['y']) ** 2


def build_path(end_node: node_dtype) -> list[tuple[int, int]]:
    node = end_node
    path = []

    while node['parent'] is not None:
        path.append((node['x'], node['y']))
        node = node['parent']

    path.append((node['x'], node['y']))
    path.reverse()
    return path


def get_neighbors(node: node_dtype, map_file: Image) -> list[node_dtype]:
    x = node['x']
    y = node['y']
    nodes = []

    if x != 0:
        left_neighbor = create_node(x - 1, y, node, False, 0, 0, 0)
        if map_file.getpixel((left_neighbor['x'], left_neighbor['y'])) <= (25, 25, 25):
            left_neighbor['wall'] = True
        nodes.append(left_neighbor)

    if x != map_file.width - 1:
        right_neighbor = create_node(x + 1, y, node, False, 0, 0, 0)
        if map_file.getpixel((right_neighbor['x'], right_neighbor['y'])) <= (25, 25, 25):
            right_neighbor['wall'] = True
        nodes.append(right_neighbor)

    if y != 0:
        bottom_neighbor = create_node(x, y - 1, node, False, 0, 0, 0)
        if map_file.getpixel((bottom_neighbor['x'], bottom_neighbor['y'])) <= (25, 25, 25):
            bottom_neighbor['wall'] = True
        nodes.append(bottom_neighbor)

    if y != map_file.height - 1:
        top_neighbor = create_node(x, y + 1, node, False, 0, 0, 0)
        if map_file.getpixel((top_neighbor['x'], top_neighbor['y'])) <= (25, 25, 25):
            top_neighbor['wall'] = True
        nodes.append(top_neighbor)

    return nodes


def compare_structs(struct1, struct2) -> bool:
    """
    :param struct1: The first structure
    :param struct2: The second structure
    :return: Returns true if the x and y values are the same for both structures
    """

    result = struct1['x'] == struct2['x'] and struct1['y'] == struct2['y']
    return result


def check_structure_in_array(array, struct) -> bool:
    """
    :param array: The numpy array
    :param struct: The structure to test if is in the array
    :return: Return true if the structure exist inside the array
    """

    for element in array:
        if compare_structs(element, struct):
            return True

    return False


def a_star(start: tuple[int, int], end: tuple[int, int], map_file: Image) -> list[tuple[int, int]] | None:
    open_list = np.empty(1, node_dtype)
    closed_list = []

    open_list.itemset(0, (create_node(
        start[0], start[1], None, False,
        0.0, 0.0, 0.0)))

    end_node = create_node(end[0], end[1], None, False,
                           0.0, 0.0, 0.0)

    while len(open_list) > 0:
        if len(open_list) > 1:
            record_array = open_list.view(np.recarray)
            sorted_indices = np.lexsort([record_array['f_value']])
            open_list = open_list[sorted_indices]

            current_node = open_list[0]
            open_list = open_list[1:]
        else:
            current_node = open_list[0]
            open_list = open_list[1:]

        closed_list.append(current_node)

        if current_node['x'] == end_node['x'] and current_node['y'] == end_node['y']:
            return build_path(current_node)

        for i, neighbor in enumerate(
                get_neighbors(current_node, map_file)):

            if check_structure_in_array(closed_list, neighbor):
                continue

            g_cost = current_node['g_value'] + 1
            h_cost = heuristic(neighbor, end_node)
            f_cost = g_cost + h_cost

            in_open_list = check_structure_in_array(open_list, neighbor)

            if in_open_list and g_cost < neighbor['g_value']:
                neighbor['g_value'] = g_cost
                neighbor['h_value'] = h_cost
                neighbor['f_value'] = f_cost
                continue
            elif not in_open_list:
                neighbor['g_value'] = g_cost
                neighbor['h_value'] = h_cost
                neighbor['f_value'] = f_cost
                open_list = np.concatenate((open_list, neighbor))

    return None


def draw_path(path: list[tuple[int, int]], image_name: str, image: Image) -> None:
    my_turtle = turtle.Turtle()
    screen = turtle.Screen()
    screen.reset()
    screen.setup(image.width + 100, image.height + 100)
    screen.setworldcoordinates(-100, image.height, image.width, -100)

    canvas = turtle.getcanvas()
    background_image = tkinter.PhotoImage(file=image_name + ".png")
    background_image_id = canvas.create_image(-100, -100, image=background_image)
    canvas.itemconfig(background_image_id, anchor="nw")

    my_turtle.penup()
    my_turtle.goto(path[0][0] - 100, path[0][1] - 100)
    my_turtle.pendown()

    for location in path:
        if location == path[0]:
            continue

        my_turtle.goto(location[0] - 100, location[1] - 100)


def main() -> None:
    sys.setrecursionlimit(10_000)

    images_and_end_points = {
        "10x10 maze": ((73, 2), (89, 160)),
        "10x10 maze 1": ((73, 1), (89, 160))
    }
    images_keys = list(images_and_end_points.keys())

    image_name = images_keys[0]
    image = Image.open(image_name + ".bmp")
    image.load()

    start_time = time.time()
    result = a_star(images_and_end_points[image_name][0], images_and_end_points[image_name][1], image)
    print(f"Time to complete was: {time.time() - start_time}")

    draw_path(result, image_name, image)
    print(result)
    input("Press Enter to continue.")


main()
