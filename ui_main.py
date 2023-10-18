from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout,QMessageBox,QLineEdit,QPushButton,QMainWindow,QSplashScreen,QFileDialog,QTreeView,QFileSystemModel,QTextBrowser,QTextEdit
from PySide6.QtGui import QPixmap,QTextCharFormat,QFont,QTextCursor,QColor
from PySide6.QtCore import Qt,QTimer,QStandardPaths
from PySide6.QtUiTools import QUiLoader
import sys
from ebooklib import epub
import qdarktheme
import hashlib
import time
import json

try:
    with open('scroll_positions.json', 'r') as json_file:
        scroll_positions = json.load(json_file)
except FileNotFoundError:
    # If the file doesn't exist yet, create an empty dictionary
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
    time.sleep(1)
    splash.close()

    main_window.children()[1].show()

    sys.exit(app.exec())

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file_hash = None
        loader = QUiLoader()
        ui_file = "main.ui" 
        ui = loader.load(ui_file, self)

        self.directory = ui.findChild(QPushButton,"direct")
        self.directory.clicked.connect(self.dirpop)

        self.tree = ui.findChild(QTreeView,"tree")
        downloads_path = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)

        self.model = QFileSystemModel()
        self.model.setRootPath(downloads_path)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(downloads_path))

        self.tree.doubleClicked.connect(self.choose)

        self.text = ui.findChild(QTextEdit,'text')
        self.text.setReadOnly(True)
        self.scroll_bar = self.text.verticalScrollBar()
        self.scroll_bar.valueChanged.connect(self.save_scroll_position)

    def dirpop(self):
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
            scroll_positions[self.current_file_hash] = self.scroll_bar.value()
            with open('scroll_positions.json', 'w') as json_file:
                json.dump(scroll_positions, json_file)

    
    def choose(self, index):
        file_path = self.model.filePath(index)
        if ".epub" in file_path:
            self.scroll_bar.valueChanged.disconnect(self.save_scroll_position)
            book = epub.read_epub(file_path)
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
                            color: rgba(197,197,197,1);
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

            # Generate a unique hash for the current file
            self.current_file_hash = self.generate_file_hash(content)


            if self.current_file_hash:
                QTimer.singleShot(100, lambda: self.scroll_bar.setValue(scroll_positions[self.current_file_hash]))
            self.scroll_bar.valueChanged.connect(self.save_scroll_position)
            

        else:
            QMessageBox.information(self, "Invalid filetype","Please choose another file")

if __name__ == "__main__":
    main()
    


