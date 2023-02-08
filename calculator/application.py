import os
import sys

# https://stackoverflow.com/questions/38276027/import-statement-is-not-working-when-running-python-script-from-the-command-line

path = os.getcwd()
sys.path.append(path)

from typing import Callable

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel

from calculator.handlers import Handleable
from calculator.validators import PromptValidator
from calculator.mixins import HasMathQButtonsMixin
from calculator.widgets import MainWindow, CalculatorWindow


class Calculator(Handleable, HasMathQButtonsMixin):
    def __init__(self, width: int, height: int, *args, **kwargs) -> None:
        self.pyqt_app = QApplication([])

        super(Calculator, self).__init__(*args, **kwargs)

        self.main_window = MainWindow(width, height)

        # Relative to calculator window (coefficient)
        # ----------------------------------------------------------
        self.prompt_window_height = 0.2

        self.digits_grid_height = 1 - self.prompt_window_height
        self.digits_grid_width = 0.6

        self.operands_grid_width = 1 - self.digits_grid_width
        self.operands_grid_height = 1 - self.prompt_window_height
        # ----------------------------------------------------------

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
