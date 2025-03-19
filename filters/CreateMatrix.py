from PyQt6.QtWidgets import QLineEdit

def create_matrix(matrix_layout, size):
    # Czyszczenie starego layoutu
    for i in reversed(range(matrix_layout.count())):
        widget = matrix_layout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()
    
    # Tworzenie nowej macierzy
    for row in range(size):
        for col in range(size):
            line_edit = QLineEdit()
            line_edit.setFixedSize(40, 40)  # Ustalony rozmiar pól
            matrix_layout.addWidget(line_edit, row, col)