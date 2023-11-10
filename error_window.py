from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QFont


class ErrorsWindow(QMainWindow):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if self.type == 'альбом уже существует':
            self.setWindowTitle('Ошибка')
            self.setFixedSize(400, 80)
            my_font = QFont("Arial", 12)
            self.text_error = QLabel('Не оригинальное название\nАльбом с таким именем уже существует', self)
            self.text_error.setFont(my_font)
            self.text_error.setGeometry(10, 10, 385, 55)
