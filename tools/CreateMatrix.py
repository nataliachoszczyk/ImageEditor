from PyQt6.QtWidgets import QLineEdit

def create_matrix(matrix_layout, size):

    for i in reversed(range(matrix_layout.count())):
        widget = matrix_layout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()
    
    for row in range(size):
        for col in range(size):
            line_edit = QLineEdit()
            line_edit.setFixedSize(25, 25)
            
            line_edit.setStyleSheet("background-color: #EDEDED; color: black; border: 1px solid gray; border-radius: 5px; font-size: 16px")
            
            matrix_layout.addWidget(line_edit, row, col)