from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, QRect, QFile
from PySide6.QtGui import QPainter, QColor, QPixmap, QCursor, QIcon, QAction
from PySide6.QtSvgWidgets import QSvgWidget
from draw_collections import Collections
from collection import change_find_collection

image_path_array = ["icons/calla_lily.png", "icons/cecilia.png", "icons/dandelion_seed.png", "icons/philanemo_mushroom.png",
                    "icons/small_lamp_grass.png", "icons/valberry.png", "icons/windwheel_aster.png", "icons/wolfhook.png"]

class AnemoTreasureCompassMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('바람의 보물찾기 나침반')
        self.setGeometry(0, 0, 1535, 865)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.show_selection_window = False
        self.collections = []
        self._selected_collection = None

        self.button = QWidget(self)
        self.button.setGeometry(0, 0, self.width(), self.height())
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.mousePressEvent = self.toggle_large_square

        self.selection_window_label = QLabel(self)
        self.selection_window_label.setGeometry((self.width() - 300) // 2, (self.height() - 280) // 2, 300, 35)
        self.selection_window_label.setAlignment(Qt.AlignCenter)

        self.transparent_overlay = QWidget(self)
        self.transparent_overlay.setGeometry(self.geometry())
        self.transparent_overlay.setStyleSheet("background-color: rgba(0, 191, 165, 0.02);")
        self.transparent_overlay.hide()

        x = self.width() - 516
        y = 15

        self.svg_widget = QSvgWidget(self.button)
        self.svg_widget.setGeometry(x, y, 42, 46)

        svg_file_path = "svg/compass.svg"
        file = QFile(svg_file_path)

        if file.exists():
            self.svg_widget.load(svg_file_path)
        else:
            print(f"File {svg_file_path} not found.")

        self.setWindowFlag(Qt.Tool)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("svg/white_compass.svg"))
        self.tray_icon.setToolTip("바람의 보물찾기 나침반")

        self.tray_menu = QMenu()
        exit_action = QAction("종료", self)
        exit_action.triggered.connect(self.close_application)
        self.tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        self.initialize_collections()

    def close_application(self):
        QApplication.quit()

    def toggle_large_square(self, event):
        self.show_selection_window = not self.show_selection_window
        self.selection_window_label.setText("")
        self.selection_window_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        
        if self.show_selection_window:
            self.transparent_overlay.show()
        else:
            self.transparent_overlay.hide()
        
        self.update()

    def mousePressEvent(self, event):
        if self.transparent_overlay.isVisible() and self.transparent_overlay.geometry().contains(event.position().toPoint()):
            self.toggle_large_square(event)
            event.accept()

    def initialize_collections(self):
        self.collections = []
        x = (self.width() - 350) // 2
        y = (self.height() - 200) // 2
        columns = 4
        rows = 2
        gap = 10
        w = (350 - gap * (columns + 1)) // columns
        h = (200 - gap * (rows + 1)) // rows

        for index in range(len(image_path_array)):
            col = index % columns
            row = index // columns
            left = x + gap * (col + 1) + w * col
            top = y + gap * (row + 1) + h * row

            collection = Collections(self, index)
            collection.setGeometry(left, top, w, h)
            collection.setCursor(QCursor(Qt.PointingHandCursor))
            self.collections.append(collection)

    def draw_selection_window(self, painter):
        self.selection_window_label.setText(f"바람의 {self.selected_collection if self.selected_collection else '보물찾기'} 나침반")
        self.selection_window_label.setStyleSheet("""
                                                    background-color: rgb(246, 246, 246);
                                                    border-radius: 10px;
                                                    font-size: 22px;
                                                  """)

        x = (self.width() - 350) // 2
        y = (self.height() - 200) // 2
        painter.setBrush(QColor(0, 191, 165))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRect(x, y, 350, 200), 10, 10)

        for i, collection in enumerate(self.collections):
            col = i % 4
            row = i // 4
            left = x + 10 * (col + 1) + collection.width() * col
            top = y + 10 * (row + 1) + collection.height() * row

            painter.setBrush(QColor(255, 255, 255))
            painter.drawRoundedRect(QRect(left, top, collection.width(), collection.height()), 10, 10)

            image = QPixmap(image_path_array[i])
            scaled_pixmap = image.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(left, top + 5, scaled_pixmap)

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.show_selection_window:
            self.draw_selection_window(painter)

    def selected_collection_changed(self):
        change_find_collection(self.selected_collection)

    @property
    def selected_collection(self):
        return self._selected_collection

    @selected_collection.setter
    def selected_collection(self, value):
        self._selected_collection = value
        self.selected_collection_changed()
