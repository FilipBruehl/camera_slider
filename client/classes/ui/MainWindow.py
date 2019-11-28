from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from time import sleep
from classes.ui.designer.main_window import Ui_MainWindow
from classes.ui.ConnectCamera import ConnectCamera
from classes.Observer import Observer, Subject
from classes.DataContainer import DataContainer


# View Teil des MVC Pattern
class MainWindow(QMainWindow, Observer):
    connect_server_signal = pyqtSignal()
    disconnect_server_signal = pyqtSignal()
    connect_camera_signal = pyqtSignal()
    close_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionConnect.triggered.connect(self.connect_server_signal)
        self.ui.actionDisconnect.triggered.connect(self.disconnect_server_signal)
        self.ui.actionConnectCamera.triggered.connect(self.connect_camera_signal)
        self.ui.menuSchliessen.triggered.connect(self.close_signal)
        DataContainer.get_instance().attach(self)

    def set_connected(self, ip):
        self.ui.label_info_server_ip.setText(ip)
        self.ui.label_info_server_ip.setStyleSheet("color: green; border: none;")
        self.ui.label_info_server_ip.update()
        self.ui.actionConnect.setDisabled(True)
        self.ui.actionDisconnect.setEnabled(True)
        self.ui.actionConnectCamera.setEnabled(True)

    def set_connection_failed(self):
        self.ui.label_info_server_ip.setText("Verbinden fehlgeschlagen")

    def set_not_connected(self):
        self.ui.label_info_server_ip.setText("Nicht verbunden")
        self.ui.label_info_server_ip.setStyleSheet("color: #DB2828; border: none;")
        self.ui.label_info_server_ip.update()
        self.ui.actionConnect.setEnabled(True)
        self.ui.actionDisconnect.setDisabled(True)

        self.ui.actionConnectCamera.setEnabled(True)
        self.ui.input_info_camera_name.setText("Nicht verbunden")
        self.ui.input_info_camera_name.setStyleSheet("color: #DB2828; border: none;")
        self.ui.input_info_camera_name.update()

        self.ui.label_info_camera_akku.setDisabled(True)
        self.ui.input_info_camera_akku.setDisabled(True)
        self.ui.input_info_camera_akku.setText("")

        self.ui.label_info_camera_blende.setDisabled(True)
        self.ui.input_info_camera_blende.setDisabled(True)
        self.ui.input_info_camera_blende.setText("")

        self.ui.label_info_camera_shutter.setDisabled(True)
        self.ui.input_info_camera_shutter.setDisabled(True)
        self.ui.input_info_camera_shutter.setText("")

        self.ui.label_info_camera_iso.setDisabled(True)
        self.ui.input_info_camera_iso.setDisabled(True)
        self.ui.input_info_camera_iso.setText("")

        self.ui.label_info_camera_fokus.setDisabled(True)
        self.ui.input_info_camera_fokus.setDisabled(True)
        self.ui.input_info_camera_fokus.setText("")

        self.ui.label_info_camera_format.setDisabled(True)
        self.ui.input_info_camera_format.setDisabled(True)
        self.ui.input_info_camera_format.setText("")

    # def connect_camera(self):
    #     index, camera = ConnectCamera.get_camera()
    #     print(index, camera)
    #     self.client.send_msg("set camera", index)
    #     if camera:
    #         self.ui.label_info_camera_name.setText(camera)
    #         self.ui.label_info_camera_name.setStyleSheet("color: green; border: none;")
    #         self.ui.label_info_camera_name.update()
    #         self.ui.actionConnectCamera.setDisabled(True)
    #     else:
    #         self.ui.label_info_camera_name.setText("Nicht verbunden")

    def set_camera_connected(self, camera_info):
        self.ui.actionConnectCamera.setDisabled(True)
        self.ui.input_info_camera_name.setText(camera_info['name'])
        self.ui.input_info_camera_name.setStyleSheet("color: green; border: none;")
        self.ui.input_info_camera_name.update()

        self.ui.label_info_camera_akku.setEnabled(True)
        self.ui.input_info_camera_akku.setEnabled(True)
        self.ui.input_info_camera_akku.setText(camera_info['battery'])

        self.ui.label_info_camera_blende.setEnabled(True)
        self.ui.input_info_camera_blende.setEnabled(True)
        self.ui.input_info_camera_blende.setText(camera_info['focal'])

        self.ui.label_info_camera_shutter.setEnabled(True)
        self.ui.input_info_camera_shutter.setEnabled(True)
        self.ui.input_info_camera_shutter.setText(camera_info['shutter'])

        self.ui.label_info_camera_iso.setEnabled(True)
        self.ui.input_info_camera_iso.setEnabled(True)
        self.ui.input_info_camera_iso.setText(camera_info['iso'])

        self.ui.label_info_camera_fokus.setEnabled(True)
        self.ui.input_info_camera_fokus.setEnabled(True)
        self.ui.input_info_camera_fokus.setText(camera_info['focus'])

        self.ui.label_info_camera_format.setEnabled(True)
        self.ui.input_info_camera_format.setEnabled(True)
        self.ui.input_info_camera_format.setText(camera_info['quality'])

    def set_camera_not_available(self):
        self.ui.label_info_camera_name.setText("Keine Kamera verfügbar")

    def update(self, subject: Subject) -> None:
        print("Inside update in MainWindow")
