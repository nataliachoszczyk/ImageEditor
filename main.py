import sys
from PyQt6.QtWidgets import QApplication
from app.app import ImageEditor

if __name__ == '__main__':
    app = QApplication(sys.argv)    
    editor = ImageEditor()    
    editor.show()
    sys.exit(app.exec())
