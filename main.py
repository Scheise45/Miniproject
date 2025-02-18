import os
import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt
from map_request import get_map_image

SCREEN_SIZE = [600, 450]
MOVE_STEP = 5  # Шаг перемещения карты


class MapViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.map_file = "map.png"

        # Начальные параметры карты
        # Центр карты (нулевой меридиан, экватор)
        self.lon, self.lat = 0.0, 0.0
        self.spn = 180.0  # Размер области просмотра

        self.load_map()
        self.initUI()

    def load_map(self):
        """Загружает карту с текущими параметрами"""
        self.map_file = get_map_image(self.lon, self.lat, self.spn)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Управление картой (стрелки)')

        # Отображение карты
        self.image = QLabel(self)
        self.image.setGeometry(0, 0, *SCREEN_SIZE)
        self.update_map()

    def update_map(self):
        """Перерисовывает карту после изменения координат"""
        self.load_map()
        pixmap = QPixmap(self.map_file)
        self.image.setPixmap(pixmap)

    def keyPressEvent(self, event):
        """Обрабатывает нажатие клавиш (стрелок)"""
        if event.key() == Qt.Key.Key_Up:
            self.lat = min(90, self.lat + MOVE_STEP)  # Двигаемся вверх
        elif event.key() == Qt.Key.Key_Down:
            self.lat = max(-90, self.lat - MOVE_STEP)  # Двигаемся вниз
        elif event.key() == Qt.Key.Key_Left:
            self.lon = max(-180, self.lon - MOVE_STEP)  # Двигаемся влево
        elif event.key() == Qt.Key.Key_Right:
            self.lon = min(180, self.lon + MOVE_STEP)  # Двигаемся вправо
        else:
            return

        self.update_map()  # Перерисовываем карту

    def closeEvent(self, event):
        """Удаляем файл при выходе"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec())
