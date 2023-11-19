from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, \
    QGridLayout, QWidget, \
    QScrollArea, QInputDialog, QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
import sqlite3
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PIL import Image


class MainGalleryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #e7cbd2")
        self.setWindowTitle('Альбомы')
        self.names_list = []
        self.layout = QGridLayout()
        self.create_new_album = QPushButton(f"Cоздать  новый  альбом", self)
        font = QFont("Comic Sans MS", 20)
        font.setBold(True)
        style = (
            "QPushButton {"
            "   background-color: #55485a;"  # Цвет фона
            "   color: white;"  # Цвет текста
            "   border-radius: 9px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #ababcb;"
            "}"
        )
        self.create_new_album.setStyleSheet(style)
        self.create_new_album.setFont(font)
        self.create_new_album.resize(399, 45)
        self.create_new_album.move(258, 30)
        self.create_new_album.clicked.connect(self.name_request)
        self.resize(700, 700)
        self.connection = sqlite3.connect('GalleryDataBase.sqlite')
        self.cursor = self.connection.cursor()
        self.update_name_list()
        self.image_album_camera = QPixmap('3.png').scaled(214, 200)
        self.layout.setContentsMargins(5, 10, 5, 5)
        self.layout.setSpacing(10)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.resize(916, 881)
        self.scroll_area.move(0, 100)
        self.scroll_area.setStyleSheet("background-color: #55485a; ")
        self.resize(915, 980)
        self.move(0, 0)
        self.display_albums(self.names_list)
        font = QFont("Comic Sans MS", 16)
        font.setBold(True)
        self.help_user = QPushButton('help', self)
        self.help_user.setFont(font)
        self.help_user.resize(100, 37)
        self.help_user.move(50, 35)
        style1 = (
            "QPushButton {"
            "   background-color: #55485a;"  # Цвет фона
            "   color: white;"  # Цвет текста
            "   border-radius: 9px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #ababcb;"
            "}"
        )
        self.help_user.setStyleSheet(style1)
        self.help_user.clicked.connect(self.memo_help)

    def memo_help(self):
        self.x = MemoWindow()
        self.x.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.update_name_list()
            self.display_albums(self.names_list)
        if int(event.modifiers()) == Qt.CTRL:
            if event.key() == Qt.Key_F:
                self.search()
        if int(event.modifiers()) == Qt.CTRL:
            if event.key() == Qt.Key_H:
                self.memo_help()

    def name_registering(self, name):
        self.cursor.execute(f'''INSERT INTO AlbumsList (album_name) VALUES ('{name}') ''')
        self.connection.commit()
        self.update_name_list()
        self.display_albums(self.names_list)

    def name_request(self):
        window = QInputDialog()
        a, ok_pressed = window.getText(self, "Создать новый альбом?",
                                       "Введите название нового альбома                          ")
        self.update_name_list()
        if ok_pressed:
            _ = a.lstrip()
            album_name = _.rstrip()
            if album_name == '':
                self._ = ErrorsWindow('Пустая строка')
                self._.show()
            elif not (album_name in self.names_list) and album_name != '':
                self.name_registering(album_name)
            elif album_name in self.names_list:
                self._ = ErrorsWindow('Альбом уже существует')
                self._.show()

    def update_name_list(self):
        self.cursor.execute('SELECT album_name FROM AlbumsList')
        self.names_list = [row[0] for row in self.cursor.fetchall()]

    def clearLayout(self):
        layout = self.layout
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def display_albums(self, ist):
        row = 0
        col = 0
        self.clearLayout()
        if not ist:
            self.cursor.execute('SELECT album_name FROM AlbumsList')
            ist = [row[0] for row in self.cursor.fetchall()]
        for i in ist:
            j = 0
            image = QLabel()
            image.resize(214, 200)
            image.setPixmap(self.image_album_camera)
            self.btn = QPushButton(f"{i}")
            self.btn.id = i
            style = (
                "QPushButton {"
                "   background-color: #f7dbc0;"  # Цвет фона
                "   color: #303030;"  # Цвет текста
                "   border-radius: 10px;"
                "}"
                "QPushButton:hover {"
                "   background-color: lightgray;"
                "}"
            )
            self.btn.setStyleSheet(style)
            font = QFont("Comic Sans MS", 16)
            font.setBold(True)
            self.btn.setFont(font)
            self.btn.clicked.connect(self.open_this_album)
            self.btn.setFixedSize(214, 30)
            self.layout.addWidget(image, row, col % 4)
            self.layout.addWidget(self.btn, row + 1, col % 4)
            self.widget = QWidget()
            self.widget.setLayout(self.layout)
            self.scroll_area.setWidget(self.widget)
            col += 1
            if col % 4 == 0:
                row += 2
            j += 1

    def open_this_album(self, window=None):
        if window:
            win = window
        else:
            win = self.btn.sender().id
        self.album = GalleryAlbum(win, ex)
        self.album.show()

    def search(self):
        window = QInputDialog()
        album_name, ok_pressed = window.getText(self, "Найти",
                                                "Введите название искомого альбома                        ")
        if ok_pressed:
            self.cursor.execute(f'''SELECT album_name FROM AlbumsList
            WHERE album_name == "{album_name}"''')
            b = self.cursor.fetchall().copy()
            if b:
                self.open_this_album(b[0][0])
            else:
                self._ = ErrorsWindow('альбом не найден')
                self._.show()


class GalleryAlbum(QMainWindow):
    def __init__(self, name_album, mw):
        super().__init__()
        self.mw = mw
        self.setStyleSheet("background-color: #e7cbd2")
        self.list_for_photos = []
        self.connection = sqlite3.connect('GalleryDataBase.sqlite')
        self.cursor = self.connection.cursor()
        self.setWindowTitle(f'Альбом: {name_album}')
        self.name_album = name_album
        self.layout = QGridLayout()
        self.layout.setContentsMargins(5, 10, 5, 5)
        self.add_button = QPushButton(f"Добавить в {self.name_album}", self)
        font = QFont("Comic Sans MS", 20)
        font.setBold(True)
        style = ("QPushButton {"
                 "   background-color: #55485a;"  # Цвет фона
                 "   color: white;"  # Цвет текста
                 "   border-radius: 15px;"
                 "}")
        self.add_button.setFont(font)
        self.add_button.setStyleSheet(style)
        self.add_button.resize(355, 45)
        self.add_button.move(280, 30)
        self.add_button.clicked.connect(self.add_photo)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.resize(915, 900)
        self.scroll_area.move(0, 100)
        self.scroll_area.setStyleSheet("background-color: #55485a")
        self.setFixedSize(915, 1050)
        self.move(0, 0)
        self.row = 0
        self.col = 0
        self.display_photos()

    def memo_help(self):
        self.x = MemoWindow()
        self.x.show()

    def keyPressEvent(self, event):
        try:
            if event.key() == Qt.Key_Delete:
                self.cursor.execute(f'''DELETE from AlbumsList WHERE Album_name == "{self.name_album}"''')
                self.connection.commit()
                self.cursor.execute('SELECT album_name FROM AlbumsList')
                ist = [row[0] for row in self.cursor.fetchall()]
                self.close()
                self.mw.display_albums(ist)
                self.connection.close()
                self.connection = sqlite3.connect('GalleryDataBase.sqlite')
                self.cursor = self.connection.cursor()
                self.cursor.execute(
                    f'''SELECT full_photo_path FROM Photos WHERE album_name LIKE "%{self.name_album}%" ''')
                b = [i[0] for i in self.cursor.fetchall()]
                for j in b:
                    self.cursor.execute(f'''SELECT album_name FROM Photos WHERE full_photo_path == "{j}" ''')
                    x = ''.join([i[0] for i in self.cursor.fetchall()]).split('√')
                    x.remove(self.name_album)
                    if x:
                        self.cursor.execute(
                            f'''UPDATE Photos SET album_name == "{'√'.join(x)}" WHERE full_photo_path == "{j}" ''')
                        self.connection.commit()
                    elif not x:
                        self.cursor.execute(
                            f'''DELETE FROM Photos WHERE full_photo_path == "{j}" ''')
                        self.connection.commit()
            if int(event.modifiers()) == Qt.CTRL:
                if event.key() == Qt.Key_H:
                    self.memo_help()
        except Exception:
            pass

    def pil_to_qpixmap(self, pil_image):
        # Преобразование изображения PIL в QPixmap
        image_data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
        qt_image = QPixmap.fromImage(QImage(image_data, pil_image.width, pil_image.height, QImage.Format_RGBA8888))
        return qt_image

    def clearLayout(self):
        layout = self.layout
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def add_photo(self):
        try:
            photo_info = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')
            photo_path = photo_info[0]
            self.cursor.execute(f'''SELECT album_name FROM Photos WHERE full_photo_path == "{photo_path}"''')
            _ = [i[0] for i in self.cursor.fetchall()]
            if self.name_album in _:
                pass
            elif not _:  # если фотографии нету нигде
                self.cursor.execute(f'''
                INSERT INTO Photos (full_photo_path, album_name) VALUES ("{photo_path}", "{self.name_album}")
                                    ''')
                self.connection.commit()
                self.add_now(photo_path)
            elif not (self.name_album in ' '.join(_)):  # если фотографии нету в данном альбоме
                self.cursor.execute(f'''SELECT album_name FROM Photos WHERE full_photo_path == "{photo_path}"''')
                value_albums = f"{self.cursor.fetchall()[0][0]}√{self.name_album}"
                self.cursor.execute(f'''
                        UPDATE Photos SET album_name == "{value_albums}" WHERE full_photo_path == "{photo_path}"
                                    ''')
                self.connection.commit()
                self.add_now(photo_path)
        except Exception:
            pass

    def add_now(self, photo_path):
        object_expansion = photo_path.split('.')[-1]
        ph = ['jpg', 'jpeg', 'png', 'gif']
        vd = ['mvk', 'gifv', 'mng', 'avi', '3gp']
        cd = ['py']
        tx = ['txt', 'docx']
        if object_expansion in ph:
            pil_image = Image.open(photo_path).resize((220, 200))
            qt_pixmap = self.pil_to_qpixmap(pil_image)
            image = QLabel()
            image.resize(220, 210)
            image.setPixmap(qt_pixmap)
            self.btn = QPushButton("Просмотр")
            self.btn.id = photo_path
            style = (
                "QPushButton {"
                "   background-color: #f7dbc0;"  # Цвет фона
                "   color: #303030;"  # Цвет текста
                "   border-radius: 10px;"
                "}"
                "QPushButton:hover {"
                "   background-color: lightgray;"
                "}")
            self.btn.setStyleSheet(style)
            font = QFont("Comic Sans MS", 16)
            font.setBold(True)
            self.btn.setFont(font)
            self.btn.setFixedSize(220, 30)
            self.btn.clicked.connect(self.this_photo)
            self.layout.addWidget(image, self.row, self.col % 4)
            self.layout.addWidget(self.btn, self.row + 1, self.col % 4)
            self.widget = QWidget()
            self.widget.setLayout(self.layout)
            self.scroll_area.setWidget(self.widget)
            self.col += 1
            if self.col % 4 == 0:
                self.row += 2

    def display_photos(self):
        self.clearLayout()
        self.cursor.execute(f''' SELECT full_photo_path FROM Photos'
                                'WHERE album_name LIKE "%{self.name_album}%" ''')
        self.list_for_photos = [i[0] for i in self.cursor.fetchall()]
        for photo_path in self.list_for_photos:
            photo_expansion = photo_path.split('/')[-1].split('.')[-1]
            if photo_expansion == 'jpeg' or \
                    photo_expansion == 'png' or \
                    photo_expansion == 'jpg' or \
                    photo_expansion == 'gif':
                pil_image = Image.open(photo_path).resize((220, 200))
                qt_pixmap = self.pil_to_qpixmap(pil_image)
                image = QLabel()
                image.resize(220, 210)
                image.setPixmap(qt_pixmap)
                self.btn = QPushButton("Просмотр")
                self.btn.id = photo_path
                style = (
                    "QPushButton {"
                    "   background-color: #f7dbc0;"  # Цвет фона
                    "   color: #303030;"  # Цвет текста
                    "   border-radius: 10px;"
                    "}"
                    "QPushButton:hover {"
                    "   background-color: lightgray;"
                    "}"
                )
                self.btn.setStyleSheet(style)
                font = QFont("Comic Sans MS", 16)
                font.setBold(True)
                self.btn.setFont(font)
                self.btn.setFixedSize(220, 30)
                self.btn.clicked.connect(self.this_photo)
                self.layout.addWidget(image, self.row, self.col % 4)
                self.layout.addWidget(self.btn, self.row + 1, self.col % 4)
                self.widget = QWidget()
                self.widget.setLayout(self.layout)
                self.scroll_area.setWidget(self.widget)
                self.col += 1
                if self.col % 4 == 0:
                    self.row += 2

    def this_photo(self):
        self.window_this_photo = PhotoGallery(self.btn.sender().id, self.name_album)
        self.window_this_photo.show()


class PhotoGallery(QMainWindow):
    def __init__(self, path, album):
        super().__init__()
        self.connection = sqlite3.connect('GalleryDataBase.sqlite')
        self.setStyleSheet("background-color: #2c2c44")
        self.cursor = self.connection.cursor()
        self.path = path
        self.album = album
        self.move(0, 0)
        self.setFixedSize(1920, 1000)
        self.label = QLabel()
        pixmap = QPixmap(self.path).scaled(1500, 975, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.w = QWidget()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.w)
        self.scroll_area.move(400, 10)
        self.scroll_area.resize(1509, 980)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setStyleSheet("background-color: #2c2c44; border: 3px solid #c3aed6; border-radius: 8px")
        t = QLabel('Заметки ', self)
        t.move(113, 380)
        t.resize(176, 52)
        t.setFont(QFont('Montserrat', 25))
        t.setStyleSheet("border: 3px solid #ababcb; padding: 5px; border-radius: 10px; background-color: #f6f6f6")

        self.text_zone = QTextEdit(self)
        self.cursor.execute(f'''SELECT remark FROM Photos WHERE full_photo_path == "{self.path}" ''')
        a = [i[0] for i in self.cursor.fetchall()][0]
        if a:
            self.text_zone.setText(a)
        self.text_zone.move(20, 470)
        self.text_zone.resize(376, 395)
        self.text_zone.move(11, 450)
        font = QFont("Arial", 16)
        font.setBold(True)
        self.text_zone.setFont(font)
        self.text_zone.setStyleSheet(
            "background-color: #2c2c44; color: white; border: 2px solid white; border-radius: 15px")
        text_save = 'Сохранить заметку'
        text_del = 'Удалить заметку'
        self.save_text_btn = QPushButton(text_save, self)
        font = QFont("Comic Sans MS", 18)
        font.setBold(True)
        self.save_text_btn.setFont(font)
        self.save_text_btn.resize(236, 50)
        self.save_text_btn.move(82, 862)
        style = (
            "QPushButton {" "border: 3px solid #8675a9;"
            "   background-color: #e8e2f0;"  # Цвет фона
            "   color: #303030;"  # Цвет текста
            "   border-radius: 19px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #ababcb;"
            "}")
        self.save_text_btn.setStyleSheet(style)
        self.save_text_btn.clicked.connect(self.save_text)
        self.del_text_btn = QPushButton(text_del, self)
        font = QFont("Comic Sans MS", 18)
        font.setBold(True)
        self.del_text_btn.setFont(font)
        self.del_text_btn.resize(236, 50)
        self.del_text_btn.move(82, 930)
        self.del_text_btn.clicked.connect(self.del_text)
        style1 = (
            "QPushButton {"
            "   background-color: #d76767;"  # Цвет фона
            "   color: #303030;"  # Цвет текста
            "   border-radius: 19px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #ababcb;"
            "}"
        )
        self.del_text_btn.setStyleSheet(style1)

    def save_text(self):
        try:
            a = self.text_zone.toPlainText()
            self.cursor.execute(f'''UPDATE Photos SET remark == "{a}" WHERE full_photo_path == "{self.path}"''')
            self.connection.commit()
        except Exception as e:
            pass

    def del_text(self):
        self.cursor.execute(f'''UPDATE Photos SET remark == "" WHERE full_photo_path == "{self.path}"''')
        self.connection.commit()

    def memo_help(self):
        self.x = MemoWindow()
        self.x.show()

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.CTRL:
            if event.key() == Qt.Key_H:
                self.memo_help()


class ErrorsWindow(QMainWindow):
    def __init__(self, e_type):
        super().__init__()
        self.type = e_type
        self.setStyleSheet("background-color: #2c2c44")
        if self.type == 'Альбом уже существует':
            error_text = 'Не оригинальное название\nАльбом с таким именем уже существует'
            self.error(error_text)
        elif self.type == 'альбом не найден':
            error_text = 'Такого альбома нет\nПожалуйста, проверьте правильность\nнаписания названия'
            self.error(error_text)
        elif self.type == 'Пустая строка':
            error_text = 'Реально, хотите альбом "Ничего"?\nПожалуйста, проверьте правильность\nнаписания названия'
            self.error(error_text)

    def error(self, er_txt):
        self.setWindowTitle('Ошибка')
        self.setFixedSize(550, 150)
        my_font = QFont("Arial", 18)
        self.text_error = QLabel(er_txt, self)
        self.text_error.setFont(my_font)
        self.text_error.setStyleSheet("background-color: #2c2c44; color: #e5e5e5")
        self.text_error.setGeometry(12, 0, 535, 150)


class MemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        memo_text = ''.join(open('memo.txt', encoding="utf-8").readlines())
        t = QLabel('Памятка пользователю ', self)
        t.move(235, 30)
        t.resize(430, 50)
        t.setFont(QFont('Montserrat', 25))
        t.setStyleSheet("border: 3px solid #ababcb; padding: 5px; border-radius: 10px; background-color: #f6f6f6")
        self.resize(900, 680)
        self.setStyleSheet("background-color: #2c2c44")
        self.text_zone = QTextEdit(self)
        font = QFont("Comic Sans MS", 16)
        font.setBold(True)
        self.text_zone.setFont(font)
        self.text_zone.resize(890, 550)
        self.text_zone.move(5, 130)
        self.text_zone.setStyleSheet(
            "background-color: #2c2c44; color: white; border: 2px solid white; border-radius: 15px")
        self.text_zone.setText(memo_text)


app = QApplication(sys.argv)
ex = MainGalleryWindow()
ex.show()
sys.exit(app.exec_())
