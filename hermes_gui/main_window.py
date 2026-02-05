from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QFrame
)
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt
import sys

# from PyQt5.QtWidgets import (
#     QMainWindow,
#     QWidget,
#     QHBoxLayout,
#     QVBoxLayout,
#     QLabel, 
# )
# from PyQt5.QtGui import QGuiApplication
# from map_widget import MapWidget

# class MainWindow(QMainWindow):
#     def __init__(self, ros):
#         super().__init__()

#         self.setWindowTitle("HERMES")

#         # adjust GUI size according to current display
#         screen = QGuiApplication.primaryScreen().availableGeometry()
#         self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))

#         central = QWidget()
#         self.setCentralWidget(central)

#         layout = QVBoxLayout(central)

#         self.map_widget = MapWidget()
#         layout.addWidget(self.map_widget)

#         # Connect ROS signal
#         ros.map_updated.connect(self.map_widget.update_map)

class MainWindow(QMainWindow):
    def __init__(self, ros):
        super().__init__()

        self.setWindowTitle("HERMES")

        # adjust display size to current display 
        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))

        # must set central widget when using QMainWindow
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(15)

        main_layout.addWidget(self.build_left_panel(), 1)
        main_layout.addWidget(self.build_right_panel(), 1)

    def build_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)

        # Title
        title = QLabel("HERMES")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(self.stat_box("Number of Robots", "2"))
        stats_layout.addWidget(self.stat_box("Number of Victims", "0"))
        layout.addLayout(stats_layout)

        # Legend
        legend = QLabel("🔴 Robot\n🔵 Person")
        legend.setFrameShape(QFrame.Box)
        legend.setAlignment(Qt.AlignLeft)
        layout.addWidget(legend)

        # Console
        console_label = QLabel("Console")
        layout.addWidget(console_label)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console, 1)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(QPushButton("Start"))
        button_layout.addWidget(QPushButton("End"))
        button_layout.addWidget(QPushButton("Reset"))
        layout.addLayout(button_layout)

        return panel

    def stat_box(self, title, value):
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: #b7c4cc;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(box)

        label_title = QLabel(title)
        label_title.setAlignment(Qt.AlignCenter)

        label_value = QLabel(value)
        label_value.setAlignment(Qt.AlignCenter)
        label_value.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout.addWidget(label_title)
        layout.addWidget(label_value)

        return box

    def build_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        label = QLabel("Occupancy Grid")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Placeholder – later replace with QGraphicsView or ROS image feed
        map_view = QLabel("Map Display Area")
        map_view.setAlignment(Qt.AlignCenter)
        map_view.setFrameShape(QFrame.Box)
        map_view.setMinimumSize(400, 400)

        layout.addWidget(map_view, 1)
        return panel
