from rclpy.node import Node
from geometry_msgs.msg import PointStamped

class VictimSubscriber(Node):
    def __init__(self, victim_point_signal):
        super().__init__("victim_subscriber")
        self.victim_point_signal = victim_point_signal
        
        self.sub = self.create_subscription(
            PointStamped,
            "/victim_point",
            self.victim_point_callback,
            10
        )

    def victim_point_callback(self, msg):
        self.victim_point_signal.emit(msg.point)