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

