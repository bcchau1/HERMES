import numpy as np
from PyQt5.QtGui import QImage

def occupancy_grid_to_qimage(msg):
    width = msg.info.width
    height = msg.info.height
    data = np.array(msg.data, dtype=np.int8).reshape((height, width))

    image = np.zeros((height, width), dtype=np.uint8)
    image[data == -1] = 127     # unknown
    image[data == 0] = 255      # free
    image[data > 0] = 0         # occupied

    return QImage(
        image.data,
        width,
        height,
        width,
        QImage.Format_Grayscale8
    ).copy()  # copy to prevent dangling memory
