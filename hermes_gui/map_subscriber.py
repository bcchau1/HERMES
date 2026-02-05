from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from map_utils import occupancy_grid_to_qimage

class MapSubscriber(Node):
    def __init__(self, map_signal):
        super().__init__('map_subscriber')
        self.map_signal = map_signal

        self.sub = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.map_callback,
            10
        )

    def map_callback(self, msg):
        # convert occupancy grid message to a Qt image
        qimage = occupancy_grid_to_qimage(msg)
        self.map_signal.emit(qimage)
