import threading
from PyQt5.QtCore import QObject, pyqtSignal
from ros.map_subscriber import MapSubscriber
from ros.victim_subscriber import VictimSubscriber
import rclpy

class RosInterface(QObject):
    map_updated = pyqtSignal(object)
    pose_updated = pyqtSignal(object)
    victim_detected = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self.node = MapSubscriber(self.map_updated, self.pose_updated)
        self.victim_node = VictimSubscriber(self.victim_detected)

        self.thread = threading.Thread(
            target=rclpy.spin,
            args=(self.node,),
            daemon=True
        )
        self.thread.start()

    def shutdown(self):
        self.node.destroy_node()
