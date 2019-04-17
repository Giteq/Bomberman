from PyQt5.QtWidgets import QMainWindow , QDesktopWidget


class MyQMainWindow(QMainWindow):
    """
    Class with useful PyQT functions for QMainWindow class.
    """
    def __init__(self):
        super(QMainWindow, self).__init__()

    def center_window_pos(self):
        """
        Function sets this window position to center of the screen.
        :return:
        """
        resolution = QDesktopWidget().screenGeometry()
        self.move(resolution.width() / 2, resolution.height() / 2)

