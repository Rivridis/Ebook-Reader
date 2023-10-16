from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout,QMessageBox,QLineEdit,QPushButton,QMainWindow,QSplashScreen,QFileDialog,QTreeView,QFileSystemModel,QTextBrowser,QTextEdit
from PySide6.QtGui import QPixmap,QTextCharFormat,QFont,QTextCursor,QColor
from PySide6.QtCore import Qt,QTimer,QPoint
from PySide6.QtUiTools import QUiLoader
import sys
from ebooklib import epub
from bs4 import BeautifulSoup
import qdarktheme
import hashlib
import time
scroll_positions = {}
qss = """
        QScrollBar::sub-page:horizontal {
        background: rgba(255, 255, 255, 0)
    }

    QScrollBar::add-page:horizontal {
        background: rgba(255, 255, 255, 0)
    }
    QScrollBar::sub-page:vertical {
        background: rgba(255, 255, 255, 0)
    }

    QScrollBar::add-page:vertical {
        background: rgba(255, 255, 255, 0)
    }
    QScrollBar::handle
    {
        background : rgba(138,124,171,1);
        min-height: 40px;
    }
    QScrollBar::handle:vertical
    {
        background : rgba(138,124,171,1);
        min-height: 40px;
    }
    QScrollBar::handle::pressed
    {
    background : rgba(138,124,171,1); 
    }
    QScrollBar::handle::hover
    {
    background : rgba(138,124,171,1);
    }
    QScrollBar::add-line,
    QScrollBar::sub-line {
        width: 0;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }


    """

def show_splash_screen():
    splash_pix = QPixmap('assets\splash.jpg')
    splash_pix = splash_pix.scaled(550, 450, Qt.KeepAspectRatio,Qt.SmoothTransformation)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    return splash

def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme(additional_qss=qss,custom_colors={
        "[dark]": {
            "primary": "#D0BCFF",
            "border": "#00000000",
            "treeSectionHeader.background":"#8a7cab"
        }
    })

    # Create and show splash screen
    splash = show_splash_screen()
    main_window = Main()
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
    
    
    def choose(self, index):
        self.file_path = self.model.filePath(index)
        if ".epub" in self.file_path:

            book = epub.read_epub(self.file_path)
            content = ""
            for item in book.items:
                if isinstance(item, epub.EpubHtml):
                    content += item.content.decode('utf-8')
            styled_content = f"""
            <html>
                <head>
                    <style>
                        body 
                        {{
                            color: rgb(255, 255, 255);
                            font-size: 16px;
                            background-color: rgba(26, 26, 29, 1);
                        }}
                    </style>
                </head>
                <body>
                    {content}
                </body>
            </html>
            """
            self.text.setHtml(styled_content)

            # Restore the scroll position if available
            if self.file_path in scroll_positions:
                text_cursor = self.text.textCursor()
                text_cursor.setPosition(scroll_positions[self.file_path])
                self.text.setTextCursor(text_cursor)
            else:
                scroll_positions[self.file_path] = 0

            print(scroll_positions)
            self.autosaveTimer = QTimer()
            self.autosaveTimer.timeout.connect(self.saveFile)
            self.autosaveTimer.setInterval(1000)
            self.autosaveTimer.start()

        else:
            QMessageBox.information(self, "Invalid filetype","Please choose another file")

    def saveFile(self):
            cursorTop = self.text.cursorForPosition(QPoint(0, 0))
            self.position = cursorTop.position()
            if self.file_path in scroll_positions:
                scroll_positions[self.file_path] = self.position
            else:
                scroll_positions[self.file_path] = 0
            print(self.position)

if __name__ == "__main__":
    main()
    
    


