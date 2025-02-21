import os
import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QInputDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from map_request import get_map_image  # Импортируем функцию из map_request.py

SCREEN_SIZE = [600, 450]


class MapLoaderThread(QThread):
    """Поток для загрузки карты."""
    finished = pyqtSignal(str)

    def __init__(self, lon, lat, spn):
        super().__init__()
        self.lon = lon
        self.lat = lat
        self.spn = spn

    def run(self):
        map_file = get_map_image(self.lon, self.lat, self.spn)
        self.finished.emit(map_file)


class MapViewer(QWidget):
    def __init__(self):
        super().__init__()

        # Запрашиваем spn у пользователя
        self.spn = self.get_spn_from_user()

        # Центр Москвы
        self.lon, self.lat = 37.6173, 55.7558
        self.map_file = None  # Файл карты (изначально нет)
        self.loading = False  # Флаг загрузки карты

        self.initUI()
        self.load_map()  # Запускаем загрузку карты

    def get_spn_from_user(self):
        """Запрашиваем у пользователя spn (масштаб карты)"""
        spn, ok = QInputDialog.getDouble(self, "Выбор масштаба",
                                         "Введите spn (0.001 - 10.0):",
                                         0.1, 0.001, 10.0, 3)
        return spn if ok else 0.1  # Если отмена — значение по умолчанию

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Карта Москвы')

        # Отображение карты
        self.image = QLabel(self)
        self.image.setGeometry(0, 0, *SCREEN_SIZE)

    def load_map(self):
        """Запуск потока загрузки карты"""
        if self.loading:
            return  # Избегаем повторной загрузки

        self.loading = True
        self.image.setText("Загрузка карты...")  # Отображаем текст вместо карты
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.thread = MapLoaderThread(self.lon, self.lat, self.spn)
        self.thread.finished.connect(self.on_map_loaded)
        self.thread.start()

    def on_map_loaded(self, filename):
        """Обновление интерфейса после загрузки карты"""
        self.map_file = filename
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.loading = False  # Разблокируем управление

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if self.loading:  # Если карта загружается, управление заблокировано
            return

        if event.key() == Qt.Key.Key_Up:
            self.change_scale(-0.5)  # Увеличиваем масштаб
        elif event.key() == Qt.Key.Key_Down:
            self.change_scale(0.5)  # Уменьшаем масштаб

    def change_scale(self, delta):
        """Изменение масштаба карты с учётом пределов"""
        new_spn = max(0.001, min(10.0, self.spn + delta))

        if new_spn != self.spn:
            self.spn = new_spn
            self.load_map()  # Загружаем карту с новым масштабом

    def closeEvent(self, event):
        """Удаление файла при закрытии"""
        if self.map_file and os.path.exists(self.map_file):
            os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec())
