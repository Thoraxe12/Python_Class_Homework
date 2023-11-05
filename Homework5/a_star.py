from enum import Enum
from typing import Any

import numpy as np
from PIL.Image import Image

# Following timings are using the "50x50 maze" map

# 32/64bit ints produced a time range of 7.6-8.2 seconds
# 16bit ints produced a time range of 10.2-11.4 seconds
# Prior times were with float32

# Moving to 64bit float reduced runtime in range of 0.4-1.0 seconds
node_dtype = np.dtype([("x", np.int32), ("y", np.int32), ("wall", np.bool_),
                       ("g_value", np.float64), ("h_value", np.float64), ("f_value", np.float64),
                       ("px", np.int32), ("py", np.int32), ("list", np.int32)])


class ListEnum(Enum):
    NONE = 0
    OPEN = 1
    CLOSED = 2


def create_map_grid(image: Image) -> np.ndarray:
    map_grid = np.ndarray((image.height + 1, image.width + 1), dtype=node_dtype)
    for row in range(0, image.height):
        for col in range(0, image.width):
            map_grid[row][col]['x'] = row
            map_grid[row][col]['y'] = col

            if image.getpixel((row, col)) <= (25, 25, 25):
                map_grid[row][col]['wall'] = True

    return map_grid


def heuristic(node: node_dtype, goal: tuple[int, int]) -> float | Any:
    if node['wall']:
        return 1_000_000.0

    return (node['x'] - goal[0]) ** 2 + (node['y'] - goal[1]) ** 2


def get_neighbors(node: node_dtype, map_grid: np.ndarray) -> list[node_dtype]:
    x = node['x']
    y = node['y']
    nodes = []

    if x != 0:
        left_neighbor = map_grid[x - 1][y]
        nodes.append(left_neighbor)

    if x != len(map_grid) - 1:
        right_neighbor = map_grid[x + 1][y]
        nodes.append(right_neighbor)

    if y != 0:
        bottom_neighbor = map_grid[x][y - 1]
        nodes.append(bottom_neighbor)

    if y != len(map_grid[0]) - 1:
        top_neighbor = map_grid[x][y + 1]
        nodes.append(top_neighbor)

    return nodes


def find_index(open_list: list[node_dtype], f_value: np.int32) -> int:
    if len(open_list) == 0:
        return 0

    if open_list[0]['f_value'] > f_value:
        return 0

    if open_list[-1]['f_value'] < f_value:
        return len(open_list)

    low = 0
    high = len(open_list) - 1
    while low <= high:
        mid = (low + high) // 2

        if open_list[mid]['f_value'] < f_value:
            low = mid + 1
        elif open_list[mid]['f_value'] > f_value:
            high = mid - 1
        else:
            return mid

    return low


def a_star(start: tuple[int, int], end: tuple[int, int], map_grid: np.ndarray) -> list[tuple[int, int]] | None:
    open_list = [map_grid[start[0]][start[1]]]

    while len(open_list) > 0:
        current_node = open_list[0]
        open_list = open_list[1:]
        current_node['list'] = ListEnum.CLOSED.value

        if current_node['x'] == end[0] and current_node['y'] == end[1]:
            return build_path(start, end, map_grid)

        neighbors = get_neighbors(current_node, map_grid)

        for i, neighbor in enumerate(
                neighbors):

            if neighbor['list'] == ListEnum.CLOSED.value:
                continue

            g_cost = current_node['g_value'] + 1
            h_cost = heuristic(neighbor, end)
            f_cost = g_cost + h_cost

            if neighbor['list'] == ListEnum.OPEN.value and g_cost < neighbor['g_value']:
                neighbor['g_value'] = g_cost
                neighbor['h_value'] = h_cost
                neighbor['f_value'] = f_cost
                neighbor['px'] = current_node['x']
                neighbor['py'] = current_node['y']

            elif neighbor['list'] == ListEnum.NONE.value:
                neighbor['g_value'] = g_cost
                neighbor['h_value'] = h_cost
                neighbor['f_value'] = f_cost
                neighbor['px'] = current_node['x']
                neighbor['py'] = current_node['y']
                neighbor['list'] = ListEnum.OPEN.value
                if len(open_list) == 0:
                    open_list.append(neighbor)
                else:
                    open_list.insert(find_index(open_list, neighbor['f_value']), neighbor)

    return None


def build_path(start_point: tuple[int, int], end_point: tuple[int, int], map_grid: np.ndarray) -> list[tuple[int, int]]:
    x = end_point[0]
    y = end_point[1]
    path = []

    while (x, y) != start_point:
        path.append((x, y))
        x = map_grid[x][y]['px']
        y = map_grid[x][y]['py']

    path.append((x, y))
    path.reverse()
    return path
