from PyQt5.QtCore import QThread, pyqtSignal
import subprocess

PI_USER = "nkle2"
IP_ADDR = ""
PACKAGE_NAME = "hermes_bringup"
LAUNCH_FILE = "hermes_bringup.launch.py"

class LaunchThread(QThread):
    finished_launch = pyqtSignal()
    status = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        try: 
            self.status.emit("Connecting to HERMES robot...")

            ssh_command = [ 
                "ssh",
                f"{PI_USER}@{IP_ADDR}",
                f"ros2 launch {PACKAGE_NAME} {LAUNCH_FILE}"
            ]

            self.status.emit("Launching ROS2 nodes...")
            self.process = subprocess.Popen(
                ssh_command,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text = True
            )
            
            # read output
            for line in self.process.stdout:
                self.status.emit(line.strip())

            stderr_output = self.process.stderr.read()
            if stderr_output:
                self.error.emit(stderr_output)

            self.finished_launch.emit()

        except Exception as e:
            self.error.emit(f"Launch failed: {str(e)}")