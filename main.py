import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from pynput import keyboard, mouse


class TrackerWindow(QWidget):
    def __init__(self):
        super().__init__()

        # ---------------- WINDOW FLAGS ----------------
        self.setWindowTitle("Activity Tracker v1.5 (Floating)")
        self.setGeometry(100, 100, 350, 250)

        # ALWAYS ON TOP
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        # Optional nice touch
        self.setWindowOpacity(0.95)

        # ---------------- DATA ----------------
        self.key_count = 0
        self.click_count = 0

        self.running = False

        self.start_time = None
        self.last_activity_time = None

        self.idle_threshold = 5  # seconds (testing)

        # ---------------- UI ----------------
        self.status_label = QLabel("Status: OFF")
        self.time_label = QLabel("Session Time: 00:00:00")
        self.idle_label = QLabel("State: IDLE")

        self.keys_label = QLabel("Keys: 0")
        self.clicks_label = QLabel("Clicks: 0")

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        # prevent button stealing keyboard focus
        self.start_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.stop_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.start_button.clicked.connect(self.start_tracker)
        self.stop_button.clicked.connect(self.stop_tracker)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.idle_label)
        layout.addWidget(self.keys_label)
        layout.addWidget(self.clicks_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        # ---------------- LISTENERS ----------------
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)

        # ---------------- TIMER LOOP ----------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

    # ---------------- ACTIVITY ----------------
    def on_activity(self):
        self.last_activity_time = time.time()

    # ---------------- KEYBOARD ----------------
    def on_key_press(self, key):
        if not self.running:
            return

        try:
            char = key.char
        except:
            return

        if char is None:
            return

        # ignore space
        if char == " ":
            return

        self.key_count += 1
        self.keys_label.setText(f"Keys: {self.key_count}")
        self.on_activity()

    # ---------------- MOUSE ----------------
    def on_click(self, x, y, button, pressed):
        if self.running and pressed:
            self.click_count += 1
            self.clicks_label.setText(f"Clicks: {self.click_count}")
            self.on_activity()

    # ---------------- CONTROL ----------------
    def start_tracker(self):
        self.running = True
        self.start_time = time.time()
        self.last_activity_time = time.time()

        self.status_label.setText("Status: ON")

        if not self.keyboard_listener.is_alive():
            self.keyboard_listener.start()

        if not self.mouse_listener.is_alive():
            self.mouse_listener.start()

    def stop_tracker(self):
        self.running = False
        self.status_label.setText("Status: OFF")

    # ---------------- UI UPDATE LOOP ----------------
    def update_ui(self):
        if not self.running:
            return

        # session time
        elapsed = int(time.time() - self.start_time)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60

        self.time_label.setText(f"Session Time: {h:02}:{m:02}:{s:02}")

        # idle detection
        if time.time() - self.last_activity_time > self.idle_threshold:
            self.idle_label.setText("State: IDLE")
        else:
            self.idle_label.setText("State: ACTIVE")


# ---------------- RUN APP ----------------
app = QApplication(sys.argv)
window = TrackerWindow()
window.show()
sys.exit(app.exec())