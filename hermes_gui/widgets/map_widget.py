from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF
from widgets.map_markers import RobotMarker, VictimMarker
from utils.map_utils import world_to_pixel
from math import atan2, degrees

class MapWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.map_item = None
        self.occupancy_grid = None

        self.robot_marker = RobotMarker(size=4)
        
        '''
        Dictionary to store victim markers. This allows for easier recompute of coordinates
        when the map is updated.

        self.victims = {
            victim_id: {
                "marker": VictimMarker,
                "world": (x, y)
            }
        }
        '''
        self.victims = {}
        self.pending_victims = []

    def update_map(self, payload):
        qimage, self.occupancy_grid = payload
        pixmap = QPixmap.fromImage(qimage.mirrored(False, True))

        if self.map_item is None:
            self.map_item = self.scene.addPixmap(pixmap)
            self.scene.addItem(self.robot_marker)
        else:
            self.map_item.setPixmap(pixmap)

        self.setSceneRect(QRectF(pixmap.rect()))
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        self.update_victim_positions()

    def update_pose(self, payload):
        """Slot to receive (transform, occupancy_grid_msg) tuples from ROS.
        transform is a geometry_msgs/Transform, occupancy_grid_msg is an
        nav_msgs/OccupancyGrid message.
        """
        try:
            transform, occupancy_grid = payload
        except Exception:
            return

        if occupancy_grid is None or self.map_item is None:
            return

        tx = transform.translation.x
        ty = transform.translation.y
        px, py = world_to_pixel(tx, ty, occupancy_grid.info)

        # yaw calculation using quaternions
        qx = transform.rotation.x
        qy = transform.rotation.y
        qz = transform.rotation.z
        qw = transform.rotation.w
        yaw = atan2(2*(qw*qz + qx*qy), 1 - 2*(qy*qy + qz*qz))

        if self.robot_marker.scene() is None:
            self.scene.addItem(self.robot_marker)

        self.robot_marker.setPos(px, py)
        self.robot_marker.setRotation(-degrees(yaw))

    def reset_map(self):
        if self.map_item is not None:
            self.scene.removeItem(self.map_item)
            self.scene.removeItem(self.robot_marker)
            self.map_item = None

    def add_victim(self, msg):
        victim = VictimMarker(size=3)
        victim_id = len(self.victims)
        self.victims[victim_id] = {
            "marker": victim,
            "world": (msg.x, msg.y)
        }

        self.scene.addItem(victim)
        self.update_victim_position()

    def update_victim_positions(self):
        if self.map_item is not None:
            return

        for victim in self.victims.values():
            vx, vy = victim["world"]
            px, py = world_to_pixel(vx, vy, self.occupancy_grid.info)
            victim["marker"].setPos(px, py)
