from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow


class Calculator:
    def __init__(self) -> None:
        self.pyqt_app = QApplication([])

        self.main_window = QMainWindow()
        self.main_window.setFixedWidth(1024)
        self.main_window.setFixedHeight(602)
        self.main_window.show()

        self.numbers_window = None
        self.numbers_window_buttons = None

        self.create_buttons_grid()

    def tests_method(self):
        print("Clicked!")

    def create_buttons_grid(self):
        self.numbers_window = QWidget(self.main_window)
        self.numbers_window.show()

        button_width = 120
        button_height = 75
        grid_pos_x = 150
        grid_pos_y = 200
        self.numbers_window.setGeometry(grid_pos_x, grid_pos_y, button_width * 3, button_height * 3)

        self.numbers_window_buttons = [
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
        ]

        for row, columns_list in enumerate(self.numbers_window_buttons):
            for column, button in enumerate(columns_list):
                button.setParent(self.numbers_window)
                button.setGeometry(column * button_width, row * button_height, button_width, button_height)
                button.setCheckable(True)
                button.show()
                button.clicked.connect(self.tests_method)

    def start(self) -> None:
        self.pyqt_app.exec()


if __name__ == '__main__':
    calc = Calculator()
    calc.start()
