import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont
from draw_menu import AnemoTreasureCompassMenu
from draw_compass import AnemoTreasureCompass

def main():
    app = QApplication(sys.argv)
    
    font_id = QFontDatabase.addApplicationFont('./fonts/PyeongChangPeace-Light.ttf')
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

    app_font = QFont(font_family)
    app.setFont(app_font)
    
    setting_window = AnemoTreasureCompassMenu()
    compass_window = AnemoTreasureCompass()
    
    setting_window.show()
    compass_window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
