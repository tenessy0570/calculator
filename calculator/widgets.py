from PyQt6.QtWidgets import QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self, width: int, height: int, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Custom calculator by tenessy0570")
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.font_size = round(
            (self.geometry().height() * 0.05) + (self.geometry().width() * 0.02) / 2
        )
        self.setStyleSheet(f"font-size: {self.font_size}px")
        self.show()


class OperandsGrid(QWidget):
    def __init__(self, main_window: MainWindow, *args, **kwargs):
        super(OperandsGrid, self).__init__(main_window, *args, **kwargs)
        self.show()
        self.buttons = []

        self.button_width = round(main_window.geometry().width() * 0.11)
        self.button_height = round(main_window.geometry().height() * 0.14)

        pos_x = round(main_window.geometry().x() + self.geometry().width()) + 5
        pos_y = main_window.geometry().y()

        self.setGeometry(pos_x, pos_y, self.button_width * 2, self.button_height * 4)
        self.setStyleSheet(f"font-size: {main_window.font_size}px")
