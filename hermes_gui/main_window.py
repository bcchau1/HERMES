from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QFrame
)
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt
from map_widget import MapWidget
from utils.window_utils import create_button, update_console, stat_box
from utils.ros_launcher import LaunchThread

class MainWindow(QMainWindow):
    def __init__(self, ros):
        super().__init__()

        self.setWindowTitle(" ")

        '''
        LAUNCH: SSH's into the HERMES robot, then runs the bringup launch file to start the camera, LiDAR, and SLAM
        START: Begins robot operation and movement. 
        END: Stops the robot operation.
        RESET: Resets map and returns robot to initial state.
        '''
        self.launch_button = None
        self.start_button = None
        self.end_button = None
        self.reset_button = None

        # adjust display size to current display 
        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * 0.9), int(screen.height() * 0.9))

        # must set central widget when using QMainWindow
        central = QWidget()
        self.setCentralWidget(central)

        self.map_widget = MapWidget()
        self.launch_thread = LaunchThread()

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
        stats_layout.addWidget(stat_box("Robot Status", "Off"))
        stats_layout.addWidget(stat_box("Number of Victims", "0"))
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

        self.launch_button = create_button("Launch") 
        button_layout.addWidget(self.launch_button)

        self.start_button = create_button("Start")
        self.start_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
       
        self.launch_button.clicked.connect(self.launch_start)
        self.launch_thread.status.connect(lambda msg: update_console(self.console, msg))
        self.launch_thread.finished_launch.connect(self.launch_finished)
        self.launch_thread.error.connect(self.launch_failed)

        self.end_button = create_button("End")
        self.end_button.setEnabled(False)
        button_layout.addWidget(self.end_button)
      
        self.reset_button = create_button("Reset")
        self.reset_button.setEnabled(False)
        button_layout.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.reset_clicked)
        
        layout.addLayout(button_layout)

        return panel

    def build_right_panel(self, ros):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(2)

        label = QLabel("Environment Mapping")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # create map widget and connect ROS signal
        self.map_widget.setFrameShape(QFrame.Box)
        layout.addWidget(self.map_widget, 2)
        ros.map_updated.connect(self.map_widget.update_map)
        ros.pose_updated.connect(self.map_widget.update_pose)

        return panel

    def launch_start(self):
        update_console(self.console, "Beginning launch...")
        self.launch_button.setEnabled(False)
        self.launch_thread.start()
    
    def reset_clicked(self):
        self.console.clear()
        update_console(self.console, "Resetting...")
        self.map_widget.reset_map()
        self.launch_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self.end_button.setEnabled(False)
        self.reset_button.setEnabled(False)

    def launch_finished(self):
        update_console(self.console, "Launch finished.")
        self.launch_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.end_button.setEnabled(True) 
        self.reset_button.setEnabled(True) 

    def launch_failed(self, msg):
        update_console(self.console, f"ERROR: {msg}")
        self.launch_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self.end_button.setEnabled(False)
        self.reset_button.setEnabled(False)