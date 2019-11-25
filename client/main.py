import sys
from PyQt5.QtWidgets import QApplication
from classes.ui.MainWindow import MainWindow
from classes.client import Client


if __name__ == "__main__":
    client = Client.get_instance()
    print(client)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())