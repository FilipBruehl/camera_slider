from PyQt5.QtWidgets import QMainWindow
from classes.ui.designer.main_window import Ui_MainWindow
from classes.ui.ConnectServer import ConnectServer
from classes.ui.ConnectCamera import ConnectCamera
from classes.Observer import Observer, Subject
from classes.client import Client
from classes.DataContainer import DataContainer


class MainWindow(QMainWindow, Observer):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionConnect.triggered.connect(self.connect_server)
        self.ui.actionDisconnect.triggered.connect(self.disconnect_server)
        self.ui.actionConnectCamera.triggered.connect(self.connect_camera)
        self.ui.menuSchliessen.triggered.connect(self.close)
        self.client = Client.get_instance()
        DataContainer.get_instance().attach(self)
        print(self.client)

    def connect_server(self):
        if self.client.connect(ConnectServer.get_ip()):
            self.ui.label_info_server_ip.setText(self.client.host_ip)
            self.ui.label_info_server_ip.setStyleSheet("color: green; border: none;")
            self.ui.label_info_server_ip.update()
            self.ui.actionConnect.setDisabled(True)
            self.ui.actionDisconnect.setEnabled(True)
            self.ui.actionConnectCamera.setEnabled(True)
        else:
            self.ui.label_info_server_ip.setText("Verbinden fehlgeschlagen")
        
    def disconnect_server(self):
        self.client.disconnect()
        self.ui.label_info_server_ip.setText("Nicht verbunden")
        self.ui.label_info_server_ip.setStyleSheet("color: #DB2828; border: none;")
        self.ui.label_info_server_ip.update()
        self.ui.actionConnect.setEnabled(True)
        self.ui.actionDisconnect.setDisabled(True)

    def connect_camera(self):
        self.client.get_cameras()
        index, camera = ConnectCamera.get_camera()
        print(index, camera)
        self.client.send("set camera", index)
        if camera:
            self.ui.label_info_camera_name.setText(camera)
            self.ui.label_info_camera_name.setStyleSheet("color: green; border: none;")
            self.ui.label_info_camera_name.update()
            self.ui.actionConnectCamera.setDisabled(True)
        else:
            self.ui.label_info_camera_name.setText("Nicht verbunden")

    def update(self, subject: Subject) -> None:
        print("Inside update in MainWindow")