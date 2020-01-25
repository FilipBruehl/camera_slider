from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from typing import Any, Dict
from classes.ui.designer.main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    QMainWindow als Hauptfenster des User Interfaces.
    """

    # Anlegen mehrerer pyqtSignal Instanzen, um ausgelöste Events an die Klasse Client weiterleiten zu können
    connect_server_signal = pyqtSignal()
    disconnect_server_signal = pyqtSignal()
    connect_camera_signal = pyqtSignal()
    disconnect_camera_signal = pyqtSignal()
    connect_motor_signal = pyqtSignal()
    disconnect_motor_signal = pyqtSignal()
    connect_sensors_signal = pyqtSignal()
    disconnect_sensors_signal = pyqtSignal()
    set_slider_settings_signal = pyqtSignal()
    set_slider_settings_manual_signal = pyqtSignal()
    set_camera_settings_signal = pyqtSignal()
    set_camera_settings_takes_signal = pyqtSignal()
    take_picture_signal = pyqtSignal()
    start_slider_signal = pyqtSignal()
    measure_distance_signal = pyqtSignal()
    position_slider_signal = pyqtSignal()
    about_signal = pyqtSignal()
    close_signal = pyqtSignal()

    def __init__(self):
        """
        Konstruktor der Klasse MainWindow.

        Erstellt das User Interface aus der vom Designer generierten Datei.
        Weist relevanten UI-Elementen Listener mit einem pyqtSignal als Callback zu.
        """

        super().__init__()                                                                                              # Ruft Kontruktor der erbenden Klasse "QMainWindow" auf
        self.ui = Ui_MainWindow()                                                                                       # Erstellt Instanz der vom Designer erstellten GUI-Klasse
        self.ui.setupUi(self)                                                                                           # Erstellen des generierten UIs
        self.ui.label_info_server_ip.setObjectName("serverip")                                                          # Weist dem Label "label_info_server_ip" den ObjectNamen "serverip" zu
        self.ui.input_info_camera_name.setObjectName("cameraname")                                                      # Weist dem Label "input_info_camera_name" den ObjectNamen "cameraname" zu
        self.ui.actionConnect.triggered.connect(self.connect_server_signal)                                             # Weist den einzelnen Menü-Punkten einen OnTriggeredListener mit einem pyqtSignal als Callback zu
        self.ui.actionDisconnect.triggered.connect(self.disconnect_server_signal)                                       # -
        self.ui.actionConnectCamera.triggered.connect(self.connect_camera_signal)                                       # -
        self.ui.actionDisconnectCamera.triggered.connect(self.disconnect_camera_signal)                                 # -
        self.ui.actionConnectMotor.triggered.connect(self.connect_motor_signal)                                         # -
        self.ui.actionDisconnectMotor.triggered.connect(self.disconnect_motor_signal)                                   # -
        self.ui.actionConnectSensors.triggered.connect(self.connect_sensors_signal)                                     # -
        self.ui.actionDisconnectSensors.triggered.connect(self.disconnect_sensors_signal)                               # -
        self.ui.actionAbout.triggered.connect(self.about)                                                               # Weist dem Menü-Punkt "actionAbout" einen OnTriggeredListener mit der Funktion "about" als Callback zu
        self.ui.actionClose.triggered.connect(self.close)                                                               # Weist dem Menü-Punkt "actionClose" einen OnTriggeredListener mit der Funktion "close" als Callback zu
        self.ui.pushButton_settings_slider.clicked.connect(self.set_slider_settings_signal)                             # Weist einzelnen Buttons einen OnClickedListener mit einem pyqtSignal als Callback zu
        self.ui.pushButton_steuerung_manuell.clicked.connect(self.set_slider_settings_manual_signal)                    # -
        self.ui.pushButton_settings_kamera.clicked.connect(self.set_camera_settings_signal)                             # -
        self.ui.pushButton_settings_kamera_takes.clicked.connect(self.set_camera_settings_takes_signal)                 # -
        self.ui.pushButton_steuerung_kamera.clicked.connect(self.take_picture_signal)                                   # -
        self.ui.pushButton_steuerung_slider.clicked.connect(self.start_slider_signal)                                   # -
        self.ui.pushButton_steuerung_abstand.clicked.connect(self.measure_distance_signal)                              # -
        self.ui.pushButton_steuerung_slider_position.clicked.connect(self.position_slider_signal)                       # -
        self.ui.comboBox_settings_slider_start.currentTextChanged.connect(self.check_slider_settings)                   # Weist der ComboBox "comboBox_settings_slider_start" einen OnCurrentTextChangesListener mit der Funktion "check_slider_settings" als Callback zu
        self.ui.comboBox_settings_slider_richtung.currentTextChanged.connect(self.check_slider_settings)                # Weist der ComboBox "comboBox_settings_slider_richtung" einen OnCurrentTextChangesListener mit der Funktion "check_slider_settings" als Callback zu
        self.ui.comboBox_steuerung_manuell_richtung.currentTextChanged.connect(self.check_manual_settings)              # Weist der ComboBox "comboBox_steuerung_manuell_richtung" einen OnCurrentTextChangesListener mit der Funktion "check_manual_settings" als Callback zu
        self.ui.lineEdit_settings_slider_steps.textChanged.connect(self.check_slider_settings)                          # Weist dem LineEdit "lineEdit_settings_slider_steps" einen OnTextChangedListener mit der Funktion "check_slider_settings" als Callback zu
        self.ui.lineEdit_settings_slider_frequenz.textChanged.connect(self.check_slider_settings)                       # Weist dem LineEdit "lineEdit_settings_slider_frequenz" einen OnTextChangedListener mit der Funktion "check_slider_settings" als Callback zu
        self.ui.lineEdit_settings_kamera_takes.textChanged.connect(self.check_camera_settings)                          # Weist dem LineEdit "lineEdit_settings_kamera_takes" einen OnTextChangedListener mit der Funktion "check_camera_settings" als Callback zu
        self.ui.lineEdit_steuerung_manuell_distanz.textChanged.connect(self.check_manual_settings)                      # Weist dem LineEdit "lineEdit_steuerung_manuell_distanz" einen OnTextChangedListener mit der Funktion "check_manual_settings" als Callback zu

    @staticmethod
    def about() -> None:
        """
        Statische Methode zum Anzeigen einer MessageBox mit Informationen zum Projekt.

        Wird aufgerufen, sobald der Nutzer den Menü-Punkt "actionAbout" anklickt.

        :return: None
        """

        msg = QMessageBox()
        msg.setWindowTitle("Über Camera Slider")
        msg.setText(
            "<h3>Über Camera Slider</h3><p>Projektarbeit für das Modul CPS der FH Kiel.<br>Erstellt von Filip Hugo Brühl</p><br><a href='https://github.com/FilipBruehl/camera_slider'>Download auf GitHub</a>")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def set_connected(self, ip: str) -> None:
        """
        Funktion zum Einstellen von UI- Elementen, nachdem der Client mit dem Server verbunden wurde.

        Aktiviert die entsprechende GroupBox für die IP-Adresse und zeigt die verbundene IP-Adresse in einem Label an.
        Zusätzlich werden Menü-Punkte für die weitere Verwendung des Programms konfiguriert.

        :param ip: IP-Adresse des Server
        :type ip: str

        :return: None
        """

        self.ui.groupBox_info_server.setEnabled(True)                                                                   # Aktiviert die GroupBox "groupBox_info_server"
        self.ui.label_info_server.setEnabled(True)                                                                      # Aktiviert das Label "label_info_server"
        self.ui.label_info_server_ip.setText(ip)                                                                        # Setzt die übergebene IP als Inhalt des Labels
        self.ui.label_info_server_ip.setProperty("connected", True)                                                     # Setzt die Property "connected" des labels auf True
        self.ui.label_info_server_ip.style().unpolish(self.ui.label_info_server_ip)                                     # Lade die Styles des Labels neu, um auf die Veränderung der Property zu reagieren
        self.ui.label_info_server_ip.style().polish(self.ui.label_info_server_ip)                                       # -
        self.ui.label_info_server_ip.update()                                                                           # -
        self.ui.actionConnect.setDisabled(True)                                                                         # Deaktiviere den Menü-Punkt "actionConnect"
        self.ui.actionClose.setDisabled(True)                                                                           # Deaktiviere den Menü-Punkt "actionClose"
        self.ui.actionDisconnect.setEnabled(True)                                                                       # Aktiviere den Menü-Punkt "actionDisconnect"
        self.ui.actionConnectCamera.setEnabled(True)                                                                    # Aktiviere den Menü-Punkt "actionConnectCamera"
        self.ui.actionConnectMotor.setEnabled(True)                                                                     # Aktiviere den Menü-Punkt "actionConnectMotor"
        self.ui.actionConnectSensors.setEnabled(True)                                                                   # Aktiviere den Menü-Punkt "actionConnectSensors"

    def set_connection_failed(self) -> None:
        """
        Funktion zum Anzeigen einer Fehlermeldung, falls keine Verbindung mit dem Server aufgebaut werden konnte.

        :return: None
        """

        self.ui.groupBox_info_server.setEnabled(True)                                                                   # Aktiviert die GroupBox "groupBox_info_server"
        self.ui.label_info_server.setEnabled(True)                                                                      # Aktiviert das Label "label_info_server"
        self.ui.label_info_server_ip.setText("Verbinden fehlgeschlagen")                                                # Setzt den Inhalt des Labels
        self.ui.label_info_server_ip.setProperty("connected", False)                                                    # Setzt die Property "connected" des Labels auf False
        self.ui.label_info_server_ip.style().unpolish(self.ui.label_info_server_ip)                                     # Lade die Styles des Labels neu, um auf die Veränderung der Property zu reagieren
        self.ui.label_info_server_ip.style().polish(self.ui.label_info_server_ip)                                       # -
        self.ui.label_info_server_ip.update()                                                                           # -

    def set_not_connected(self) -> None:
        """
        Funktion zum Deaktivieren von UI-Elementen, nachdem die Verbindung mit dem Server beendet wurde.

        Deaktiviert die entsprechende GroupBox für die IP-Adresse und konfiguriert Menü-Punkte für die weitere Benutzung des Programms.

        :return: None
        """

        self.ui.groupBox_info_server.setDisabled(True)                                                                  # Deaktiviert die GroupBox "groupBox_info_server"
        self.ui.label_info_server.setDisabled(True)                                                                     # Deaktiviert das label "label_info_server"
        self.ui.label_info_server_ip.setText("Nicht verbunden")                                                         # Setzt den Inhalt des Labels
        self.ui.label_info_server_ip.setProperty("connected", False)                                                    # Setzt die Property "connected" des Labels auf False
        self.ui.label_info_server_ip.style().unpolish(self.ui.label_info_server_ip)                                     # Lade die Styles des Labels neu, um auf die Veränderung der Property zu reagieren
        self.ui.label_info_server_ip.style().polish(self.ui.label_info_server_ip)                                       # -
        self.ui.label_info_server_ip.update()                                                                           # -
        self.ui.actionConnect.setEnabled(True)                                                                          # Aktiviere den Menü-Punkt "actionConnect"
        self.ui.actionClose.setEnabled(True)                                                                            # Aktiviere den Menü-Punkt "actionClose"
        self.ui.actionDisconnect.setDisabled(True)                                                                      # Deaktiviere den Menü-Punkt "actionDisconnect"
        self.ui.actionConnectCamera.setDisabled(True)                                                                   # Deaktiviere den Menü-Punkt "actionConnectCamera"
        self.ui.actionConnectMotor.setDisabled(True)                                                                    # Deaktiviere den Menü-Punkt "actionConnectMotor"
        self.ui.actionConnectSensors.setDisabled(True)                                                                  # Deaktiviere den Menü-Punkt "actionConnectSensors"

    def set_camera_connected(self, camera_info: Dict) -> None:
        """
        Funktion zum Aktivieren der UI-Elemente der Kamera und Setzen von übergebenen Initialwerten.

        Konfiguriert die zur Kamera gehörenden Menü-Punkte und aktiviert die zur Kamera gehörenden UI-Elemente.
        Anschließend werden die übergebenen Kamera-Daten in den jeweiligen Labels angezeigt.

        :param camera_info: Daten der Kamera
        :type camera_info: dict

        :return: None
        """

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
        self.ui.pushButton_settings_kamera.setEnabled(True)

        self.ui.groupBox_steuerung_kamera.setEnabled(True)
        self.ui.pushButton_steuerung_kamera.setEnabled(True)

    def set_camera_options(self, data: Dict) -> None:
        """
        Funktion zum Anzeigen der verfügbaren Einstellungsmöglichkeiten der Kamera.

        Extrahiert die einzelnen Einstellungsmöglichkeiten der Kamera und schreibt diese in die dazugehörige ComboBox.
        Anschließend wird mit Hilfe der bereits vorhandenen Informationen aus den Informations-Labels die momentane Einstellung als aktiv gesetzt.

        :param data: Einstellungsmöglichkeiten der Kamera
        :type data: dict

        :return: None
        """

        self.ui.comboBox_settings_kamera_blende.addItems(data['focal'])                                                 # Einzelne Einstellungsmöglichkeiten in ihre entsprechende ComboBox schreiben
        self.ui.comboBox_settings_kamera_shutter.addItems(data['shutter'])                                              # -
        self.ui.comboBox_settings_kamera_iso.addItems(data['iso'])                                                      # -

        focal_index = self.ui.comboBox_settings_kamera_blende.findText(self.ui.input_info_camera_blende.text())         # Herausfinden des Index der aktuellen Blenden-Einstellung
        if focal_index >= 0:                                                                                            # Überprüfen, ob der Index größer als 0 ist
            self.ui.comboBox_settings_kamera_blende.setCurrentIndex(focal_index)                                        # Aktuelle Blenden-Einstellung als aktives Element setzen
        shutter_index = self.ui.comboBox_settings_kamera_shutter.findText(self.ui.input_info_camera_shutter.text())     # Herausfinden des Index der aktuellen Verschlusszeit-Einstellung
        if shutter_index >= 0:                                                                                          # Überprüfen, ob der Index größer als 0 ist
            self.ui.comboBox_settings_kamera_shutter.setCurrentIndex(shutter_index)                                     # Aktuelle Verschlusszeit-Einstellung als aktives Element setzen
        iso_index = self.ui.comboBox_settings_kamera_iso.findText(self.ui.input_info_camera_iso.text())                 # Herausfinden des Index der aktuellen Iso-Einstellung
        if iso_index >= 0:                                                                                              # Überprüfen, ob der Index größer als 0 ist
            self.ui.comboBox_settings_kamera_iso.setCurrentIndex(iso_index)                                             # Aktuelle Iso-Einstellung als aktives Element setzen

    def set_camera_values(self, data: Dict) -> None:
        """
        Funktion zum Anzeigen der Kamera-Einstellung.

        Extrahiert die einzelnen Einstellungen aus den übergebenen Daten und weist sie ihrem jeweiligem Label zu.

        :param data: Kamera-Einstellungen
        :type data: dict

        :return: None
        """

        self.ui.input_info_camera_akku.setText(data['battery'])
        self.ui.input_info_camera_blende.setText(data['focal'])
        self.ui.input_info_camera_shutter.setText(data['shutter'])
        self.ui.input_info_camera_iso.setText(data['iso'])
        self.ui.input_info_camera_fokus.setText(data['focus'])
        self.ui.input_info_camera_format.setText(data['quality'])

    def set_camera_not_available(self) -> None:
        """
        Funktion zum Anzeigen einer Fehlermeldung, dass keine Kamera verfügbar ist bzw. verbunden werden konnte.

        Schreibt eine Meldung in das Label des Kameranamens und aktualisiert die Property.
        Anschließend werden die Styles für das Label neu geladen.

        :return: None
        """

        self.ui.input_info_camera_name.setText("Keine Kamera verfügbar")
        self.ui.input_info_camera_name.setProperty("connected", False)
        self.ui.input_info_camera_name.style().unpolish(self.ui.input_info_camera_name)
        self.ui.input_info_camera_name.style().polish(self.ui.input_info_camera_name)
        self.ui.input_info_camera_name.update()

    def set_camera_disconnected(self) -> None:
        """
        Funktion zum Deaktivieren von UI-Elementen der Kamera, nachdem die Verbindung zu dieser getrennt wurde.

        Konfiguriert die zur Kamera gehörenden Menü-Punkte.
        Überprüft, ob noch weitere Komponenten (Motor, Sensoren) verbunden sind, um das Menü weiter zu konfigurieren.
        Anschließend werden die zur Kamera gehörenden UI-Elemente in ihren Ursprungszustand gestzt und deaktiviert.

        :return: None
        """

        self.ui.actionConnectCamera.setEnabled(True)
        self.ui.actionDisconnectCamera.setDisabled(True)
        if not self.ui.actionDisconnectCamera.isEnabled() and not self.ui.actionDisconnectMotor.isEnabled() and not self.ui.actionDisconnectSensors.isEnabled():
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

        self.ui.pushButton_settings_kamera_takes.setDisabled(True)

    def set_motor_connected(self) -> None:
        """
        Funktion zum Aktivieren der UI-Elemente des Motors.

        Konfiguriert die zum Motor gehörenden Menü-Punkte und aktiviert die zum Motor gehörenden UI-Elemente.

        :return: None
        """

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
        self.ui.pushButton_steuerung_slider_position.setEnabled(True)

        self.ui.groupBox_steuerung_manuell.setEnabled(True)
        self.ui.pushButton_steuerung_manuell.setDisabled(True)

    def set_motor_disabled(self) -> None:
        """
        Funktion zum Deaktivieren von UI-Elementen des Schrittmotors, nachdem die Verbindung zu diesem getrennt wurde.

        Konfiguriert die zum Motor gehörenden Menü-Punkte.
        Überprüft, ob noch weitere Komponenten (Kamera, Sensoren) verbunden sind, um das Menü weiter zu konfigurieren.
        Anschließend werden die zum Motor gehörenden UI-Elemente in ihren Ursprungszustand gestzt und deaktiviert.

        :return: None
        """

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
                and not self.ui.pushButton_steuerung_slider.isEnabled() \
                and not self.ui.actionDisconnectSensors.isEnabled():
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

        self.ui.groupBox_steuerung_manuell.setDisabled(True)

    def check_slider_settings(self, data):
        if self.ui.comboBox_settings_slider_start.currentText() and \
                self.ui.comboBox_settings_slider_richtung.currentText() and \
                self.ui.lineEdit_settings_slider_steps.text() and \
                self.ui.lineEdit_settings_slider_frequenz.text():
            self.ui.pushButton_settings_slider.setEnabled(True)

    def get_slider_settings(self):
        return {
            'direction': self.ui.comboBox_settings_slider_richtung.currentText(),
            'distance': self.ui.lineEdit_settings_slider_steps.text(),
            'frequency': self.ui.lineEdit_settings_slider_frequenz.text()
        }

    def check_manual_settings(self, data):
        if self.ui.comboBox_steuerung_manuell_richtung.currentText() and \
                self.ui.lineEdit_steuerung_manuell_distanz.text():
            self.ui.pushButton_steuerung_manuell.setEnabled(True)

    def get_slider_settings_manual(self):
        return {
            'direction': self.ui.comboBox_steuerung_manuell_richtung.currentText(),
            'distance': self.ui.lineEdit_steuerung_manuell_distanz.text(),
            'frequency': 900
        }

    def get_slider_start(self):
        return self.ui.comboBox_settings_slider_start.currentText()

    def set_slider_info(self, data):
        self.ui.input_info_slider_status.setText("Aus")
        self.ui.input_info_slider_status.setStyleSheet("color: #DB2828; border: none;")
        self.ui.input_info_slider_frequenz.setText(data['frequency'])
        self.ui.input_info_slider_richtung.setText(data['direction'])
        self.ui.input_info_slider_steps.setText(f"{data['distance']} cm")
        self.ui.groupBox_steuerung_slider.setEnabled(True)
        self.ui.pushButton_steuerung_slider.setEnabled(True)

    def slider_started(self):
        self.ui.pushButton_steuerung_slider.setDisabled(True)
        self.ui.pushButton_steuerung_kamera.setDisabled(True)
        self.ui.pushButton_steuerung_abstand.setDisabled(True)
        self.ui.input_info_slider_status.setText("An")
        self.ui.input_info_slider_status.setStyleSheet("color: green; border: none;")
        self.ui.groupBox_settings_slider.setDisabled(True)
        self.ui.groupBox_steuerung_manuell.setDisabled(True)
        self.ui.groupBox_settings_kamera.setDisabled(True)

    def slider_finished(self):
        self.ui.pushButton_steuerung_slider.setEnabled(True)
        self.ui.pushButton_steuerung_kamera.setEnabled(True)
        self.ui.pushButton_steuerung_abstand.setEnabled(True)
        self.ui.input_info_slider_status.setText("Aus")
        self.ui.input_info_slider_status.setStyleSheet("color: #DB2828; border: none;")
        self.ui.groupBox_settings_slider.setEnabled(True)
        self.ui.groupBox_steuerung_manuell.setEnabled(True)
        self.ui.groupBox_settings_kamera.setEnabled(True)

    def set_distance(self, distance):
        self.ui.input_info_slider_links.setText(f"{distance['left']} cm")
        self.ui.input_info_slider_rechts.setText(f"{distance['right']} cm ")

    def set_sensors_connected(self):
        self.ui.actionConnectSensors.setDisabled(True)
        self.ui.actionDisconnectSensors.setEnabled(True)
        self.ui.groupBox_steuerung_abstand.setEnabled(True)
        self.ui.pushButton_steuerung_abstand.setEnabled(True)

    def set_sensors_disconnected(self):
        self.ui.actionConnectSensors.setEnabled(True)
        self.ui.actionDisconnectSensors.setDisabled(True)
        self.ui.input_info_slider_links.setText("")
        self.ui.input_info_slider_rechts.setText("")
        self.ui.groupBox_steuerung_abstand.setDisabled(True)
        self.ui.pushButton_steuerung_abstand.setDisabled(True)

    def check_camera_settings(self, data):
        if self.ui.lineEdit_settings_kamera_takes.text():
            self.ui.pushButton_settings_kamera_takes.setEnabled(True)

    def get_camera_settings(self):
        return {
            'focal': self.ui.comboBox_settings_kamera_blende.currentText(),
            'shutter': self.ui.comboBox_settings_kamera_shutter.currentText(),
            'iso': self.ui.comboBox_settings_kamera_iso.currentText()
        }

    def get_camera_takes(self):
        return self.ui.lineEdit_settings_kamera_takes.text()
