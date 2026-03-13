from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QColor, QPolygonF, QBrush
from PyQt5.QtCore import QPointF, Qt
from math import radians, sin, cos

class RobotMarker(QGraphicsItem):
    def __init__(self, size):
         super().__init__()
         self.size = size

         h_offset = size * 0.866
         v_offset = size * 0.5

         self.triangle = QPolygonF([
             QPointF(0, -size),          # Tip (pointing up)
             QPointF(v_offset, h_offset),  # Bottom Right (cos 30, sin 30)
             QPointF(-v_offset, h_offset)  # Bottom Left
         ])

         self.setTransformOriginPoint(0, 0)

    def boundingRect(self):
         return self.triangle.boundingRect().adjusted(-2, -2, 2, 2)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("blue"))
        painter.drawPolygon(self.triangle)

class VictimMarker(QGraphicsItem):
    def __init__(self, size):
        super().__init__()
        self.size = size
        
        # Star parameters
        outer_radius = size
        inner_radius = size * 0.4  # Adjust this (0.3 to 0.5) to change "pointedness"
        points_count = 5           # Number of tips
        
        self.star = QPolygonF()
        
        # We need 10 points total (tips + valleys)
        # 360 degrees / 10 = 36 degrees per step
        for i in range(points_count * 2):
            # Alternate between outer and inner radius
            r = outer_radius if i % 2 == 0 else inner_radius
            
            # Calculate angle: subtract 90 to start at the top (pointing UP)
            angle_deg = (i * 36) - 90
            angle_rad = radians(angle_deg)
            
            # Standard Polar to Cartesian conversion
            x = r * cos(angle_rad)
            y = r * sin(angle_rad)
            
            self.star.append(QPointF(x, y))

        self.setTransformOriginPoint(0, 0)

    def boundingRect(self):
        return self.star.boundingRect().adjusted(-2, -2, 2, 2)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor("red")))
        painter.setPen(Qt.NoPen) 
        painter.drawPolygon(self.star) 