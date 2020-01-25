import socket
import pickle
import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication
from typing import Any
from classes.ui.MainWindow import MainWindow
from classes.ui.ConnectServer import ConnectServer


class Client:
    """
    Client für die Kommunikation mit dem Server.

    Der Client kümmert sich um die Kommunikation mit dem Server und die Interaktion mit der GUI.
    """

    def __init__(self):
        """
        Konstruktor der Klasse Client.

        Erstellt den Socket für die Netzwerk-Verbindung und die Hauptapplikation, sowie das User Interface
        """

        self.host_port = 50007                                                                                          # Initialisiere den Host-Port auf 50007
        self.host_ip = ""                                                                                               # Initialisiere die Host-IP auf einen leeren String
        self.header_size = 10                                                                                           # Setze die Header Größe auf 10 fest
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                 # Erstelle einen neuen TCP/IPv4 Socket
        self._connected = False                                                                                         # Initialisiere Variable mit False
        self._camera_connected = False                                                                                  # -
        self._camera_info = None                                                                                        # Initialisisiere Variable mit None
        self._camera_options = None                                                                                     # -
        self._motor_connected = False                                                                                   # -
        self._app = QApplication(sys.argv)                                                                              # Erstelle Instanz von QApplication als Hauptapplikation
        self._window = MainWindow()                                                                                     # Erstelle Instanz von MainWindow für das User Interface
        self._thread_recv = Thread(target=self.receive)                                                                 # Erstlle einen neuen Thread mit der Funktion "receive" als Ziel
        self.init_main_window_signals()                                                                                 # Führe die Funktion "init_main_window_signals" aus

    def init_main_window_signals(self) -> None:
        """
        Funktion fängt die von der UI-Klasse ausgelösten Signale ab und weist ihnen Callback-Methoden zu.

        :return: None
        """

        self._window.connect_server_signal.connect(self.connect)
        self._window.disconnect_server_signal.connect(self.disconnect)
        self._window.connect_camera_signal.connect(self.connect_camera)
        self._window.disconnect_camera_signal.connect(self.disconnect_camera)
        self._window.connect_motor_signal.connect(self.connect_motor)
        self._window.disconnect_motor_signal.connect(self.disconnect_motor)
        self._window.connect_sensors_signal.connect(self.connect_sensors)
        self._window.disconnect_sensors_signal.connect(self.disconnect_sensors)
        self._window.set_slider_settings_signal.connect(self.set_slider_settings)
        self._window.set_slider_settings_manual_signal.connect(self.set_slider_settings_manual)
        self._window.set_camera_settings_signal.connect(self.set_camera_settings)
        self._window.set_camera_settings_takes_signal.connect(self.set_camera_settings_takes)
        self._window.take_picture_signal.connect(self.take_picture)
        self._window.start_slider_signal.connect(self.start_slider)
        self._window.measure_distance_signal.connect(self.measure_distance)
        self._window.position_slider_signal.connect(self.position_slider)

    def run(self) -> int:
        """
        Funktion zum Starten und Anzeigen des User Interfaces

        :return: Exit-Code der Applikation
        :rtype: int
        """

        self._window.show()                                                                                             # Zeigt das Fenster der UI an
        return self._app.exec_()                                                                                        # Startet den Event-Loop der Applikation und gibt nach Beenden den Exit-Code zurück

    def connect(self) -> None:
        """
        Baut eine Socket Verbindung mit dem Server auf.

        Öffnet ein neues Fenster zur Eingabe der IP-Adresse und versucht anschließend zu dieser eine Verbindung aufzubauen.
        Falls der Verbindungsaufbau erfolgreich ist, wird dies in der UI angezeigt.
        Sollte der Aufbau fehlschlagen wird eine Fehlermeldung angezeigt.

        :return: None
        """

        self.host_ip = ConnectServer.get_ip()                                                                           # Öffne ein neues Fenster der Klasse "ConnectServer" und speichere die zurück gegebene IP-Adresse
        try:
            self.socket.connect((self.host_ip, self.host_port))                                                         # Baue eine Verbindung mit dem Server auf. Ruft eine Exception hervor, falls der Aufbau fehlschlägt
            self._connected = True                                                                                      # Setze die Variable "_connected" auf True
            self._thread_recv.start()                                                                                   # Starte den Thread zum Empfangen der Daten vom Server
            print(f"Verbunden mit dem Server {self.host_ip}:{self.host_port}")                                          # Gebe eine Meldung in der Konsole aus
            self._window.set_connected(self.host_ip)                                                                    # Zeige in der GUI die verbundene IP-Adresse an
        except Exception as e:                                                                                          # Fange die Exception ab, falls beim Verbindungsaufbau ein Fehler auftritt
            self._window.set_connection_failed()                                                                        #   -> Gebe in der GUI eine Fehlermeldung aus
            print(e)                                                                                                    #   -> Schreibe den Fehler in die Konsole

    def disconnect(self) -> None:
        """
        Funktion zum Trennen der Verbidnung mit dem Server.

        Schickt an den Server eine Nachricht, dass die Verbindung getrennt werden soll.

        :return: None
        """

        self.send("disconnect_client")

    def connect_camera(self) -> None:
        """
        Funktion zum Verbinden der Kamera.

        Schickt dem Server eine Nachricht, dass die erste angeschlossene Kamera verbunden werden soll.

        :return: None
        """

        self.send("connect_camera", 0)

    def disconnect_camera(self) -> None:
        """
        Funktion zum Trennen der Verbindung mit der Kamera.

        Schickt dem Server eine Nachricht, dass die verbundene Kamera getrennt werden soll.

        :return: None
        """

        self.send("disconnect_camera")

    def connect_motor(self) -> None:
        """
        Funktion zum Verbinden des Schrittmotors.

        Schickt dem Server eine Nachricht, dass der Schrittmotor verbunden werden soll.

        :return: None
        """

        self.send("connect_motor")

    def disconnect_motor(self) -> None:
        """
        Funktion zum Trennen der Verbindung mit dem Schrittmotor.

        Schickt dem Server eine Nachricht, dass der verbundene Schrittmotor getrennt werden soll.

        :return: None
        """

        self.send("disconnect_motor")

    def connect_sensors(self) -> None:
        """
        Funktion zum Verbinden der Ultraschallsensoren.

        Schickt dem Server eine Nachricht, dass die Ultraschallsensoren verbunden werden sollen.

        :return: None
        """

        self.send("connect_sensors")

    def disconnect_sensors(self) -> None:
        """
        Funktion zum Trennen der Verbindung mit den Ultraschallsensoren.

        Schickt dem Server eine Nachricht, dass die verbundenen Ultraschallsensoren getrennt werden sollen.

        :return: None
        """

        self.send("disconnect_sensors")

    def set_slider_settings(self) -> None:
        """
        Funktion zum Einstellen des Sliders.

        Schickt dem Server eine Nachricht mit den aktuellen Einstellungen des Sliders, damit diese vom Server eingestellt werden können.

        :return: None
        """

        self.send("set_slider_settings", self._window.get_slider_settings())

    def set_slider_settings_manual(self) -> None:
        """
        Funktion zum manuellen Einstellen des Sliders.

        Schickt dem Server eine Nachricht mit den aktuellen manuellen Einstellungen des Sliders, damit diese vom Server eingestellt werden können.

        :return: None
        """

        self.send("set_slider_settings_manual", self._window.get_slider_settings_manual())

    def set_camera_settings(self) -> None:
        """
        Funktion zum Einstellen der Kamera.

        Schickt dem Server eine Nachricht mit den neuen Einstellungen der Kamera, damit dieser die Kamera einstellen kann.

        :return: None
        """

        self.send("set_camera_settings", self._window.get_camera_settings())

    def set_camera_settings_takes(self) -> None:
        """
        Funktion zum Einstellen der Anzahl an Aufnahmen.

        Schickt dem Server eine Nachricht mit der Anzahl der zu machenden Aufnahmen, damit der Server diese einstellen kann.

        :return: None
        """

        self.send("set_camera_settings_takes", self._window.get_camera_takes())

    def take_picture(self) -> None:
        """
        Funktion zum Aufnehmen eines Fotos.

        Schickt dem Server eine Nachricht, dass er ein Foto mit der Kamera aufnehmen soll.

        :return: None
        """

        self.send("take_picture")

    def start_slider(self) -> None:
        """
        Funktion zum Starten des Sliders.

        Schickt dem Server eine Nachricht, dass der Slider gestartet werden soll.

        :return: None
        """

        self.send("start_slider")

    def measure_distance(self) -> None:
        """
        Funktion zum Messen der Entfernungen.

        Schickt dem Server eine Nachricht, dass die Entfernungen gemessen werden sollen.

        :return: None
        """

        self.send("measure_distance")

    def position_slider(self) -> None:
        """
        Funktion zum Positionieren des Sliders.

        Schickt dem Server eine Nachricht mit der neuen Position, damit der Server den Slider positionieren kann.

        :return: None
        """

        self.send("position_slider", self._window.get_slider_start())

    def send(self, command: str, data: Any = None) -> None:
        """
        Funktion zum Senden von Befehlen und Daten an den Server.

        Nimmt einen Befehl und optional Daten in beliebiger Form (int, str, list, tuple) entgegen.
        Mit Hilfe der "pickle"-Bibliothek werden der Befehl und die Daten jeweils in ein Byte-Objekt konvertiert.
        Anschließend wird die jeweilige Größe der Byte-Objekte berechnet.

        Die zu verschickende Nachricht besteht aus drei Teilen, die separat nacheinander geschickt werden:
        1.) 10 Byte großer Header, der die Größe des nachfolgenden Befehls-Objekts beinhaltet.
        2.) Befehels-Objekt mit variabler Größe. Beinhaltet einen 10 Byte-Header mit der Größe des nachfolgenden Daten-Objekts, falls vorhanden, und den Befehl des Clients.
        3.) Das Daten-Objekt mit variabler Größe, falls vorhanden.

        Falls keine Daten zum versenden vorhanden sind, fällt das Daten-Objekt weg und der dazugehörige Header im Befehls-Objekt beinhaltet eine 0 als Größe.

        Durch das seperate versenden von Befehl und Daten mit einem jeweiligen Header kann gewährleistet werden, dass Befehel und Daten mit unterschiedlicher Größe ordnungsgemäß übertragen werden.

        :param command: zu verschickendes Kommando bzw. Nachricht
        :param data: zu verschickende Daten, falls vorhanden
        :type command: str
        :type data: Any

        :return: None
        """

        try:
            if data is not None:                                                                                        # Überprüfe, ob Daten übergeben wurden
                data = pickle.dumps(data)                                                                               #   -> Konvertiere die übergebenen Daten in ein Byte-Objekt
                data_len = bytes(f"{len(data):<{self.header_size}}", 'utf-8')                                           #   -> Ersetlle einen 10 Byte großen Header mit der Größe des Daten-Objekts als Inhalt
            else:                                                                                                       # Falls keine Daten übergeben wurden
                data_len = bytes(f"{0:<{self.header_size}}", 'utf-8')                                                   #   -> Erstelle einen 10 Byte großen Header mit 0 als Größe des Daten-Objektes als Inhalt
            command = pickle.dumps(command)                                                                             # Konvertiere den Befehl in ein Byte-Objekt
            command = data_len + command                                                                                # Der Daten-Header wird dem Befehl im Befehls-Objekt vorangestellt
            command_len = bytes(f"{len(command):<{self.header_size}}", 'utf-8')                                         # Erstelle einen 10 Byte großen Header mit der Größe des Befehls-Objekts als Inhalt
            self.socket.send(command_len)                                                                               # Verschicke den Befehls-Header
            self.socket.send(command)                                                                                   # Verschicke das Befehls-Objekt
            if data:                                                                                                    # Falls Daten übergeben wurden
                self.socket.send(data)                                                                                  #   -> Schicke das Daten-Objekt
            print(f"message send. command_len = {command_len}, command = {command}, data_len = {data_len}, data = {data}")
        except Exception as e:                                                                                          # Falls ein Fehler auftritt
            print(e)                                                                                                    #   -> Fehler wird in der Konsole ausgegeben

    def receive(self) -> None:
        """
        Funktion zum Empfangen von Nachrichten und Daten vom Server.

        Die Funktion läuft in einer while-Schleife, um so kontinuirlich Daten zu empfangen.

        Empfängt vom Server nacheinander 2 (falls keine Daten vorhanden sind) bzw. 3 (falls Daten vorhanden sind) Nachrichten:
        1.) 10 Byte großer Header, der die Größe des nachfolgenden Befehls-Objekts beinhaltet.
        2.) Befehels-Objekt mit variabler Größe. Beinhaltet einen 10 Byte-Header mit der Größe des nachfolgenden Daten-Objekts, falls vorhanden, und den Befehl des Clients.
        3.) Das Daten-Objekt mit variabler Größe, falls vorhanden.

        Die empfangenen Nachrichten werden anschließend dekodiert, in ihren ursprünglichen Datentyp umgewandelt und zu einer Nachricht zusammengefügt.
        Die zusammengefügte Nachricht wird zur Weiterverarbeitung durch den Client an eine separate Funktion übergeben.

        Durch das separate Empfangen von Befehl und Daten mit einem jeweiligen Header kann gewährleistet werden, dass Befehl und Daten mit unterschiedlicher Größe ordnungsgemäß empfangen werden.

        :return: None
        """

        command = None
        command_len = None
        data = None
        data_len = None

        while self._connected:                                                                                          # Dauerschleife, während "_connected" True ist
            try:
                command_len = self.socket.recv(self.header_size)                                                        # Empfange den ersten 10 Byte großen Header
                command_len = int(command_len.decode().strip())                                                         # Dekodiere den Header und konvertiere ihn in einen int
                if command_len > 0:                                                                                     # Überprüfe, ob der Header größer als 0 ist
                    command = self.socket.recv(command_len)                                                             #   -> Empfange das Befehls-Objekt mit der im Header angegebenen Größe
                    data_len = int(command[:self.header_size].decode().strip())                                         #   -> Extrahiere aus dem Befehls-Objekt den 10 Byte großen Header für das Datenobjekt, dekodiere diesen und wandle ihn in einen int um
                    command = command[self.header_size:]                                                                #   -> Extrahiere aus dem Befehls-Objekt den Befehls-Teil
                    command = pickle.loads(command)                                                                     #   -> Dekodiere den Befehl
                    if data_len > 0:                                                                                    # Überprüfe, ob der Daten-Header größer als 0 ist
                        data = self.socket.recv(data_len)                                                               #   -> Empfange das Daten-Objekt
                        data = pickle.loads(data)                                                                       #   -> Dekodiere das Daten-Objekt
                print(f"message received. command_len = {command_len}, command = {command}, data_len = {data_len}, data = {data}")
                self.handle_command(command, data)                                                                      # Übergebe den Befehl und die Daten an eine separate Funktion zur weiteren Verarbeitung
            except Exception as e:                                                                                      # Falls ein Fehler auftritt
                print(e)                                                                                                #   -> Gebe den Fehler in der Konsole aus
            finally:
                command = None
                command_len = None
                data = None
                data_len = None

    def handle_command(self, command: str, data: Any = None) -> None:
        """
        Funktion zum verarbeiten der empfangenen Befehle und Daten.

        Es wird der übergebene Befehl mit zu erwartenden Befehlen verglichen und bei Übereinstimmung eine entsprechende Funktion zum ausführen des Befehls aufgerufen.

        :param command: übergebener Befehl
        :param data: übergebene Daten, falls vorhanden
        :type command: str
        :type data: Any

        :return: None
        """
        
        if command == "camera_not_available":
            self.on_camera_not_available()
        elif command == "camera_init":
            self.on_camera_init(data)
        elif command == "camera_options":
            self.on_camera_options(data)
        elif command == "camera_values":
            self.on_camera_values(data)
        elif command == "camera_disconnected":
            self.on_camera_disconnected()
        elif command == "motor_connected":
            self.on_motor_connected()
        elif command == "motor_disconnected":
            self.on_motor_disconnected()
        elif command == "slider_settings_set":
            self.on_slider_settings_set(data)
        elif command == "slider_started":
            self.on_slider_started()
        elif command == "slider_finished":
            self.on_slider_finished()
        elif command == "sensors_connected":
            self.on_sensors_connected()
        elif command == "sensors_disconnected":
            self.on_sensors_disconnected()
        elif command == "distance":
            self.on_distance(data)
        elif command == "disconnect":
            self.on_disconnect()

    def on_disconnect(self) -> None:
        """
        Funktion zum Beenden des Clients.

        Wird ausgeführt, sbald der Server die Nachricht "disconnect" sendet.
        Beendet die Socket-Verbindung und gibt eine Meldung in der UI aus.

        :return: None
        """

        self.socket.close()                                                                                             # Beendet die Socket-Verbindung
        self._connected = False                                                                                         # Setzt "_connected" auf False, da keine Verbindung mehr aktiv ist
        self._window.set_not_connected()                                                                                # Gibt eine Meldung in der UI aus
        print("Disconnected")

    def on_camera_not_available(self) -> None:
        """
        Funktion zum Anzeigen einer Fehlermeldung in der UI, falls keine Kamera angeschlossen ist.

        Wird ausgeführt, sobald der Server die Nachricht "camera_not_available" sendet.

        :return: None
        """

        self._window.set_camera_not_available()

    def on_camera_init(self, data: Any) -> None:
        """
        Funktion zum Empfangen und Initalisieren der UI mit Einstellungsdaten der verbundenen Kamera.

        Wird ausgeführt, sobald der Server die Nachricht "camera_init" sendet.
        Speichert die mitgeschickten Daten der Kamera und übergibt diese an die UI, damit sie angezeigt werden.
        Fordert anschließend die verfügbaren Einstellungsmöglichkeiten der Kamera vom Server an.

        :param data: Daten der Kamera
        :type data: Any

        :return: None
        """

        self._camera_connected = True
        self._camera_info = data
        self._window.set_camera_connected(data)
        self.send("get_camera_options")

    def on_camera_options(self, data: Any) -> None:
        """
        Funktion zum Empfangen von Einstellungsmöglichkeiten der verbundenen Kamera.

        Wird ausgeführt, sobald der Server die Nachricht "camera_options" sendet.
        Speichert die mitgeschickten Einstellungsmöglichkeiten der Kamera und übergibt diese an die UI, damit sie angezeigt werden.

        :param data: Einstellungsmöglichkeiten der Kanmera
        :type data: Any

        :return: None
        """

        self._camera_options = data
        self._window.set_camera_options(data)

    def on_camera_values(self, data: Any) -> None:
        """
        Funktion zum Empfangen von neuen Daten der Kamera und Anzeigen dieser in der UI.

        Wird ausgeführt, sobald der Server die Nachricht "camera_values" sendet.
        Speichert die neu geschickten Daten der Kamera und übergibt sie der UI zum Anzeigen.

        :param data: Daten der Kamera
        :type data: Any

        :return: None
        """

        self._camera_info = data
        self._window.set_camera_values(data)

    def on_camera_disconnected(self) -> None:
        """
        Funktion zum Zurücksetzen der Kameradaten, nachdem die Verbindung zur Kamera getrennt wurde.

        Wird ausgeführt, sobald der Server die Nachricht "camera_disconnected" sendet.
        Setzt die zur Kamera gehörigen Variablen in ihren Ursprungszustand zurück und zeigt in der UI eine Meldung an, dass keine Kamera mehr verbunden ist.

        :return: None
        """

        self._camera_connected = False
        self._camera_info = None
        self._camera_options = None
        self._window.set_camera_disconnected()

    def on_motor_connected(self) -> None:
        """
        Funktion zum Initialisieren der UI, nachdem der Schrittmotor verbunden wurde.

        Wird ausgeführt, sobald der Server die Nachricht "motor_connected" sendet.

        :return: None
        """

        self._motor_connected = True
        self._window.set_motor_connected()

    def on_motor_disconnected(self) -> None:
        """
        Funktion zum Zurücksetzen der UI, nachdem die Verbindung mit dem Schrittmotor getrennt wurde.

        Wird ausgefühert, sobald der Server die Nachricht "motor_disconnected" sendet.

        :return: None
        """

        self._motor_connected = False
        self._window.set_motor_disabled()

    def on_slider_settings_set(self, data: Any) -> None:
        """
        Funktion zum Empfangen der Slider-Einstellungen und Übergabe dieser an die UI.

        Wird ausgeführt, sobald der Server die Nachricht "slider_settings_set" sendet.

        :param data: Einstellungen des Sliders
        :type data: Any

        :return: None
        """

        self._window.set_slider_info(data)

    def on_slider_started(self) -> None:
        """
        Funktion zum Aktualisieren der UI, sobald der Slider-Durchlauf gestartet wurde.

        Wird ausgeführt, sobald der Server die Nachricht "slider_started" sendet.

        :return: None
        """

        self._window.slider_started()

    def on_slider_finished(self) -> None:
        """
        Funktion zum Aktualisieren der UI, sobald der Slider-Durchlauf beendet ist.

        Wird ausgeführt, sobald der Server die Nachricht "slider_finished" sendet.

        :return: None
        """

        self._window.slider_finished()

    def on_distance(self, data: Any) -> None:
        """
        Funktion zum Empfangen der gemessenen Distanzen der Ultraschallsensoren.

        Wird ausgeführt, sobald der Server die Nachricht "distance" sendet.
        Übergibt die empfangenen Distanzen an die UI zum Anzeigen dieser.

        :param data: gemessene Distanzen
        :type data: Any

        :return: None
        """

        self._window.set_distance(data)

    def on_sensors_connected(self):
        """
        Funktion zum Initialisieren der UI, nachdem die Ultraschallsensoren verbunden wurden.

        Wird ausgeführt, sobald der Server die Nachricht "sensors_connected" sendet.

        :return: None
        """

        self._window.set_sensors_connected()

    def on_sensors_disconnected(self):
        """
        Funktion zum Aktualisieren der UI, nachdem die Verbindung mit den Ultraschallsensoren getrennt wurde.

        Wird ausgeführt, sobald der Server die Nachricht "sensors_disconnected" sendet.

        :return: None
        """

        self._window.set_sensors_disconnected()
