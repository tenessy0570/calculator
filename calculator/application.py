from typing import Callable

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLineEdit, QLabel

from calculator.handlers import Handleable
from calculator.validators import PromptValidator
from calculator.widgets import MainWindow, CalculatorWindow


class Calculator(Handleable):
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

        self.main_window = MainWindow(width, height)

        self.digits_grid: QWidget = None
        self.digits_grid_buttons = [
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
        self.prompt_window: QLineEdit = None
        self.operation_window: QLabel = None

        self.operands_grid: QWidget = None
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
        self.left_digit_value = None
        self.right_digit_value = None
        self.previous_right_digit_value = None
        self.current_operand = None
        self.previous_operand = None
        self.operation_result = None
        self.execute_button: QPushButton = None

        self.calculator_window: CalculatorWindow = None

        # Relative to calculator window (coefficient)
        # ----------------------------------------------------------
        self.prompt_window_height = 0.2

        self.digits_grid_height = 1 - self.prompt_window_height
        self.digits_grid_width = 0.6

        self.operands_grid_width = 1 - self.digits_grid_width
        self.operands_grid_height = 1 - self.prompt_window_height
        # ----------------------------------------------------------

        self.execute_button_width = None
        self.execute_button_height = None
        self.digit_button_width = None
        self.digit_button_height = None
        self.operand_button_width = None
        self.operand_button_height = None
        self.create_calculator()

    def create_calculator(self):
        self.calculator_window = CalculatorWindow(self.main_window)

        self.create_digits_grid()
        self.create_operands_grid()
        self.create_execute_button()
        self.create_prompt_window()

    @staticmethod
    def handle_button(btn: QPushButton, parent: QWidget, click_handler: Callable):
        btn.setParent(parent)
        btn.show()
        btn.clicked.connect(click_handler)

    def create_digits_grid(self):
        self.digits_grid = QWidget(self.calculator_window)
        self.digits_grid.show()

        self.digit_button_width = round(self.calculator_window.width() * (self.digits_grid_width / 3))
        self.digit_button_height = round(self.calculator_window.height() * (self.digits_grid_height / 5))
        grid_pos_x = 0
        grid_pos_y = round(self.calculator_window.height() - 5 * self.digit_button_height)

        self.digits_grid.setGeometry(
            grid_pos_x,
            grid_pos_y,
            self.digit_button_width * 3,
            self.digit_button_height * 4
        )

        for row, columns_list in enumerate(self.digits_grid_buttons):
            if isinstance(columns_list, QPushButton):
                button = columns_list
                self.handle_button(button, self.digits_grid, self.handle_digit_grid_click)
                button.setGeometry(
                    0,
                    3 * self.digit_button_height,
                    3 * self.digit_button_width,
                    1 * self.digit_button_height
                )
                continue

            for column, button in enumerate(columns_list):
                self.handle_button(button, self.digits_grid, self.handle_digit_grid_click)
                button.setGeometry(
                    column * self.digit_button_width,
                    row * self.digit_button_height,
                    self.digit_button_width,
                    self.digit_button_height
                )

    def create_operands_grid(self):
        self.operands_grid = QWidget(self.calculator_window)
        self.operands_grid.show()

        self.operand_button_width = round(self.calculator_window.width() * (self.operands_grid_width / 2))
        self.operand_button_height = round(self.calculator_window.height() * (self.operands_grid_height / 5))
        grid_pos_x = round(self.calculator_window.width() - (self.operand_button_width * 2))
        grid_pos_y = self.calculator_window.height() - 5 * self.operand_button_height

        self.operands_grid.setGeometry(
            grid_pos_x,
            grid_pos_y,
            self.operand_button_width * 2,
            self.operand_button_height * 4
        )
        self.operands_grid.setStyleSheet(f"font-size: {self.main_window.font_size}px")

        for row, columns_list in enumerate(self.operands_grid_buttons):
            if isinstance(columns_list, QPushButton):
                button = columns_list
                self.handle_button(button, self.operands_grid, self.handle_operands_grid_click)
                button.setGeometry(
                    0,
                    3 * self.operand_button_height,
                    2 * self.operand_button_width,
                    1 * self.operand_button_height
                )
                continue

            for column, button in enumerate(columns_list):
                self.handle_button(button, self.operands_grid, self.handle_operands_grid_click)
                button.setGeometry(
                    column * self.operand_button_width,
                    row * self.operand_button_height,
                    self.operand_button_width,
                    self.operand_button_height
                )

    def create_execute_button(self):
        self.execute_button = QPushButton("=")
        self.execute_button.setParent(self.calculator_window)
        self.execute_button.show()
        self.execute_button.setStyleSheet(f"font-size: {round(self.main_window.font_size * 1.2)}px")

        coord_x = 0
        coord_y = self.calculator_window.height() - self.digit_button_height
        exec_btn_width = self.calculator_window.width()
        exec_btn_height = self.digit_button_height

        self.execute_button.setGeometry(coord_x, coord_y, exec_btn_width, exec_btn_height)
        self.execute_button.clicked.connect(self.handle_execute_button_click)

    def create_prompt_window(self):
        self.prompt_window = QLineEdit(self.calculator_window)
        self.prompt_window.show()
        self.prompt_window.setValidator(PromptValidator)

        prompt_width = self.calculator_window.width()
        prompt_height = round(self.prompt_window_height * self.calculator_window.height())

        prompt_pos_x = 0
        prompt_pos_y = 0

        self.prompt_window.setGeometry(prompt_pos_x, prompt_pos_y, prompt_width, prompt_height)
        self.prompt_window.setStyleSheet(f"""
            padding: 0px 10px;
            border-radius: 5%;
            font-size: {self.main_window.font_size}px
        """)
        self.prompt_window.setMaxLength(8)

        self.create_operation_window()

    def create_operation_window(self):
        self.operation_window = QLabel(self.prompt_window)
        self.operation_window.show()
        self.operation_window.setStyleSheet(f"""
            font-size: {round(self.main_window.font_size * 0.5)}px;
            background-color: lightgrey
        """)

        width = round(self.prompt_window.geometry().width() * 0.55)
        height = round(self.prompt_window.geometry().height() * 0.7)
        coord_x = self.prompt_window.geometry().width() - width - 5
        coord_y = round(self.prompt_window.geometry().height() * 0.1)
        self.operation_window.setGeometry(coord_x, coord_y, width, height)

    def execute_operation(self):
        try:
            self.operation_result: float | int = round(getattr(
                self.left_digit_value,
                self.math_method_by_symbol[self.current_operand]
            )(self.right_digit_value), 3)
        except ZeroDivisionError:
            self.operation_result = 0

        if isinstance(self.operation_result, int):
            pass
        elif isinstance(self.operation_result, float) and self.operation_result.is_integer():
            self.operation_result = int(self.operation_result)

    def clear_all(self):
        self.current_operand = None
        self.left_digit_value = None
        self.right_digit_value = None
        self.operation_result = None
        self.previous_right_digit_value = None
        self.previous_operand = None
        self.prompt_window.clear()
        self.operation_window.clear()

    def start(self) -> None:
        self.pyqt_app.exec()


if __name__ == '__main__':
    calc = Calculator(1024, 612)
    calc.start()
