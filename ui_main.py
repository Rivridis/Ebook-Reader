from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout,QMessageBox,QLineEdit,QPushButton,QMainWindow,QSplashScreen,QFileDialog,QTreeView,QFileSystemModel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
import sys


import time

def show_splash_screen():
    splash_pix = QPixmap('assets\splash.jpg')
    splash_pix = splash_pix.scaled(550, 450, Qt.KeepAspectRatio,Qt.SmoothTransformation)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    return splash

def main():
    app = QApplication(sys.argv)

    # Create and show splash screen
    splash = show_splash_screen()
    main_window = Main()
    time.sleep(1)
    splash.close()

    main_window.children()[1].show()

    sys.exit(app.exec())

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        
        loader = QUiLoader()
        ui_file = "assets/main.ui" 
        ui = loader.load(ui_file, self)

        self.directory = ui.findChild(QPushButton,"direct")
        self.directory.clicked.connect(self.dirpop)

        self.tree = ui.findChild(QTreeView,"tree")

        self.model = QFileSystemModel()
        self.model.setRootPath("/")
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index("/"))


    def dirpop(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", "", options=options)

        if directory:
            self.tree.setRootIndex(self.model.index(directory))


if __name__ == "__main__":
    main()
    


