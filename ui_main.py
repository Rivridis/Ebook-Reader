import PySide6
from PySide6.QtWidgets import QApplication, QMessageBox,QPushButton,QMainWindow,QSplashScreen,QFileDialog,QTreeView,QFileSystemModel,QTextEdit
from PySide6.QtGui import QPixmap,QStandardItem,QStandardItemModel
from PySide6.QtCore import Qt,QTimer,QStandardPaths,QCoreApplication
from PySide6.QtUiTools import QUiLoader
import sys
import ebooklib
from ebooklib import epub
import hashlib
import time
import json
from bs4 import BeautifulSoup

try:
    with open('scroll_positions.json', 'r') as json_file:
        scroll_positions = json.load(json_file)
except FileNotFoundError:
    # If the file doesn't exist yet, create an empty dictionary
    scroll_positions = {}


def show_splash_screen():
    splash_pix = QPixmap(r"B:\Github\Ebook-Reader\assets\splash.jpg")
    splash_pix = splash_pix.scaled(550, 450, Qt.KeepAspectRatio,Qt.SmoothTransformation)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    return splash

def main():
    app = QApplication(sys.argv)
    qss=r"B:\Github\Ebook-Reader\style.qss"
    with open(qss,"r") as qs:
        app.setStyleSheet(qs.read())
    # Create and show splash screen
    splash = show_splash_screen()
    main_window = Main()
    time.sleep(1)
    splash.close()

    main_window.children()[1].showFullScreen()
    sys.exit(app.exec())

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file_hash = None
        loader = QUiLoader()
        ui_file = r"B:\Github\Ebook-Reader\main.ui" 
        ui = loader.load(ui_file, self)

        self.directory = ui.findChild(QPushButton,"direct")
        self.directory.clicked.connect(self.dirpop)

        self.content = ui.findChild(QPushButton,"content")
        self.content.clicked.connect(self.confil)

        self.exit = ui.findChild(QPushButton,"exit")
        self.exit.clicked.connect(QCoreApplication.instance().quit)

        self.settings = ui.findChild(QPushButton,"settings")
        self.settings.clicked.connect(self.sett)

        self.tree = ui.findChild(QTreeView,"tree")
        downloads_path = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)

        self.model = QFileSystemModel()
        self.model.setRootPath(downloads_path)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(downloads_path))

        self.tree.doubleClicked.connect(self.choose)

        self.text = ui.findChild(QTextEdit,'text')
        self.text.setReadOnly(True)
        self._resize_start_cursor = None
        self.scroll_bar = self.text.verticalScrollBar()
        self.scroll_bar.valueChanged.connect(self.save_scroll_position)

    def sett(self):
        pass
        
    def confil(self):
        if self.current_file_hash:
            chapters = []

            for item in self.book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    title = soup.find('h1')  # Assuming the chapter titles are in h1 tags
                    if title:
                        chapters.append(title.get_text())
            self.displayChaptersInTreeView(chapters)

    def displayChaptersInTreeView(self, chapters):
        model = QStandardItemModel()
        self.tree.doubleClicked.disconnect() 
        
        for chapter in chapters:
            item = QStandardItem(chapter)
            item.setEditable(False)
            model.appendRow(item)
        model.setHorizontalHeaderLabels(["Chapter List"])
        self.tree.setModel(model)
            
    def dirpop(self):
        self.tree.setModel(self.model)
        self.tree.doubleClicked.connect(self.choose)
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", "", options=options)

        if directory:
            self.tree.setRootIndex(self.model.index(directory))
    
    def generate_file_hash(self, content):
        sha256 = hashlib.sha256()
        sha256.update(content.encode('utf-8'))
        return sha256.hexdigest()

    
    def save_scroll_position(self):
        if self.current_file_hash:
            QTimer.singleShot(300, lambda: self._save_scroll_position())

    def _save_scroll_position(self):
        max_value = self.scroll_bar.maximum()
        scroll_positions[self.current_file_hash] = [self.scroll_bar.value(), max_value]
        with open('scroll_positions.json', 'w') as json_file:
            json.dump(scroll_positions, json_file)
    
    def choose(self, index):
        file_path = self.model.filePath(index)
        if ".epub" in file_path:
            self.scroll_bar.valueChanged.disconnect(self.save_scroll_position)
            self.book = epub.read_epub(file_path)
            content = ""
            for item in self.book.items:
                if isinstance(item, epub.EpubHtml):
                    content += item.content.decode('utf-8')
            styled_content = f"""
            <html>
                <head>
                    <style>
                        body 
                        {{
                            color: rgba(210,210,210,1);
                            font-size: 18px;
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
            #self.text.setWordWrapMode(QTextOption.NoWrap)

            # Generate a unique hash for the current file
            self.current_file_hash = self.generate_file_hash(content)


            if self.current_file_hash in scroll_positions.keys():
                QTimer.singleShot(100, lambda: self.scroll_bar.setValue(scroll_positions[self.current_file_hash][0]))
            self.scroll_bar.valueChanged.connect(self.save_scroll_position)
            

        else:
            QMessageBox.information(self, "Invalid filetype","Please choose another file")

main()
input()