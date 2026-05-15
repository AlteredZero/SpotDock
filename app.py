from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QSizePolicy,
    QGraphicsOpacityEffect
)

from PyQt5.QtCore import (
    Qt,
    QSize,
    QPropertyAnimation,
    QEasingCurve,
    pyqtProperty
)

from PyQt5.QtGui import (
    QPixmap,
    QPainter,
    QPainterPath,
    QIcon,
    QColor
)

PANEL_COLLAPSED_H = 0
PANEL_EXPANDED_H = 510

BAR_H = 95
BAR_W = 400

WINDOW_H = PANEL_EXPANDED_H + BAR_H + 8

ANIM_DURATION = 320

THEMES = {
    "glass": """
        * {
            font-family: 'Segoe UI';
            color: white;
            outline: none;
        }

        #Container, #PanelContainer {
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
        }

        #ArtistLabel {
            font-size: 11px;
            color: rgba(255,255,255,170);
        }

        #AppName {
            font-size: 15px;
            font-weight: 700;
        }

        QPushButton {
            background-color: rgba(255,255,255,10);
            border: none;
            border-radius: 12px;
            padding: 4px;
        }

        QPushButton:hover {
            background-color: rgba(255,255,255,25);
        }

        #TabBar QPushButton {
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            padding: 6px 14px;
            color: rgba(255,255,255,150);
            background-color: rgba(255,255,255,6);
        }

        #TabBar QPushButton:checked {
            background-color: rgba(255,255,255,20);
            color: white;
        }

        #Divider {
            background-color: rgba(255,255,255,22);
        }

        #TabPage {
            background-color: rgba(255,255,255,7);
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,14);
        }
    """
}


class SpotDockUi(QWidget):
    def __init__(self):
        super().__init__()

        self._old_pos = None
        self.panel_open = False
        self.current_theme = "glass"

        self.setup_window()
        self.build_ui()
        self.load_theme()

    def setup_window(self):
        self.setWindowTitle("SpotDock")

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(BAR_W, WINDOW_H)

    def build_ui(self):
        self.setLayout(QVBoxLayout())

        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.panel_wrapper = QWidget(self)

        self.panel_wrapper.setFixedSize(
            BAR_W,
            PANEL_COLLAPSED_H
        )

        self.panel_wrapper.move(
            0,
            WINDOW_H - BAR_H
        )

        panel_layout = QVBoxLayout(self.panel_wrapper)

        panel_layout.setContentsMargins(0, 0, 0, 8)

        self.panel_container = QWidget()

        self.panel_container.setObjectName("PanelContainer")

        panel_layout.addWidget(self.panel_container)

        self._build_panel(self.panel_container)

        self.bar_widget = QWidget(self)

        self.bar_widget.setFixedSize(
            BAR_W,
            BAR_H
        )

        self.bar_widget.move(
            0,
            WINDOW_H - BAR_H
        )

        bar_layout_outer = QVBoxLayout(self.bar_widget)

        bar_layout_outer.setContentsMargins(0, 0, 0, 0)

        self.container = QWidget()

        self.container.setObjectName("Container")

        bar_layout_outer.addWidget(self.container)

        self._build_bar(self.container)

        self.panel_anim = QPropertyAnimation(
            self,
            b"panelHeight"
        )

        self.panel_anim.setDuration(ANIM_DURATION)

        self.panel_anim.setEasingCurve(
            QEasingCurve.OutCubic
        )

        self.panel_opacity = QGraphicsOpacityEffect()

        self.panel_wrapper.setGraphicsEffect(
            self.panel_opacity
        )

        self.panel_opacity.setOpacity(0)

        self.opacity_anim = QPropertyAnimation(
            self.panel_opacity,
            b"opacity"
        )

        self.opacity_anim.setDuration(ANIM_DURATION)

        self.opacity_anim.setEasingCurve(
            QEasingCurve.OutCubic
        )

    def _get_panel_height(self):
        return self.panel_wrapper.height()

    def _set_panel_height(self, h):
        self.panel_wrapper.setFixedHeight(h)

        spacing = 8 if h > 0 else 0

        dock_y = WINDOW_H - BAR_H

        self.bar_widget.move(
            0,
            dock_y
        )

        self.panel_wrapper.move(
            0,
            dock_y - h - spacing
        )

    panelHeight = pyqtProperty(
        int,
        _get_panel_height,
        _set_panel_height
    )

    def _build_panel(self, parent):
        layout = QVBoxLayout(parent)

        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        header = QHBoxLayout()

        header.setSpacing(8)

        icon_label = QLabel()

        icon_pix = QPixmap("./assets/SpotDockIcon.png")

        if icon_pix.isNull():
            icon_pix = QPixmap(28, 28)
            icon_pix.fill(QColor(29, 185, 84))

        icon_label.setPixmap(
            icon_pix.scaled(
                28,
                28,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        icon_label.setFixedSize(28, 28)

        app_name = QLabel("SpotDock")

        app_name.setObjectName("AppName")

        header.addWidget(icon_label)
        header.addWidget(app_name)
        header.addStretch()

        layout.addLayout(header)

        divider = QWidget()

        divider.setObjectName("Divider")

        divider.setFixedHeight(1)

        layout.addWidget(divider)

        tab_bar_widget = QWidget()

        tab_bar_widget.setObjectName("TabBar")

        tab_bar_layout = QHBoxLayout(tab_bar_widget)

        tab_bar_layout.setContentsMargins(0, 0, 0, 0)

        tab_bar_layout.setSpacing(4)

        self.tab_buttons = []

        tab_names = [
            "Library",
            "Playlist",
            "Queue",
            "Settings"
        ]

        for i, name in enumerate(tab_names):
            btn = QPushButton(name)

            btn.setCheckable(True)

            btn.clicked.connect(
                lambda checked, idx=i:
                self._switch_tab(idx)
            )

            tab_bar_layout.addWidget(btn)

            self.tab_buttons.append(btn)

        tab_bar_layout.addStretch()

        layout.addWidget(tab_bar_widget)

        self.tab_stack = QStackedWidget()

        self.tab_stack.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        for _ in range(4):
            self.tab_stack.addWidget(
                self._create_empty_tab()
            )

        layout.addWidget(self.tab_stack)

        self._switch_tab(0)

    def _create_empty_tab(self):
        page = QWidget()

        page.setObjectName("TabPage")

        layout = QVBoxLayout(page)

        layout.setContentsMargins(18, 18, 18, 18)

        return page

    def _switch_tab(self, idx):
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == idx)

        self.tab_stack.setCurrentIndex(idx)

    def _build_bar(self, parent):
        layout = QHBoxLayout(parent)

        layout.setContentsMargins(14, 14, 14, 14)

        layout.setSpacing(12)

        self.album_art = QLabel()

        self.album_art.setFixedSize(64, 64)

        pixmap = QPixmap("./assets/default_cover.png")

        if pixmap.isNull():
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.gray)

        scaled = pixmap.scaled(
            64,
            64,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        rounded = QPixmap(64, 64)

        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        path = QPainterPath()

        path.addRoundedRect(
            0,
            0,
            64,
            64,
            10,
            10
        )

        painter.setClipPath(path)

        painter.drawPixmap(
            0,
            0,
            scaled
        )

        painter.end()

        self.album_art.setPixmap(rounded)

        layout.addWidget(self.album_art)

        info_layout = QVBoxLayout()

        info_layout.setSpacing(0)

        song_label = QLabel("No song playing")

        song_label.setObjectName("SongLabel")

        artist_label = QLabel("Spotify")

        artist_label.setObjectName("ArtistLabel")

        info_layout.addWidget(song_label)
        info_layout.addWidget(artist_label)

        info_layout.addSpacing(6)

        controls = QHBoxLayout()

        controls.setSpacing(6)

        button_icons = [
            "./assets/shuffle.png",
            "./assets/prev.png",
            "./assets/paused.png",
            "./assets/next.png",
            "./assets/loop.png"
        ]

        for icon_path in button_icons:
            btn = QPushButton()

            btn.setFixedSize(32, 32)

            btn.setIcon(QIcon(icon_path))

            btn.setIconSize(QSize(20, 20))

            controls.addWidget(btn)

        info_layout.addLayout(controls)

        layout.addLayout(info_layout)

        layout.addStretch()

        self.expand_button = QPushButton()

        self.expand_button.setParent(self.container)

        self.expand_button.setFixedSize(34, 34)

        self.expand_button.setIconSize(QSize(18, 18))

        self.expand_button.setIcon(
            QIcon("./assets/expand.png")
        )

        self.expand_button.move(360, 5)

        self.expand_button.raise_()

        self.expand_button.clicked.connect(
            self.toggle_expand
        )

    def toggle_expand(self):
        self.panel_open = not self.panel_open

        if self.panel_open:
            self.panel_anim.setStartValue(
                PANEL_COLLAPSED_H
            )

            self.panel_anim.setEndValue(
                PANEL_EXPANDED_H
            )

            self.opacity_anim.setStartValue(0)

            self.opacity_anim.setEndValue(1)

            self.expand_button.setIcon(
                QIcon("./assets/deexpand.png")
            )

        else:
            self.panel_anim.setStartValue(
                PANEL_EXPANDED_H
            )

            self.panel_anim.setEndValue(
                PANEL_COLLAPSED_H
            )

            self.opacity_anim.setStartValue(1)

            self.opacity_anim.setEndValue(0)

            self.expand_button.setIcon(
                QIcon("./assets/expand.png")
            )

        self.panel_anim.start()

        self.opacity_anim.start()

    def load_theme(self):
        self.setStyleSheet(
            THEMES[self.current_theme]
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self._old_pos:
            delta = (
                event.globalPos() -
                self._old_pos
            )

            self.move(
                self.x() + delta.x(),
                self.y() + delta.y()
            )

            self._old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self._old_pos = None