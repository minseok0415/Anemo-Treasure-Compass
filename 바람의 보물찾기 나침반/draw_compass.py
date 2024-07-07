from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QPixmap
from get_degree import get_deg
from collection import get_selected_collection

# icon_path_array = ["icons/calla_lily_icon.png", "icons/cecilia_icon.png", "icons/dandelion_seed_icon.png", "icons/philanemo_mushroom_icon.png",
#                     "icons/small_lamp_grass_icon.png", "icons/valberry_icon.png", "icons/windwheel_aster_icon.png", "icons/wolfhook_icon.png"]
icon_path_array = ["icons/calla_lily.png", "icons/cecilia.png", "icons/dandelion_seed.png", "icons/philanemo_mushroom.png",
                    "icons/small_lamp_grass.png", "icons/valberry.png", "icons/windwheel_aster.png", "icons/wolfhook.png"]
collection_names = ["통통 연꽃", "세실리아꽃", "민들레 씨앗", "바람버섯",
               "등불꽃", "낙락베리", "풍차 국화", "고리고리 열매"]

class AnemoTreasureCompass(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 부모 클래스의 __init__ 메서드 호출
        self.setWindowTitle('바람의 보물찾기 나침반')
        self.setGeometry(0, 0, 1535, 865)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.accuracy_label = QLabel(self)
        self.accuracy_label.setGeometry(240, 60, 280, 36)
        self.accuracy_label.setAlignment(Qt.AlignVCenter)
        
        self.setWindowFlag(Qt.Tool)

        # QTimer 객체 생성
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(100)

    def close_application(self):
        QApplication.quit()
    
    def draw_compass(self, painter, position, distance, startAngle, sc):        
        # Draw arc (segment) of the circle within the specified angle range
        if startAngle is not None:
            for i in range(10):
                pen = QPen(QColor(80, 213, 255, 25 + i * 10))
                pen.setWidth(2)
                pen.setJoinStyle(Qt.RoundJoin)  # Set round join style for rounded corners
                painter.setPen(pen)
                painter.drawArc(59 - i, 24 - i, 151 + 2 * i, 151 + 2 * i,
                                (startAngle - 30 / 2) * 16, 30 * 10)
            painter.setPen(QColor(0, 0, 0))

        if distance is not None and position is not None and distance < 80:
            x = 135 - position[1]
            y = 98 - position[0]

            image = QPixmap(icon_path_array[collection_names.index(sc)])
            scaled_pixmap = image.scaled(15, 15, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(x - 5, y - 5, scaled_pixmap)

    def paintEvent(self, event):
        sc = get_selected_collection()
        if sc == None:
            self.accuracy_label.setText("")
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Enable antialiasing for smoother edges

        # Draw arc (segment) of the circle within the specified angle range
        my_position, collection_position, relative_position, distance, startAngle, accuracy = get_deg()
        
        if distance > 80:
            # self.accuracy_label.setText(str(int(distance)))
            self.accuracy_label.setText(f'{" " * 4}{self.to_location_name(collection_position)} 이동해주세요')
            self.accuracy_label.setStyleSheet("""
                                                background: rgba(0, 0, 0, 100);
                                                color: rgba(255, 255, 255, 200);
                                                font-size: 16px;
                                                border-radius: 12px;
                                            """)
        else:
            self.accuracy_label.setText("")
            self.accuracy_label.setStyleSheet("background: none;")
        
        if accuracy < 0.7 or accuracy == 1.0:
            self.accuracy_label.setText("")
            self.accuracy_label.setStyleSheet("background: none;")
            return
        
        self.draw_compass(painter, relative_position, distance, startAngle, sc)
        
    def to_location_name(self, pos):
        y, x = pos
        if x <= 450 and y <= 450:
            return "바람 드래곤의 폐허로"
        elif x <= 670 and y <= 450:
            return "크라운 협곡으로"
        elif x <= 935 and y <= 380:
            return "시드르 호수로"
        elif x <= 1200 and y <= 250:
            return "바람맞이 산으로"
        elif y <= 230:
            return "바람맞이 봉우리로"
        elif x <= 670 and y <= 670:
            return "울프 영지로"
        elif x <= 935 and y <= 590:
            return "몬드성으로"
        elif x <= 1070 and y <= 590:
            return "속삭임의 숲으로"
        elif x <= 1200 and y <= 400:
            return "별이 떨어지는 호수로"
        elif y <= 375:
            return "별을 따는 절벽으로"
        elif y <= 590:
            return "천풍 신전으로"
        elif x <= 750:
            return "다운 와이너리로"
        elif x <= 970:
            return "샘물 마을로"
        elif x <= 1180 and y <= 840:
            return "바람이 시작되는 곳으로"
        elif y <= 840:
            return "매의 해안으로"
        elif x <= 1400:
            return "타타우파 협곡으로"
        else:
            return "맹세의 갑각으로"
            