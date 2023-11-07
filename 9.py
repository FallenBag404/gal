# def keyPressEvent(self, event):
#     if int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
#         if event.key() == Qt.Key_R:
#             row = 0
#             col = 0
#             for i in self.names_list:
#                 j = 0
#                 image = QLabel()
#                 image.resize(220, 210)
#                 image.setPixmap(self.image_album_camera)
#                 self.btn = QPushButton(f"{i[j]}")
#                 # self.btn.id = i
#                 self.btn.setFixedSize(220, 30)
#                 self.layout.addWidget(image, row, col % 4)
#                 self.layout.addWidget(self.btn, row + 1, col % 4)
#                 self.widget = QWidget()
#                 self.widget.setLayout(self.layout)
#                 self.scroll_area.setWidget(self.widget)
#                 col += 1
#                 if col % 4 == 0:
#                     row += 2
#                 j += 1