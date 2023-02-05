from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLineEdit

from calculator.validators import PromptValidator


class Calculator:
    def __init__(self, width: int, height: int) -> None:
        self.pyqt_app = QApplication([])

        self.main_window = QMainWindow()
        self.main_window.setFixedWidth(width)
        self.main_window.setFixedHeight(height)
        self.main_window_geometry = self.main_window.geometry()
        self.font_size = round((self.main_window_geometry.height() * 0.05) + (self.main_window_geometry.width() * 0.02) / 2)
        self.main_window.show()

        self.numbers_grid: QWidget = None
        self.numbers_grid_buttons = None
        self.prompt_window: QLineEdit = None

        self.create_buttons_grid()
        self.create_prompt_window()

    def handle_number_grid_click(self, checked: bool):
        sender: QPushButton = self.numbers_grid.sender()
        value = sender.text()
        self.prompt_window.insert(value)

    def create_prompt_window(self):
        self.prompt_window = QLineEdit(self.main_window)
        self.prompt_window.show()
        self.prompt_window.setValidator(PromptValidator)
        numbers_grid_geometry = self.numbers_grid.geometry()

        prompt_width = numbers_grid_geometry.width()
        prompt_height = round(self.main_window_geometry.height() * 0.1)

        prompt_pos_x = numbers_grid_geometry.x()
        prompt_pos_y = numbers_grid_geometry.y() - 5 - prompt_height
        self.prompt_window.setGeometry(prompt_pos_x, prompt_pos_y, prompt_width, prompt_height)
        self.prompt_window.setStyleSheet(f"""
            border: 1px solid black;
            padding: 0px 10px;
            border-radius: 5%;
            font-size: {self.font_size}px
        """)
        self.prompt_window.setMaxLength(8)

    def create_buttons_grid(self):
        self.numbers_grid = QWidget(self.main_window)
        self.numbers_grid.show()

        button_width = round(self.main_window_geometry.width() * 0.13)
        button_height = round(self.main_window_geometry.height() * 0.12)
        grid_pos_x = round(self.main_window_geometry.width() * 0.10)
        grid_pos_y = round(self.main_window_geometry.height() * 0.35)
        self.numbers_grid.setGeometry(grid_pos_x, grid_pos_y, button_width * 3, button_height * 4)
        self.numbers_grid.setStyleSheet(f"font-size: {self.font_size}px")

        self.numbers_grid_buttons = [
            [
                QPushButton("1"),
                QPushButton("2"),
                QPushButton("3")
            ],
            [
                QPushButton("4"),
                QPushButton("5"),
                QPushButton("6")
            ],
            [
                QPushButton("7"),
                QPushButton("8"),
                QPushButton("9")
            ],
            QPushButton("0")
        ]

        for row, columns_list in enumerate(self.numbers_grid_buttons):
            if not isinstance(columns_list, list):
                button = columns_list
                button.setParent(self.numbers_grid)
                button.setGeometry(1, 3 * button_height, 3 * button_width, 1 * button_height)
                button.show()
                button.clicked.connect(self.handle_number_grid_click)
                continue

            for column, button in enumerate(columns_list):
                button.setParent(self.numbers_grid)
                button.setGeometry(column * button_width, row * button_height, button_width, button_height)
                button.show()
                button.clicked.connect(self.handle_number_grid_click)

    def start(self) -> None:
        self.pyqt_app.exec()


if __name__ == '__main__':
    calc = Calculator(800, 500)
    calc.start()
