from PyQt5.QtWidgets import QMainWindow
from classes.ui.designer.main_window import Ui_MainWindow
from classes.ui.ConnectServer import ConnectServer
from classes.client import Client

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionConnect.triggered.connect(self.connect_server)
        self.ui.actionDisconnect.triggered.connect(self.disconnect_server)
        self.client = Client()

    def connect_server(self):
        if self.client.connect(ConnectServer.get_ip()):
            self.ui.label_info_server_ip.setText(self.client.host_ip)
            self.ui.label_info_server_ip.setStyleSheet("color: green; border: none;")
            self.ui.label_info_server_ip.update()
            self.ui.actionConnect.setDisabled(True)
            self.ui.actionDisconnect.setEnabled(True)
        else:
            self.ui.label_info_server_ip.setText("Verbinden fehlgeschlagen")
        
    def disconnect_server(self):
        self.client.disconnect()
        self.ui.label_info_server_ip.setText("Nicht verbunden")
        self.ui.label_info_server_ip.setStyleSheet("color: #DB2828; border: none;")
        self.ui.label_info_server_ip.update()
        self.ui.actionConnect.setEnabled(True)
        self.ui.actionDisconnect.setDisabled(True)
    