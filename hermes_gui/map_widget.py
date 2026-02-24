from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF

class MapWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.map_item = None

    def update_map(self, qimage):
        pixmap = QPixmap.fromImage(qimage.mirrored(False, True))

        if self.map_item is None:
            self.map_item = self.scene.addPixmap(pixmap)
        else:
            self.map_item.setPixmap(pixmap)

        self.setSceneRect(QRectF(pixmap.rect()))
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def reset_map(self):
        self.scene.clear()
        self.map_item = None