from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

import os


THEMES = {
    "dark": """
        * {
            font-family: 'Segoe UI';
            color: white;
            outline: none;
        }

        #Container {
            background-color: rgba(28, 28, 30, 230);
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,20);
        }

        QLabel {
            background: transparent;
        }

        #SongLabel {
            font-size: 14px;
            font-weight: 600;
            color: white;
        }

        #ArtistLabel {
            font-size: 12px;
            color: rgba(255,255,255,160);
        }

        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: rgba(255,255,255,25);
        }

        QPushButton:pressed {
            background-color: rgba(255,255,255,40);
        }
    """,

    "glass": """
        * {
            font-family: 'Segoe UI';
            color: white;
            outline: none;
        }

        #Container {
            background-color: rgba(18, 18, 18, 170);
            border-radius: 22px;
            border: 1px solid rgba(255,255,255,35);
        }

        QLabel {
            background: transparent;
        }

        #SongLabel {
            font-size: 14px;
            font-weight: bold;
            color: white;
        }

        #ArtistLabel {
            font-size: 11px;
            color: rgba(255,255,255,170);
        }

        QPushButton {
            background-color: rgba(255,255,255,10);
            border: none;
            border-radius: 12px;
            font-size: 16px;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: rgba(255,255,255,25);
        }
    """
}


class SpotDockUi(QWidget):
    def __init__(self):
        super().__init__()

        self._old_pos = None
        self.current_theme = "glass"

        self.setup_window()
        self.build_ui()
        self.load_theme()

    def setup_window(self):
        self.setWindowTitle("SpotDock")

        self.setFixedSize(400, 92)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

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

        self.album_art = QLabel()
        self.album_art.setFixedSize(64, 64)

        pixmap = QPixmap("./assets/default_cover.png")
        self.album_art.setPixmap(
            pixmap.scaled(
                64,
                64,
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
        )

        self.info_layout = QVBoxLayout()
        self.info_layout.setSpacing(2)

        self.song_label = QLabel("No song playing")
        self.song_label.setObjectName("SongLabel")

        self.artist_label = QLabel("Spotify")
        self.artist_label.setObjectName("ArtistLabel")

        self.info_layout.addWidget(self.song_label)
        self.info_layout.addWidget(self.artist_label)

        self.controls_layout = QHBoxLayout()
        self.controls_layout.setSpacing(4)

        self.prev_button = QPushButton("◀")
        self.play_button = QPushButton("▶")
        self.next_button = QPushButton("▶")

        self.prev_button.setFixedSize(34, 34)
        self.play_button.setFixedSize(34, 34)
        self.next_button.setFixedSize(34, 34)

        self.controls_layout.addWidget(self.prev_button)
        self.controls_layout.addWidget(self.play_button)
        self.controls_layout.addWidget(self.next_button)

        self.info_layout.addSpacing(4)
        self.info_layout.addLayout(self.controls_layout)

        self.layout.addWidget(self.album_art)
        self.layout.addLayout(self.info_layout)

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