from PyQt5.QtWidgets import QMainWindow, QLabel

# try:
#     error_window = QMainWindow()
#     error_window.setFixedSize(150, 60)
#     text_error = QLabel('Не оригинальное название \n Альбом с таким именем уже существует')
#     text_error.resize(100, 30)
#     text_error.setParent(error_window)
#     error_window.show()
# except Exception as e:
#     print(e)
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

app = QApplication([])
error_window = QMainWindow()
error_window.setFixedSize(230, 80)
text_error = QLabel('Не оригинальное название \n Альбом с таким именем уже существует', error_window)
text_error.setGeometry(10, 10, 220, 40)
error_window.show()
app.exec_()
