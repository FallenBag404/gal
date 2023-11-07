from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, \
    QScrollArea, QTextEdit
from PyQt5.QtGui import QPixmap, QFont


class PhotoGallery(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.move(0, 0)
        self.setFixedSize(1920, 1000)
        self.layout = QGridLayout()
        self.label = QLabel()
        pixmap = QPixmap(self.path)
        self.label.setPixmap(pixmap)
        self.layout.addWidget(self.label)
        self.w = QWidget()
        self.w.setLayout(self.layout)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.w)
        self.scroll_area.move(400, 10)
        self.scroll_area.resize(1520, 980)
        t = QLabel('Заметки: ', self)
        t.move(150, 640)
        t.resize(160, 25)
        t.setFont(QFont('Montserrat', 15))
        self.text_ = QTextEdit(self)
        self.text_.move(20, 670)
        self.text_.resize(350, 300)
