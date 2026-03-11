from PyQt5.QtCore import QThread, pyqtSignal
import subprocess

class LaunchThread(QThread):
    finished_launch = pyqtSignal()

    def run(self):
        process = subprocess.Popen(
            ["ros2", "launch", "hermes_bringup", "hermes_bringup.launch.py"]
        )

        self.sleep(3)
        self.finished_launch.emit()
