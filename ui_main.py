from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout,QMessageBox,QLineEdit,QPushButton,QMainWindow,QSplashScreen,QFileDialog,QTreeView,QFileSystemModel,QTextBrowser,QTextEdit
from PySide6.QtGui import QPixmap,QTextCharFormat,QFont,QTextCursor,QColor
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
import sys
from ebooklib import epub
from bs4 import BeautifulSoup

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

        self.tree.doubleClicked.connect(self.choose)

        self.text = ui.findChild(QTextEdit,'text')
        self.text.setReadOnly(True)


    def dirpop(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", "", options=options)

        if directory:
            self.tree.setRootIndex(self.model.index(directory))
    
    def choose(self,index):
        file_path = self.model.filePath(index)
        if ".epub" in file_path:
            book = epub.read_epub(file_path)
            content = ""
            for item in book.items:
                if isinstance(item, epub.EpubHtml):
                    content += item.content.decode('utf-8')
            self.text.setHtml(content)

            #text_format = QTextCharFormat()


            # # Set font color
            # text_format.setForeground(QColor("#FFFFFF"))  # Change to desired color

            # # Set font family
            # font = QFont("garamond")  # Change to desired font family
            # text_format.setFont(font)

            # # Set font size
            # text_format.setFontPointSize(22)  # Change to desired size

            # # Apply the format to the entire document
            # cursor = self.text.textCursor()
            # cursor.select(QTextCursor.Document)
            # cursor.setCharFormat(text_format)
            
        
        else:
            QMessageBox.information(self, "Invalid filetype","Please choose another file")
        


if __name__ == "__main__":
    main()
    
    


