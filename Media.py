# PyQt6 for web popup
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
#for images (not implemented yet)
from PIL import Image, ImageTk
import os

folderloc = input("Enter the folder location of the pngs: ")
filedirect = os.listdir(folderloc)
for i in filedirect:
    print(i)

# PyQt6 implementing???
class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Player")
        self.setGeometry(100, 100, 800, 600)
        button = QPushButton("Exit")
        input = QLineEdit()
        input.setMaximumHeight(30)
        button.setFixedSize(200, 30)
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(input)
        self.setMenuWidget(button)
        input.setPlaceholderText("Search here:")
        input.text()

    def button_clicked(self):
        exit()
app = QApplication([])

mdpl = MW()
mdpl.show()
app.exec()

print("Done")