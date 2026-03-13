from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import time

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
            # -----------------------------
            # 1. Test SSH connection
            # -----------------------------
            self.status.emit("Connecting to HERMES robot...")
            ssh_test = subprocess.run(
                ["ssh", f"{PI_USER}@{IP_ADDR}", "echo connected"],
                capture_output=True,
                text=True
            )

            if ssh_test.returncode != 0:
                self.error.emit(
                    ssh_test.stderr.strip() or
                    "Unable to establish SSH connection."
                )
                return

            self.status.emit("SSH connection successful.")

            # 2. Launch ROS2 nodes
            self.status.emit("Launching ROS2 nodes...")

            ssh_command = [
                "ssh",
                f"{PI_USER}@{IP_ADDR}",
                f"ros2 launch {PACKAGE_NAME} {LAUNCH_FILE}'"
            ]

            self.process = subprocess.Popen(
                ssh_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # -----------------------------
            # 3. Detect early SSH failure
            # -----------------------------
            time.sleep(3)

            if self.process.poll() is not None:
                stderr_output = self.process.stderr.read()
                self.error.emit(stderr_output or "Launch failed.")
                return

            # -----------------------------
            # 4. Wait for ROS topic (robot ready)
            # -----------------------------
            self.status.emit("Waiting for robot topics...")

            topic_ready = False

            for _ in range(3):   
                result = subprocess.run(
                    ["ros2", "topic", "list"],
                    capture_output=True,
                    text=True
                )

                if "/scan" in result.stdout:
                    topic_ready = True
                    break

                time.sleep(1)

            if not topic_ready:
                self.error.emit("Launch started but required ROS topic not detected.")
                return

            self.status.emit("Robot system ready.")

            # -----------------------------
            # 5. Stream ROS logs
            # -----------------------------
            for line in self.process.stdout:
                self.status.emit(line.strip())

            # -----------------------------
            # 6. Signal success
            # -----------------------------
            self.finished_launch.emit()

        except Exception as e:
            self.error.emit(f"Launch failed: {str(e)}")