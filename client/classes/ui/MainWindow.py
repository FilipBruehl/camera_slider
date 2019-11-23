from PyQt5.QtWidgets import QMainWindow
from classes.ui.designer.main_window import Ui_MainWindow
from classes.ui.ConnectServer import ConnectServer
from classes.client import Client

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionConnect.triggered.connect(self.open_connect_server)
        self.client = Client()

    def open_connect_server(self):
        if self.client.connect(ConnectServer.get_ip()) :
            self.ui.label_info_server_ip.setText(self.client.host_ip)
            self.ui.label_info_server_ip.setStyleSheet("color: green; border: none;")
            self.ui.label_info_server_ip.update()
        else:
            self.ui.label_info_server_ip.setText("Verbinden fehlgeschlagen")
    