import os
import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QInputDialog
from map_request import get_map_image  # Импортируем функцию из map_request.py

SCREEN_SIZE = [600, 450]


class MapViewer(QWidget):
    def __init__(self):
        super().__init__()

        # Запрашиваем spn у пользователя
        self.spn = self.get_spn_from_user()

        # Загружаем карту Москвы с заданным spn
        self.lon, self.lat = 37.6173, 55.7558
        self.map_file = get_map_image(self.lon, self.lat, self.spn)

        self.initUI()

    def get_spn_from_user(self):
        """Запрашиваем у пользователя spn (масштаб карты)"""
        spn, ok = QInputDialog.getDouble(self, "Выбор масштаба",
                                         "Введите spn (0.001 - 10.0):",
                                         0.1, 0.001, 10.0, 3)
        return spn if ok else 0.1  # Если отмена — значение по умолчанию

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Карта Москвы')

        # Загружаем изображение карты
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.setGeometry(0, 0, *SCREEN_SIZE)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """Удаление файла при закрытии"""
        if self.map_file and os.path.exists(self.map_file):
            os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec())
