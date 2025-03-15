import sys
from PyQt6.QtWidgets import QApplication
from app.app import ImageEditor
from PyQt6.QtGui import QIcon

if __name__ == '__main__':
    app = QApplication(sys.argv)    
    editor = ImageEditor()    
    editor.setWindowTitle('Image Editor')
    editor.setWindowIcon(QIcon("logo.ico"))
    editor.show()
    sys.exit(app.exec())