from PyQt6.QtWidgets import QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self, width: int, height: int, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Custom calculator by tenessy0570")
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.font_size = round(
            (self.height() * 0.05) + (self.width() * 0.02) / 2
        )
        self.setStyleSheet(f"font-size: {self.font_size}px")
        self.show()


class CalculatorWindow(QWidget):
    def __init__(self, parent_window, *args, **kwargs):
        super(CalculatorWindow, self).__init__(parent_window, *args, **kwargs)
        self.show()

        self.setFixedWidth(round(parent_window.width() * 0.6))
        self.setFixedHeight(round(parent_window.height() * 0.75))

        self.center_widget(self, parent_window)

    @staticmethod
    def center_widget(target: QWidget, parent_widget: QWidget):
        coord_x = round(parent_widget.geometry().width() / 2) - round(target.width() / 2)
        coord_y = round(parent_widget.geometry().height() / 2) - round(target.height() / 2)

        target.setGeometry(coord_x, coord_y, target.width(), target.height())
