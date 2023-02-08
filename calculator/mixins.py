from PyQt6.QtWidgets import QPushButton, QLineEdit, QWidget, QLabel

from calculator.widgets import CalculatorWindow


class ContainsQWidgetWindowsMixin:
    def __init__(self, *args, **kwargs):
        self.prompt_window = QLineEdit()
        self.digits_grid = QWidget()
        self.operation_window = QLabel()
        self.operands_grid = QWidget()
        self.execute_button = QPushButton()
        self.calculator_window: CalculatorWindow = None
        self.prompt_window = QLineEdit()


class ContainsMathMethodsMixin:
    def __init__(self, *args, **kwargs):
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


class CalculableMixin(ContainsMathMethodsMixin):
    def __init__(self, *args, **kwargs):
        super(CalculableMixin, self).__init__(*args, **kwargs)

        self.operation_result = None
        self.previous_operand = None
        self.current_operand = None
        self.left_digit_value = None
        self.right_digit_value = None
        self.previous_right_digit_value = None

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

        if len(str(int(self.operation_result))) > 8:
            self.operation_result = "ERR"


class HasMathQButtonsMixin(ContainsMathMethodsMixin):
    def __init__(self, *args, **kwargs):
        super(HasMathQButtonsMixin, self).__init__(*args, **kwargs)

        self.execute_button_width = None
        self.execute_button_height = None
        self.digit_button_width = None
        self.digit_button_height = None
        self.operand_button_width = None
        self.operand_button_height = None

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
