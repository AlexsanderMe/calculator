from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QShortcut, QGridLayout, QLineEdit, QPushButton, QApplication
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtCore import Qt
from app.ui import setup_ui
from app.utils import evaluate_expression, add_implicit_multiplication


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowOpacity(0.92)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.7); color: #fff;")
        self.app = QApplication.instance()
        self.app.focusWindowChanged.connect(self.handle_focus_changed)

        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)

        # Setup UI elements
        self.display, self.buttons = setup_ui(grid, self)

        # Cria uma ação para o atalho Ctrl+V
        paste_shortcut = QShortcut(QKeySequence(QKeySequence.Paste), self)
        paste_shortcut.activated.connect(self.on_paste)

        self.setWindowTitle('Calculadora')
        self.resize(515, 365)

    def handle_focus_changed(self, activated):
        if activated:
            self.setStyleSheet("background-color: rgba(0, 0, 0, 0.7); color: #fff;")
            self.setWindowOpacity(0.92)
        else:
            self.setStyleSheet("background-color: rgba(0, 0, 0, 0.7); color: #444;")
            self.setWindowOpacity(0.65)

    def on_paste(self):
        clipboard = QApplication.clipboard()
        pasted_text = clipboard.text().replace('\n', '').replace(',', '.')
        self.add_to_display(pasted_text)

    def resizeEvent(self, event):
        font_size = self.height() / 10
        font = QFont("Arial", int(font_size))
        self.display.setFont(font)

        font_size = self.height() / 15
        font_buttons = QFont("Arial", int(font_size))
        for button in self.buttons:
            button.setFont(font_buttons)

    def keyPressEvent(self, event):
        key = event.text()
        if event.key() == 16777216:
            self.display.setText('')
        if key in '0123456789.+-*/()x=%':
            self.add_to_display(key)
        elif key == '\r':
            self.calculate_result()
        elif event.key() == Qt.Key_Backspace:
            text = self.display.text()[:-1]
            self.display.setText(text)

    def add_to_display(self, button_text=None):
        try:
            if not button_text:
                button_text = self.sender().text()
            if button_text == '←':
                text = self.display.text()[:-1]
                self.display.setText(text)
                return
            if button_text == '＝':
                button_text = '='
            display_text = self.display.text()
            self.display.setText(display_text + button_text)
        except AttributeError:
            pass

    def calculate_result(self):
        display_text = self.display.text()
        try:
            result = evaluate_expression(display_text)
            self.display.setText(str(result))
        except Exception as e:
            # Se não fizer o uso correto da equação com X, o usuário pode ter confundido com o *
            try:
                if 'x' in display_text:
                    display_text = display_text.replace('x', '*')
                    result = eval(display_text)
                    self.display.setText(str(result))
            except Exception as e:
                self.display.setText("Erro")

    def clear_display(self):
        self.display.clear()
