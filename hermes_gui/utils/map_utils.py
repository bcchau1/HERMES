import numpy as np
from PyQt5.QtGui import QImage

def occupancy_grid_to_qimage(msg):
    w, h = msg.info.width, msg.info.height
    data = np.array(msg.data, dtype=np.int8).reshape((h, w))

    # rotate data because QImage origin is different from ROS2
    data = np.rot90(data, k = -1)
    new_height, new_width = data.shape

    # numpy boolean indexing
    image = np.zeros((new_height, new_width), dtype=np.uint8)
    image[data == -1] = 127     # unknown
    image[data == 0] = 255      # free
    image[data > 0] = 0         # occupied

    return QImage(
        image.data,
        new_width,
        new_height,
        new_width,
        QImage.Format_Grayscale8
    ).copy()

def world_to_pixel(x, y, map_info):
    origin_x = map_info.origin.position.x
    origin_y = map_info.origin.position.y
    w, h = map_info.width, map_info.height

    pixel_x = (x - origin_x) / map_info.resolution
    pixel_y = (y - origin_y) / map_info.resolution
    pixel_y = h - pixel_y - 1     # invert y-axis to adjust for map rotation

    # adjust for 90 degrees rotation
    px_rot = pixel_y
    py_rot = w - pixel_x

    return px_rot, py_rot 
