from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit


def create_matrix(matrix_layout, size):

    while matrix_layout.count():
        item = matrix_layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()

    print(f"Matrix size: {size}")

    for row in range(size):
        for col in range(size):
            line_edit = QLineEdit()
            line_edit.setFixedSize(40, 30)  # Adjust size as needed
            line_edit.setText("0")  # Default value
            line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            line_edit.setStyleSheet("background-color: #EDEDED; color: black; border: 1px solid gray; border-radius: 5px; font-size: 16px")
            matrix_layout.addWidget(line_edit, row, col)
            print(f"Adding widget at position: ({row}, {col})")