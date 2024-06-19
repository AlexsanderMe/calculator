from PyQt5.QtWidgets import QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

def setup_ui(grid, parent):
    display = QLineEdit()
    display.setReadOnly(True)
    display.setAlignment(Qt.AlignRight)
    display.setFont(QFont("Arial", 24))
    grid.addWidget(display, 0, 0, 1, 4)

    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '(', '0', ')', '+',
        '＝', '.', '%', '←',
        'C', '**', 'x', '='
    ]

    positions = [(i, j) for i in range(1, 7) for j in range(4)]

    button_widgets = []

    for position, button in zip(positions, buttons):
        btn = QPushButton(button)
        btn.setStyleSheet("QPushButton{font-weight: bold; color: #fff; background-color: #333; border-radius: 5px;} :hover {background-color: #222;}")
        if button in '0123456789.+-*/()**x%←＝':
            btn.clicked.connect(parent.add_to_display)
        elif button == '=':
            btn.setStyleSheet("QPushButton{background-color: #00f; border-radius: 5px;} :hover {background-color: #0000b3;}")
            btn.clicked.connect(parent.calculate_result)
        elif button == 'C':
            btn.setStyleSheet("QPushButton{background-color: #f00; border-radius: 5px;} :hover {background-color: #b30000;}")
            btn.clicked.connect(parent.clear_display)
        grid.addWidget(btn, *position)
        button_widgets.append(btn)

    return display, button_widgets
