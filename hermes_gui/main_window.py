from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QFrame
)
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt
import sys
from map_widget import MapWidget

class MainWindow(QMainWindow):
    def __init__(self, ros):
        super().__init__()

        self.setWindowTitle(" ")

        # adjust display size to current display 
        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * 0.9), int(screen.height() * 0.9))

        # must set central widget when using QMainWindow
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(15)

        main_layout.addWidget(self.build_left_panel(), 1)
        main_layout.addWidget(self.build_right_panel(ros), 2)

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
        stats_layout.addWidget(self.stat_box("Number of Robots", "0"))
        stats_layout.addWidget(self.stat_box("Number of Victims", "0"))
        layout.addLayout(stats_layout)

        # Camera View
        camera_layout = QVBoxLayout()
        camera_layout.setSpacing(2)
        camera_label = QLabel("Camera Image")
        camera_label.setAlignment(Qt.AlignCenter)
        camera_view = QLabel("Camera Display Area")
        camera_view.setAlignment(Qt.AlignCenter)
        camera_view.setFrameShape(QFrame.Box)
        camera_layout.addWidget(camera_label)
        camera_layout.addWidget(camera_view, 1)
        layout.addLayout(camera_layout)

        # Console 
        console_layout = QVBoxLayout()
        console_layout.setSpacing(2)
        console_label = QLabel("Console")
        console_label.setAlignment(Qt.AlignCenter)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        console_layout.addWidget(console_label)
        console_layout.addWidget(self.console, 1)
        layout.addLayout(console_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button("Start"))
        button_layout.addWidget(self.create_button("End"))
        button_layout.addWidget(self.create_button("Reset"))
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

    def build_right_panel(self, ros):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(2)

        label = QLabel("Environment Mapping")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # create map widget and connect ROS signal
        map_widget = MapWidget()
        map_widget.setFrameShape(QFrame.Box)
        layout.addWidget(map_widget, 2)
        ros.map_updated.connect(map_widget.update_map)

        return panel

    def create_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #b7c4cc;
                border: none;
                padding: 10px;
                text-align: center;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #a4b0b7;
            }
        """)
        return button