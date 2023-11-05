import time

import PIL.Image

from a_star import *
from graphics import draw_path_V2


def main() -> None:
    images_and_end_points = {
        "10x10 maze": ((73, 2), (89, 160)),
        "10x10 maze 1": ((73, 1), (89, 160)),
        "50x50 maze": ((392, 2), (408, 800)),
        "100x100 maze": ((792, 2), (809, 1600)),
    }
    images_keys = list(images_and_end_points.keys())

    image_name = images_keys[2]
    image = PIL.Image.open(image_name + ".bmp")
    image.load()

    map_grid = create_map_grid(image)

    start_time = time.time()
    result = a_star(images_and_end_points[image_name][0], images_and_end_points[image_name][1], map_grid)
    print(f"Time to complete was: {time.time() - start_time}")

    draw_path_V2(result, image_name, image)
    input("Press Enter to continue.")


main()
