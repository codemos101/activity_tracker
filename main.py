import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from pynput import keyboard, mouse


class TrackerWindow(QWidget):
    def __init__(self):
        super().__init__()

        # counters
        self.key_count = 0
        self.click_count = 0
        self.running = False

        # UI
        self.setWindowTitle("Activity Tracker v1")
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel("Status: OFF")
        self.keys_label = QLabel("Keys pressed: 0")
        self.clicks_label = QLabel("Mouse clicks: 0")

        self.start_button = QPushButton("Start Tracker")
        self.stop_button = QPushButton("Stop Tracker")

        self.start_button.clicked.connect(self.start_tracker)
        self.stop_button.clicked.connect(self.stop_tracker)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.keys_label)
        layout.addWidget(self.clicks_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        # listeners (but not started yet)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)

    # KEY EVENT
    def on_key_press(self, key):
        if self.running:
            self.key_count += 1
            self.keys_label.setText(f"Keys pressed: {self.key_count}")

    # MOUSE EVENT
    def on_click(self, x, y, button, pressed):
        if self.running and pressed:
            self.click_count += 1
            self.clicks_label.setText(f"Mouse clicks: {self.click_count}")

    # START
    def start_tracker(self):
        self.running = True
        self.label.setText("Status: ON")

        if not self.keyboard_listener.is_alive():
            self.keyboard_listener.start()

        if not self.mouse_listener.is_alive():
            self.mouse_listener.start()

    # STOP
    def stop_tracker(self):
        self.running = False
        self.label.setText("Status: OFF")


app = QApplication(sys.argv)
window = TrackerWindow()
window.show()
sys.exit(app.exec())