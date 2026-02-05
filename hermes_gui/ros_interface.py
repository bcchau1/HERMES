import threading
from PyQt5.QtCore import QObject, pyqtSignal
from map_subscriber import MapSubscriber
import rclpy

class RosInterface(QObject):
    map_updated = pyqtSignal(object)  # defines pyqtSignal that can carry any Python object (we will use QImage)

    def __init__(self):
        super().__init__()

        self.node = MapSubscriber(self.map_updated)

        self.thread = threading.Thread(
            target=rclpy.spin,
            args=(self.node,),
            daemon=True
        )
        self.thread.start()

    def shutdown(self):
        self.node.destroy_node()
