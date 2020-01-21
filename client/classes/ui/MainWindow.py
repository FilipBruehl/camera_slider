from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from classes.ui.designer.main_window import Ui_MainWindow
from styles.Styles import MainWindowStyles
from classes.ui.ConnectCamera import ConnectCamera
from classes.DataContainer import DataContainer


# View Teil des MVC Pattern
class MainWindow(QMainWindow):
    connect_server_signal = pyqtSignal()
    disconnect_server_signal = pyqtSignal()
    connect_camera_signal = pyqtSignal()
    disconnect_camera_signal = pyqtSignal()
    connect_motor_signal = pyqtSignal()
    disconnect_motor_signal = pyqtSignal()
    connect_sensors_signal = pyqtSignal()
    disconnect_sensors_signal = pyqtSignal()
    set_slider_settings_singal = pyqtSignal()
    set_kamera_settings_signal = pyqtSignal()
    take_picture_signal = pyqtSignal()
    start_slider_signal = pyqtSignal()
    position_slider_signal = pyqtSignal()
    about_signal = pyqtSignal()
    close_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.groupBox_info.setStyleSheet(MainWindowStyles.main_window_information_style().toString())
        # self.ui.menubar.setStyleSheet(MainWindowStyles.main_window_menu_style().toString())
        # self.ui.groupBox_settings.setStyleSheet(MainWindowStyles.main_window_settings_style().toString())
        self.ui.label_info_server_ip.setObjectName("serverip")
        self.ui.input_info_camera_name.setObjectName("cameraname")
        self.ui.actionConnect.triggered.connect(self.connect_server_signal)
        self.ui.actionDisconnect.triggered.connect(self.disconnect_server_signal)
        self.ui.actionConnectCamera.triggered.connect(self.connect_camera_signal)
        self.ui.actionDisconnectCamera.triggered.connect(self.disconnect_camera_signal)
        self.ui.actionConnectMotor.triggered.connect(self.connect_motor_signal)
        self.ui.actionDisconnectMotor.triggered.connect(self.disconnect_motor_signal)
        self.ui.actionConnectSensors.triggered.connect(self.connect_sensors_signal)
        self.ui.actionDisconnectSensors.triggered.connect(self.disconnect_sensors_signal)
        self.ui.pushButton_settings_slider.clicked.connect(self.set_slider_settings_singal)
        self.ui.pushButton_settings_kamera.clicked.connect(self.set_kamera_settings_signal)
        self.ui.pushButton_steuerung_kamera.clicked.connect(self.take_picture_signal)
        self.ui.pushButton_steuerung_slider.clicked.connect(self.start_slider_signal)
        self.ui.pushButton_steuerung_slider_position.clicked.connect(self.position_slider_signal)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.comboBox_settings_slider_start.currentTextChanged.connect(self.check_slider_settings)
        self.ui.comboBox_settings_slider_richtung.currentTextChanged.connect(self.check_slider_settings)
        self.ui.lineEdit_settings_slider_steps.textChanged.connect(self.check_slider_settings)
        self.ui.lineEdit_settings_slider_frequenz.textChanged.connect(self.check_slider_settings)
        self.ui.lineEdit_settings_kamera_takes.textChanged.connect(self.check_kamera_settings)

    def about(self):
        msg = QMessageBox()
        msg.setWindowTitle("Über Camera Slider")
        msg.setText(
            "<h3>Über Camera Slider</h3><p>Projektarbeit für das Modul CPS der FH Kiel.<br>Erstellt von Filip Hugo Brühl</p>")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def set_connected(self, ip):
        self.ui.groupBox_info_server.setEnabled(True)

        self.ui.label_info_server.setEnabled(True)
        self.ui.label_info_server_ip.setText(ip)
        self.ui.label_info_server_ip.setProperty("connected", True)
        self.ui.label_info_server_ip.style().unpolish(self.ui.label_info_server_ip)
        self.ui.label_info_server_ip.style().polish(self.ui.label_info_server_ip)
        self.ui.label_info_server_ip.update()
        self.ui.actionConnect.setDisabled(True)
        self.ui.actionClose.setDisabled(True)
        self.ui.actionDisconnect.setEnabled(True)
        self.ui.actionConnectCamera.setEnabled(True)
        self.ui.actionConnectMotor.setEnabled(True)
        self.ui.actionConnectSensors.setEnabled(True)

    def set_connection_failed(self):
        self.ui.groupBox_info_server.setEnabled(True)
        self.ui.label_info_server_ip.setText("Verbinden fehlgeschlagen")

    def set_not_connected(self):
        self.ui.label_info_server.setDisabled(True)
        self.ui.label_info_server_ip.setText("Nicht verbunden")
        self.ui.label_info_server_ip.setProperty("connected", False)
        self.ui.label_info_server_ip.style().unpolish(self.ui.label_info_server_ip)
        self.ui.label_info_server_ip.style().polish(self.ui.label_info_server_ip)
        self.ui.label_info_server_ip.update()
        self.ui.actionConnect.setEnabled(True)
        self.ui.actionClose.setEnabled(True)
        self.ui.actionDisconnect.setDisabled(True)

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
        self.ui.actionDisconnectCamera.setEnabled(True)
        self.ui.actionDisconnect.setDisabled(True)
        self.ui.groupBox_info_kamera.setEnabled(True)

        self.ui.label_info_camera_name.setEnabled(True)
        self.ui.input_info_camera_name.setText(camera_info['name'])
        self.ui.input_info_camera_name.setProperty("connected", True)
        self.ui.input_info_camera_name.style().unpolish(self.ui.input_info_camera_name)
        self.ui.input_info_camera_name.style().polish(self.ui.input_info_camera_name)
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

        self.ui.groupBox_settings_kamera.setEnabled(True)
        self.ui.label_settings_kamera_takes.setEnabled(True)
        self.ui.lineEdit_settings_kamera_takes.setEnabled(True)
        self.ui.label_settings_kamera_blende.setEnabled(True)
        self.ui.comboBox_settings_kamera_blende.setEnabled(True)
        self.ui.label_settings_kamera_shutter.setEnabled(True)
        self.ui.comboBox_settings_kamera_shutter.setEnabled(True)
        self.ui.label_settings_kamera_iso.setEnabled(True)

        self.ui.groupBox_steuerung_kamera.setEnabled(True)
        self.ui.pushButton_steuerung_kamera.setEnabled(True)

    def set_camera_options(self, data):
        print(data)
        self.ui.comboBox_settings_kamera_blende.addItems(data['focal'])
        self.ui.comboBox_settings_kamera_shutter.addItems(data['shutter'])
        self.ui.comboBox_settings_kamera_iso.addItems(data['iso'])

        focal_index = self.ui.comboBox_settings_kamera_blende.findText(self.ui.input_info_camera_blende.text())
        if focal_index >= 0:
            self.ui.comboBox_settings_kamera_blende.setCurrentIndex(focal_index)
        shutter_index = self.ui.comboBox_settings_kamera_shutter.findText(self.ui.input_info_camera_shutter.text())
        if shutter_index >= 0:
            self.ui.comboBox_settings_kamera_shutter.setCurrentIndex(shutter_index)
        iso_index = self.ui.comboBox_settings_kamera_iso.findText(self.ui.input_info_camera_iso.text())
        if iso_index >= 0:
            self.ui.comboBox_settings_kamera_iso.setCurrentIndex(iso_index)

    def set_camera_values(self, data):
        self.ui.input_info_camera_akku.setText(data['battery'])
        self.ui.input_info_camera_blende.setText(data['focal'])
        self.ui.input_info_camera_shutter.setText(data['shutter'])
        self.ui.input_info_camera_iso.setText(data['iso'])
        self.ui.input_info_camera_fokus.setText(data['focus'])
        self.ui.input_info_camera_format.setText(data['quality'])


    def set_camera_not_available(self):
        self.ui.input_info_camera_name.setText("Keine Kamera verfügbar")

    def set_camera_disconnected(self):
        self.ui.actionConnectCamera.setEnabled(True)
        self.ui.actionDisconnectCamera.setDisabled(True)
        if not self.ui.actionDisconnectCamera.isEnabled() and not self.ui.actionDisconnectMotor.isEnabled():
            self.ui.actionDisconnect.setEnabled(True)

        self.ui.label_info_camera_name.setDisabled(True)
        self.ui.input_info_camera_name.setText("Nicht verbunden")
        self.ui.input_info_camera_name.setProperty("connected", False)
        self.ui.input_info_camera_name.style().unpolish(self.ui.input_info_camera_name)
        self.ui.input_info_camera_name.style().polish(self.ui.input_info_camera_name)
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

        self.ui.groupBox_settings_kamera.setDisabled(True)
        self.ui.label_settings_kamera_takes.setDisabled(True)
        self.ui.lineEdit_settings_kamera_takes.setDisabled(True)
        self.ui.pushButton_settings_kamera.setDisabled(True)

        self.ui.groupBox_steuerung_kamera.setDisabled(True)
        self.ui.pushButton_steuerung_kamera.setDisabled(True)

    def set_motor_connected(self):
        self.ui.actionConnectMotor.setDisabled(True)
        self.ui.actionDisconnectMotor.setEnabled(True)

        self.ui.groupBox_info_slider.setEnabled(True)
        self.ui.input_info_slider_rechts.setEnabled(True)
        self.ui.input_info_slider_links.setEnabled(True)
        self.ui.input_info_slider_frequenz.setEnabled(True)
        self.ui.input_info_slider_richtung.setEnabled(True)
        self.ui.input_info_slider_status.setEnabled(True)
        self.ui.input_info_slider_steps.setEnabled(True)
        self.ui.label_info_slider_rechts.setEnabled(True)
        self.ui.label_info_slider_links.setEnabled(True)
        self.ui.label_info_slider_frequenz.setEnabled(True)
        self.ui.label_info_slider_richtung.setEnabled(True)
        self.ui.label_info_slider_status.setEnabled(True)
        self.ui.label_info_slider_steps.setEnabled(True)

        self.ui.groupBox_settings_slider.setEnabled(True)
        self.ui.comboBox_settings_slider_richtung.setEnabled(True)
        self.ui.comboBox_settings_slider_start.setEnabled(True)
        self.ui.label_settings_slider_frequenz.setEnabled(True)
        self.ui.label_settings_slider_richtung.setEnabled(True)
        self.ui.label_settings_slider_start.setEnabled(True)
        self.ui.label_settings_slider_steps.setEnabled(True)
        self.ui.lineEdit_settings_slider_frequenz.setEnabled(True)
        self.ui.lineEdit_settings_slider_steps.setEnabled(True)
        self.ui.pushButton_settings_slider.setEnabled(True)

    def set_motor_disabled(self):
        self.ui.actionConnectMotor.setEnabled(True)
        self.ui.actionDisconnectMotor.setDisabled(True)
        self.ui.lineEdit_settings_slider_steps.setText("")
        self.ui.lineEdit_settings_slider_frequenz.setText("")
        self.ui.input_info_slider_links.setText("")
        self.ui.input_info_slider_rechts.setText("")
        self.ui.input_info_slider_status.setText("")
        self.ui.input_info_slider_frequenz.setText("")
        self.ui.input_info_slider_richtung.setText("")
        self.ui.input_info_slider_steps.setText("")
        if not self.ui.actionDisconnectCamera.isEnabled() and not self.ui.actionDisconnectMotor.isEnabled() \
                and not self.ui.pushButton_steuerung_slider.isEnabled():
            self.ui.actionDisconnect.setEnabled(True)

        self.ui.groupBox_info_slider.setDisabled(True)
        self.ui.input_info_slider_rechts.setDisabled(True)
        self.ui.input_info_slider_links.setDisabled(True)
        self.ui.input_info_slider_frequenz.setDisabled(True)
        self.ui.input_info_slider_richtung.setDisabled(True)
        self.ui.input_info_slider_status.setDisabled(True)
        self.ui.input_info_slider_steps.setDisabled(True)
        self.ui.label_info_slider_rechts.setDisabled(True)
        self.ui.label_info_slider_links.setDisabled(True)
        self.ui.label_info_slider_frequenz.setDisabled(True)
        self.ui.label_info_slider_richtung.setDisabled(True)
        self.ui.label_info_slider_status.setDisabled(True)
        self.ui.label_info_slider_steps.setDisabled(True)

        self.ui.groupBox_settings_slider.setDisabled(True)
        self.ui.comboBox_settings_slider_richtung.setDisabled(True)
        self.ui.comboBox_settings_slider_start.setDisabled(True)
        self.ui.label_settings_slider_frequenz.setDisabled(True)
        self.ui.label_settings_slider_richtung.setDisabled(True)
        self.ui.label_settings_slider_start.setDisabled(True)
        self.ui.label_settings_slider_steps.setDisabled(True)
        self.ui.lineEdit_settings_slider_frequenz.setDisabled(True)
        self.ui.lineEdit_settings_slider_steps.setDisabled(True)
        self.ui.pushButton_settings_slider.setDisabled(True)
        self.ui.pushButton_steuerung_slider_position.setDisabled(True)

    def check_slider_settings(self, data):
        if self.ui.comboBox_settings_slider_start.currentText() and \
                self.ui.comboBox_settings_slider_richtung.currentText() and \
                self.ui.lineEdit_settings_slider_steps.text() and \
                self.ui.lineEdit_settings_slider_frequenz.text():
            self.ui.pushButton_settings_slider.setEnabled(True)
            self.ui.pushButton_steuerung_slider_position.setEnabled(True)

    def get_slider_settings(self):
        return {
            'start': self.ui.comboBox_settings_slider_start.currentText(),
            'direction': self.ui.comboBox_settings_slider_richtung.currentText(),
            'distance': self.ui.lineEdit_settings_slider_steps.text(),
            'frequency': self.ui.lineEdit_settings_slider_frequenz.text(),
            'type': 'automatic'
        }

    def get_slider_start(self):
        return self.ui.comboBox_settings_slider_start.currentText()

    def set_slider_info(self, data):
        # if 'running' in data and data['running']:
        #     self.ui.input_info_slider_status.setText("An")
        #     self.ui.input_info_slider_status.setStyleSheet("color: green; border: none;")
        # else:
        self.ui.input_info_slider_status.setText("Aus")
        self.ui.input_info_slider_status.setStyleSheet("color: #DB2828; border: none;")
        self.ui.input_info_slider_frequenz.setText(data['frequency'])
        self.ui.input_info_slider_richtung.setText(data['direction'])
        if data['type'] == 'automatic':
            self.ui.input_info_slider_steps.setText(f"{data['distance']} cm")
        elif data['type'] == 'manual':
            self.ui.input_info_slider_steps.setText(f"{data['distance']} Schritte")
        self.ui.groupBox_steuerung_slider.setEnabled(True)
        self.ui.pushButton_steuerung_slider.setEnabled(True)
        print("Button enabled")

    def slider_started(self):
        print("Started")
        self.ui.pushButton_steuerung_slider.setDisabled(True)
        self.ui.input_info_slider_status.setText("An")
        self.ui.input_info_slider_status.setStyleSheet("color: green; border: none;")
        self.ui.groupBox_settings_slider.setDisabled(True)

    def slider_finished(self):
        print("Finished")
        self.ui.pushButton_steuerung_slider.setEnabled(True)
        self.ui.input_info_slider_status.setText("Aus")
        self.ui.input_info_slider_status.setStyleSheet("color: #DB2828; border: none;")
        self.ui.groupBox_settings_slider.setEnabled(True)

    def set_distance(self, distance):
        self.ui.input_info_slider_links.setText(f"{distance['left']} cm")
        self.ui.input_info_slider_rechts.setText(f"{distance['right']} cm ")

    def set_sensors_connected(self):
        self.ui.actionConnectSensors.setDisabled(True)
        self.ui.actionDisconnectSensors.setEnabled(True)

    def set_sensors_disconnected(self):
        self.ui.actionConnectSensors.setEnabled(True)
        self.ui.actionDisconnectSensors.setDisabled(True)
        self.ui.input_info_slider_links.setText("")
        self.ui.input_info_slider_rechts.setText("")

    def check_kamera_settings(self, data):
        if self.ui.lineEdit_settings_kamera_takes.text():
            self.ui.pushButton_settings_kamera.setEnabled(True)

    def get_kamera_settings(self):
        return {
            'takes': self.ui.lineEdit_settings_kamera_takes.text(),
            'focal': self.ui.comboBox_settings_kamera_blende.currentText(),
            'shutter': self.ui.comboBox_settings_kamera_shutter.currentText(),
            'iso': self.ui.comboBox_settings_kamera_iso.currentText()
        }
