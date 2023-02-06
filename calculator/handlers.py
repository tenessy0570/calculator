from PyQt6.QtWidgets import QPushButton


class Handleable:
    def handle_digit_grid_click(self):
        sender: QPushButton = self.digits_grid.sender()
        value = sender.text()
        self.prompt_window.insert(value)

    def handle_execute_button_click(self):
        if any((
                self.left_digit_value is None,
                self.current_operand is None,
                not self.prompt_window.text()
        )):
            return None

        self.right_digit_value = int(self.prompt_window.text())
        self.execute_operation()
        self.operation_window.setText(str(self.operation_result))
        self.prompt_window.clear()

        self.left_digit_value = None
        self.right_digit_value = None
        self.current_operand = None

    def handle_operands_grid_click(self):
        sender: QPushButton = self.operands_grid.sender()

        if sender.text() == self.clear_button_text:
            self.clear_all()
            return None

        if all((
                self.operation_result is None,
                all((
                        self.left_digit_value is None,
                        not self.prompt_window.text()
                ))
        )):
            return None

        if all((
                not self.prompt_window.text(),
                self.left_digit_value is None,
                self.right_digit_value is None,
                self.operation_result is not None
        )):
            self.left_digit_value = self.operation_result
            self.operation_result = None
            self.current_operand = sender.text()
            self.operation_window.setText(f"{self.left_digit_value} {self.current_operand}")
            return None

        if all((
                self.left_digit_value,
                self.current_operand,
                self.prompt_window.text()
        )):
            self.right_digit_value = int(self.prompt_window.text())

            self.execute_operation()

            self.operation_window.setText(str(self.operation_result))
            self.left_digit_value = self.operation_result
            self.right_digit_value = None
            self.operation_result = None
            self.current_operand = sender.text()
            self.operation_window.setText(f"{self.left_digit_value} {self.current_operand}")
            self.prompt_window.clear()
            return None

        if self.left_digit_value is not None:
            self.current_operand = sender.text()
            self.operation_window.setText(f"{self.left_digit_value} {self.current_operand}")
            return None

        self.left_digit_value = int(self.prompt_window.text())
        self.current_operand = sender.text()
        self.operation_window.setText(f"{self.left_digit_value} {self.current_operand}")
        self.prompt_window.setText("")
