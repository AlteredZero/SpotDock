from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel )
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QIcon
import os

THEMES = {
    "dark": """
        * { font-family: 'Segoe UI'; color: white; outline: none; }
        #Container { background-color: rgba(28, 28, 30, 230); border-radius: 20px; border: 1px solid rgba(255,255,255,20); }
        QLabel { background: transparent; }
        #SongLabel { font-size: 14px; font-weight: 600; color: white; }
        #ArtistLabel { font-size: 12px; color: rgba(255,255,255,160); }
        QPushButton { background-color: transparent; border: none; border-radius: 10px; padding: 4px; }
        QPushButton:hover { background-color: rgba(255,255,255,25); }
        QPushButton:pressed { background-color: rgba(255,255,255,40); }
        #ShuffleBtn:checked { background-color: rgba(29, 185, 84, 40); }
    """,
    "glass": """
        * { font-family: 'Segoe UI'; color: white; outline: none; }
        #Container { background-color: rgba(18, 18, 18, 170); border-radius: 22px; border: 1px solid rgba(255,255,255,35); }
        QLabel { background: transparent; }
        #SongLabel { font-size: 14px; font-weight: bold; color: white; }
        #ArtistLabel { font-size: 11px; color: rgba(255,255,255,170); }
        QPushButton { background-color: rgba(255,255,255,10); border: none; border-radius: 12px; padding: 4px; }
        QPushButton:hover { background-color: rgba(255,255,255,25); }
        #ShuffleBtn:checked { background-color: rgba(29, 185, 84, 40); }
    """
}

class SpotDockUi(QWidget):
    def __init__(self):
        super().__init__()
        self._old_pos = None
        self.current_theme = "glass"
        self.is_playing = False
        self.loop_state = 0
        self.setup_window()
        self.build_ui()
        self.load_theme()

    def setup_window(self):
        self.setWindowTitle("SpotDock")
        self.setFixedSize(400, 95)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def build_ui(self):
        self.master_layout = QVBoxLayout(self)
        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.container = QWidget()
        self.container.setObjectName("Container")
        self.master_layout.addWidget(self.container)
        self.layout = QHBoxLayout(self.container)
        self.layout.setContentsMargins(14, 14, 14, 14)
        self.layout.setSpacing(12)
        self.layout.setAlignment(Qt.AlignLeft)

        self.album_art = QLabel()
        self.album_art.setFixedSize(64, 64)
        pixmap = QPixmap("./assets/default_cover.png")
        if pixmap.isNull():
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.gray)

        scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x_offset = (64 - scaled_pixmap.width()) // 2
        y_offset = (64 - scaled_pixmap.height()) // 2
        rounded_pixmap = QPixmap(64, 64)
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, 64, 64, 10, 10)
        painter.setClipPath(path)
        painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
        painter.end()
        self.album_art.setPixmap(rounded_pixmap)

        self.info_layout = QVBoxLayout()
        self.info_layout.setSpacing(0)
        self.info_layout.setContentsMargins(0, 0, 0, 0)
        self.song_label = QLabel("No song playing")
        self.song_label.setObjectName("SongLabel")
        self.artist_label = QLabel("Spotify")
        self.artist_label.setObjectName("ArtistLabel")
        self.info_layout.addWidget(self.song_label)
        self.info_layout.addWidget(self.artist_label)

        self.info_layout.addSpacing(6)

        self.controls_layout = QHBoxLayout()
        self.controls_layout.setSpacing(6)
        self.controls_layout.setAlignment(Qt.AlignLeft)

        self.shuffle_button = QPushButton()
        self.shuffle_button.setObjectName("ShuffleBtn")
        self.prev_button = QPushButton()
        self.play_button = QPushButton()
        self.next_button = QPushButton()
        self.loop_button = QPushButton()
        self.loop_button.setObjectName("LoopBtn")

        self.shuffle_button.setIcon(QIcon("./assets/shuffle.png"))
        self.prev_button.setIcon(QIcon("./assets/prev.png"))
        self.play_button.setIcon(QIcon("./assets/paused.png"))
        self.next_button.setIcon(QIcon("./assets/next.png"))
        self.loop_button.setIcon(QIcon("./assets/loop.png"))

        self.shuffle_button.setCheckable(True)
        self.play_button.clicked.connect(self.pause_unpause)
        self.loop_button.clicked.connect(self.cycle_loop)

        icon_size = QSize(20, 20)
        for btn in [self.shuffle_button, self.prev_button, self.play_button, self.next_button, self.loop_button]:
            btn.setFixedSize(32, 32)
            btn.setIconSize(icon_size)
            self.controls_layout.addWidget(btn)

        self.info_layout.addLayout(self.controls_layout)
        self.layout.addWidget(self.album_art)
        self.layout.addLayout(self.info_layout)
        self.layout.addStretch()

        self.expand_button = QPushButton()
        self.expand_button.setIcon(QIcon("./assets/expand.png"))
        self.expand_button.setFixedSize(34, 34)
        self.expand_button.setIconSize(QSize(18, 18))
        self.expand_button.move(360, 5)
        self.expand_button.setParent(self.container)
        self.expand_button.raise_()

    def cycle_loop(self):
        self.loop_state = (self.loop_state + 1) % 3
        if self.loop_state == 0:
            self.loop_button.setStyleSheet("")
            self.loop_button.setIcon(QIcon("./assets/loop.png"))
        elif self.loop_state == 1:
            self.loop_button.setStyleSheet("background-color: rgba(29, 185, 84, 40);")
            self.loop_button.setIcon(QIcon("./assets/loop.png"))
        elif self.loop_state == 2:
            self.loop_button.setStyleSheet("background-color: rgba(29, 185, 84, 40);")
            self.loop_button.setIcon(QIcon("./assets/LoopSong.png"))

    def pause_unpause(self):
        self.is_playing = not self.is_playing
        icon_path = "./assets/paused.png" if not self.is_playing else "./assets/playing.png"
        self.play_button.setIcon(QIcon(icon_path))

    def load_theme(self):
        if self.current_theme in THEMES:
            self.setStyleSheet(THEMES[self.current_theme])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self._old_pos:
            delta = event.globalPos() - self._old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self._old_pos = None
