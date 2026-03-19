from PyQt5.QtWidgets import (
    QPushButton, QTextEdit, QLabel, 
    QFrame, QVBoxLayout
)
from PyQt5.QtCore import Qt

def stat_box(title, value):
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

def create_button(text):
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
        QPushButton:disabled {
            background-color: #d3d3d3;
        }
    """)
    return button

def update_console(console: QTextEdit, text):
    console.append(text)
