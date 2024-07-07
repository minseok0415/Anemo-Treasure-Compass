from PySide6.QtWidgets import QWidget

collection_names = ["통통 연꽃", "세실리아꽃", "민들레 씨앗", "바람버섯",
               "등불꽃", "낙락베리", "풍차 국화", "고리고리 열매"]

class Collections(QWidget):
    def __init__(self, parent, index):
        super().__init__(parent)
        self.parent = parent
        self.index = index

    def mousePressEvent(self, event):
        # Handle mouse click event for the small square
        if self.parent.selected_collection != collection_names[self.index]:
            self.parent.selected_collection = collection_names[self.index]
        else:
            self.parent.selected_collection = None