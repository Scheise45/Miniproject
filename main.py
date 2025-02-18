import os
import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from map_request import get_map_image  # Импортируем функцию из map_request.py

SCREEN_SIZE = [600, 450]


class MapViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.map_file = get_map_image()  # Загружаем карту
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        # Загружаем изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*SCREEN_SIZE)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """Удаление файла при закрытии"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec())
