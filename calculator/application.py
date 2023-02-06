from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLineEdit, QLabel

from calculator.validators import PromptValidator


class Calculator:
    def __init__(self, width: int, height: int) -> None:
        self.pyqt_app = QApplication([])

        self.math_multiple = "*"
        self.math_division = "/"
        self.math_add = "+"
        self.math_sub = "-"
        self.math_pow = "**"
        self.math_mod = "%"
        self.math_floordiv = "//"
        self.clear_button_text = "C"

        self.math_method_by_symbol = {
            self.math_multiple: "__mul__",
            self.math_division: "__truediv__",
            self.math_add: "__add__",
            self.math_sub: "__sub__",
            self.math_pow: "__pow__",
            self.math_mod: "__mod__",
            self.math_floordiv: "__floordiv__",
        }

        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("Custom calculator by tenessy0570")
        self.main_window.setFixedWidth(width)
        self.main_window.setFixedHeight(height)
        self.main_window_geometry = self.main_window.geometry()
        self.font_size = round(
            (self.main_window_geometry.height() * 0.05) + (self.main_window_geometry.width() * 0.02) / 2
        )
        self.main_window.show()

        self.numbers_grid: QWidget = None
        self.numbers_grid_buttons = None
        self.prompt_window: QLineEdit = None
        self.operation_window: QLabel = None
        self.operands_grid: QWidget = None
        self.operands_grid_buttons: list = None
        self.left_number_value = None
        self.right_number_value = None
        self.current_operand = None
        self.operation_result = None

        self.create_digits_grid()
        self.create_operands_grid()
        self.create_prompt_window()

    def handle_number_grid_click(self, checked: bool):
        sender: QPushButton = self.numbers_grid.sender()
        value = sender.text()
        self.prompt_window.insert(value)

    def handle_operands_grid_click(self, checked: bool):
        sender: QPushButton = self.operands_grid.sender()

        if sender.text() == self.clear_button_text:
            self.current_operand = None
            self.left_number_value = None
            self.right_number_value = None
            self.operation_result = None
            self.prompt_window.clear()
            self.operation_window.clear()
            return None

        if not self.prompt_window.text() and not self.left_number_value:
            return None

        if self.left_number_value and self.current_operand:
            self.right_number_value = int(self.prompt_window.text())

            self.operation_result: float | int = round(getattr(
                self.left_number_value,
                self.math_method_by_symbol[self.current_operand]
            )(self.right_number_value), 3)

            if self.operation_result.is_integer():
                self.operation_result = int(self.operation_result)

            self.operation_window.setText(
                f"{self.left_number_value} {self.current_operand} {self.right_number_value} = {self.operation_result}"
            )
            return None

        if self.left_number_value is not None:
            self.current_operand = sender.text()
            self.operation_window.setText(f"{self.left_number_value} {self.current_operand}")
            return None

        self.left_number_value = int(self.prompt_window.text())
        self.current_operand = sender.text()
        self.operation_window.setText(f"{self.left_number_value} {self.current_operand}")
        self.prompt_window.setText("")

    def create_operands_grid(self):
        self.operands_grid = QWidget(self.main_window)
        self.operands_grid.show()

        button_width = round(self.main_window_geometry.width() * 0.13)
        button_height = round(self.main_window_geometry.height() * 0.12)
        grid_pos_x = round(self.numbers_grid.geometry().x() + self.numbers_grid.geometry().width()) + 5
        grid_pos_y = self.numbers_grid.geometry().y()

        self.operands_grid.setGeometry(grid_pos_x, grid_pos_y, button_width * 2, button_height * 4)
        self.operands_grid.setStyleSheet(f"font-size: {self.font_size}px")

        self.operands_grid_buttons = [
            [
                QPushButton(self.math_add),
                QPushButton(self.math_sub)
            ],
            [
                QPushButton(self.math_division),
                QPushButton(self.math_multiple)
            ],
            [
                QPushButton(self.math_pow),
                QPushButton(self.math_mod),
            ],
            [
                QPushButton(self.math_floordiv),
                QPushButton(self.clear_button_text)
            ]
        ]

        def handle_button(btn):
            btn.setParent(self.operands_grid)
            btn.show()
            btn.clicked.connect(self.handle_operands_grid_click)

        for row, columns_list in enumerate(self.operands_grid_buttons):
            if isinstance(columns_list, QPushButton):
                button = columns_list
                handle_button(button)
                button.setGeometry(0, 3 * button_height, 2 * button_width, 1 * button_height)
                continue

            for column, button in enumerate(columns_list):
                handle_button(button)
                button.setGeometry(column * button_width, row * button_height, button_width, button_height)

    def create_prompt_window(self):
        self.prompt_window = QLineEdit(self.main_window)
        self.prompt_window.show()
        self.prompt_window.setValidator(PromptValidator)
        numbers_grid_geometry = self.numbers_grid.geometry()

        prompt_width = numbers_grid_geometry.width() + self.operands_grid.geometry().width() + 5
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

        self.operation_window = QLabel(self.prompt_window)
        self.operation_window.show()
        self.operation_window.setStyleSheet(f"border: 1px solid black; font-size: {round(self.font_size * 0.5)}px")

        width = round(self.prompt_window.geometry().width() * 0.55)
        height = round(self.prompt_window.geometry().height() * 0.7)
        coord_x = self.prompt_window.geometry().width() - width - 5
        coord_y = round(self.prompt_window.geometry().height() * 0.1)
        self.operation_window.setGeometry(coord_x, coord_y, width, height)

    def create_digits_grid(self):
        self.numbers_grid = QWidget(self.main_window)
        self.numbers_grid.show()

        button_width = round(self.main_window_geometry.width() * 0.13)
        button_height = round(self.main_window_geometry.height() * 0.12)
        grid_pos_x = round(self.main_window_geometry.width() * 0.28 - button_width)
        grid_pos_y = round(self.main_window_geometry.height() * 0.42 - button_height)
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

        def handle_button(btn):
            btn.setParent(self.numbers_grid)
            btn.show()
            btn.clicked.connect(self.handle_number_grid_click)

        for row, columns_list in enumerate(self.numbers_grid_buttons):
            if isinstance(columns_list, QPushButton):
                button = columns_list
                handle_button(button)
                button.setGeometry(0, 3 * button_height, 3 * button_width, 1 * button_height)
                continue

            for column, button in enumerate(columns_list):
                handle_button(button)
                button.setGeometry(column * button_width, row * button_height, button_width, button_height)

    def start(self) -> None:
        self.pyqt_app.exec()


if __name__ == '__main__':
    calc = Calculator(1024, 512)
    calc.start()
