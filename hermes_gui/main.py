import sys
import rclpy
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from ros_interface import RosInterface

def main():
    rclpy.init()

    app = QApplication(sys.argv)

    ros = RosInterface()
    window = MainWindow(ros)
    window.show()

    exit_code = app.exec_()

    ros.shutdown()
    rclpy.shutdown()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
