from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QGridLayout, QWidget, \
    QScrollArea, QTextEdit, QInputDialog
from PyQt5.QtGui import QPixmap, QFont
import sqlite3
import sys
from error_name_window import ErrorNameWindow
from PyQt5.QtCore import Qt
from gallery_album import GalleryAlbum


class MainGalleryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Альбомы')
        self.layout = QGridLayout()
        self.create_new_album = QPushButton(f"Cоздать новый альбом", self)
        self.create_new_album.resize(915, 35)
        self.create_new_album.move(0, 30)
        self.create_new_album.clicked.connect(self.name_request)
        self.resize(700, 700)
        # self.connection = sqlite3.connect('GalleryDataBase.sqlite')
        self.connection = sqlite3.connect('my_first_data_base.sqlite')
        self.cursor = self.connection.cursor()
        self.cursor.execute('SELECT album_name FROM AlbumsList')
        self.names_list = [row[0] for row in self.cursor.fetchall()]  # получаем список названий альбомов
        self.image_album_camera = QPixmap('camera.jpg').scaled(150, 150)
        self.layout = QGridLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.resize(915, 900)
        self.scroll_area.move(0, 100)
        self.setFixedSize(915, 1050)
        self.move(0, 0)
        self.display_albums(self.names_list)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.cursor.execute('SELECT album_name FROM AlbumsList')
            self.upgrated_list = [row[0] for row in self.cursor.fetchall()]
            self.display_albums(self.upgrated_list)

    def name_registering(self, name):
        self.cursor.execute(f'''INSERT INTO AlbumsList (album_name) VALUES ('{name}') ''')
        self.connection.commit()
        self.names_list = [row[0] for row in self.cursor.fetchall()]
        self.display_albums(self.names_list)

    def name_request(self):
        window = QInputDialog()
        album_name, ok_pressed = window.getText(self, "Создать новый альбом?",
                                                "Введите название нового альбома                          ")
        if ok_pressed:
            if not (album_name in self.names_list):
                self.name_registering(album_name)
            else:
                self._ = ErrorNameWindow()
                self._.show()

    def display_albums(self, ist):
        row = 0
        col = 0
        for i in ist:
            j = 0
            image = QLabel()
            image.resize(220, 210)
            image.setPixmap(self.image_album_camera)
            self.btn = QPushButton(f"{i}")
            self.btn.id = i
            self.btn.clicked.connect(self.open_this_album)
            self.btn.setFixedSize(220, 30)
            self.layout.addWidget(image, row, col % 4)
            self.layout.addWidget(self.btn, row + 1, col % 4)
            self.widget = QWidget()
            self.widget.setLayout(self.layout)
            self.scroll_area.setWidget(self.widget)
            col += 1
            if col % 4 == 0:
                row += 2
            j += 1

    def open_this_album(self):
        self.album = GalleryAlbum(self.btn.sender().id)
        self.album.show()


app = QApplication(sys.argv)
ex = MainGalleryWindow()
ex.show()
sys.exit(app.exec_())
