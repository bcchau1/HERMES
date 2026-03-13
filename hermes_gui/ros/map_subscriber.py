from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from utils.map_utils import occupancy_grid_to_qimage
from tf2_ros import Buffer, TransformListener
import rclpy

class MapSubscriber(Node):
    def __init__(self, map_signal, pose_signal):
        super().__init__('map_subscriber')
        self.map_signal = map_signal
        self.pose_signal = pose_signal
        self.latest_map_info = None

        self.sub = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.map_callback,
            10
        )

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(0.05, self.get_robot_pose)

    def map_callback(self, msg):
        self.latest_map_info = msg
        qimage = occupancy_grid_to_qimage(self.latest_map_info)
        self.map_signal.emit((qimage, self.latest_map_info))

    def get_robot_pose(self):
        if self.latest_map_info is None:
            return
        try:
            t = self.tf_buffer.lookup_transform(
                "map",          # target frame 
                "base_link",    # source frame 
                rclpy.time.Time()
            )
            self.pose_signal.emit((t.transform, self.latest_map_info))
        except:
            return
