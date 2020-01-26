import socket
import pickle
import sys
from threading import Thread
from time import sleep
from typing import Any, Dict
from classes.camera import Camera
from classes.motor import StepMotor
from classes.hc_sr04 import HcSr04
from classes.pins import Pins


class Server:
    """
    Server für die Kommunikation mit dem Client und allen angeschlossenen Geräten.

    Kümmert sich um die Steuerung des Schrittmotors, der Ultraschallsensoren und der Kamera.
    """

    def __init__(self):
        """
        Konstruktor der Klasse Server.

        Erstellt den Socket für die Netzwerk-Kommunikation.
        Initialisiert die für den Server notwendigen Einstellugnen und Variablen
        """
        self.port = 50007                                                                                               # Initialisiere den Host-Port auf 50007
        self.ip = ""                                                                                                    # Initialisiere die Host-IP auf einen leeren String
        self.header_size = 10                                                                                           # Setze die Header Größe auf 10 fest
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                 # Erstelle einen neuen TCP/IPv4 Socket
        self.socket.bind((self.ip, self.port))                                                                          # Startet den Socket und bindet ihn an die eigene IP und den festgelegten Port
        self.conn, self.conn_ip, self.conn_port = None, None, None                                                      # Initialisiere die Variablen für die spätere Verbindung mit dem Client mit None
        self.exit = False                                                                                               # Variable "exit" als Abbruchbedingung für die Threads mit False initialisieren
        self.thread_recv = Thread(target=self.receive)                                                                  # Erstelle einen neuen Thread mit der Funktion "receive" als Ziel
        self.camera_selected = None                                                                                     # Initialisiere Variable mit None
        self.pictures_to_take = None                                                                                    # -
        self.motor = None                                                                                               # -
        self.motor_running = False                                                                                      # Initialisiere Variable mit False
        self.motor_data = None                                                                                          # Initialisiere Variable mit None
        self.hc_sr04_left = None                                                                                        # -
        self.hc_sr04_right = None                                                                                       # -

    def run(self) -> None:
        """
        Funktion zum Starten des Servers und einrichten einer eingehenden Verbindung.

        Server wartet auf eine eingehende Verbindung des Clients und startet anschließend den Thread zum Empfangen von Nachrichten.

        :return: None
        """

        self.socket.listen(1)                                                                                           # Warte auf eine eingehende Verbindung
        print("Server gestartet")
        self.conn, (self.conn_ip, self.conn_port) = self.socket.accept()                                                # Akzeptiere die eingehende Verbindung und speichere diese mit der dazugehörigen IP und dem Port
        print(f"{self.conn_ip} verbunden")
        try:
            self.thread_recv.start()                                                                                    # Starte den Thread zum Empfangen von Nachrichten
        except:
            pass

    def stop(self) -> None:
        """
        Funktion zum Beenden des Servers.

        Falls noch eine aktive Verbindung zum Client besteht wird diese beendet.
        Beendet anschließend den ausgehenden Socket und das Programm.

        :return: None
        """

        if self.conn:
            self.on_disconnect_client()
        self.socket.close()
        sys.exit()

    def receive(self) -> None:
        """
        Funktion zum Empfangen von Nachrichten und Daten vom Client.

        Die Funktion läuft in einer while-Schleife, um so kontinuirlich Daten zu empfangen.

        Empfängt vom Client nacheinander 2 (falls keine Daten vorhanden sind) bzw. 3 (falls Daten vorhanden sind) Nachrichten:
        1.) 10 Byte großer Header, der die Größe des nachfolgenden Befehls-Objekts beinhaltet.
        2.) Befehels-Objekt mit variabler Größe. Beinhaltet einen 10 Byte-Header mit der Größe des nachfolgenden Daten-Objekts, falls vorhanden, und den Befehl des Clients.
        3.) Das Daten-Objekt mit variabler Größe, falls vorhanden.

        Die empfangenen Nachrichten werden anschließend dekodiert, in ihren ursprünglichen Datentyp umgewandelt und zu einer Nachricht zusammengefügt.
        Die zusammengefügte Nachricht wird zur Weiterverarbeitung durch den Server an eine separate Funktion übergeben.

        Durch das separate Empfangen von Befehl und Daten mit einem jeweiligen Header kann gewährleistet werden, dass Befehl und Daten mit unterschiedlicher Größe ordnungsgemäß empfangen werden.

        :return: None
        """

        command = None
        command_len = None
        data = None
        data_len = None

        while not self.exit:                                                                                            # Dauerschleife, während "_connected" True ist
            try:
                command_len = self.socket.recv(self.header_size)                                                        # Empfange den ersten 10 Byte großen Header
                command_len = int(command_len.decode().strip())                                                         # Dekodiere den Header und konvertiere ihn in einen int
                if command_len > 0:                                                                                     # Überprüfe, ob der Header größer als 0 ist
                    command = self.socket.recv(command_len)                                                             # -> Empfange das Befehls-Objekt mit der im Header angegebenen Größe
                    data_len = int(command[:self.header_size].decode().strip())                                         # -> Extrahiere aus dem Befehls-Objekt den 10 Byte großen Header für das Datenobjekt, dekodiere diesen und wandle ihn in einen int um
                    command = command[self.header_size:]                                                                # -> Extrahiere aus dem Befehls-Objekt den Befehls-Teil
                    command = pickle.loads(command)                                                                     # -> Dekodiere den Befehl
                    if data_len > 0:                                                                                    # Überprüfe, ob der Daten-Header größer als 0 ist
                        data = self.socket.recv(data_len)                                                               # -> Empfange das Daten-Objekt
                        data = pickle.loads(data)                                                                       # -> Dekodiere das Daten-Objekt
                print(
                    f"message received. command_len = {command_len}, command = {command}, data_len = {data_len}, data = {data}")
                self.handle_command(command, data)                                                                      # Übergebe den Befehl und die Daten an eine separate Funktion zur weiteren Verarbeitung
            except Exception as e:                                                                                      # Falls ein Fehler auftritt
                print(e)                                                                                                # -> Gebe den Fehler in der Konsole aus
            finally:
                command = None
                command_len = None
                data = None
                data_len = None

    def send(self, command: str, data : Any = None) -> None:
        """
        Funktion zum Senden von Befehlen und Daten an den Client.

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
                data = pickle.dumps(data)                                                                               # -> Konvertiere die übergebenen Daten in ein Byte-Objekt
                data_len = bytes(f"{len(data):<{self.header_size}}", 'utf-8')                                           # -> Ersetlle einen 10 Byte großen Header mit der Größe des Daten-Objekts als Inhalt
            else:                                                                                                       # Falls keine Daten übergeben wurden
                data_len = bytes(f"{0:<{self.header_size}}", 'utf-8')                                                   # -> Erstelle einen 10 Byte großen Header mit 0 als Größe des Daten-Objektes als Inhalt
            command = pickle.dumps(command)                                                                             # Konvertiere den Befehl in ein Byte-Objekt
            command = data_len + command                                                                                # Der Daten-Header wird dem Befehl im Befehls-Objekt vorangestellt
            command_len = bytes(f"{len(command):<{self.header_size}}", 'utf-8')                                         # Erstelle einen 10 Byte großen Header mit der Größe des Befehls-Objekts als Inhalt
            self.socket.send(command_len)                                                                               # Verschicke den Befehls-Header
            self.socket.send(command)                                                                                   # Verschicke das Befehls-Objekt
            if data:                                                                                                    # Falls Daten übergeben wurden
                self.socket.send(data)                                                                                  # -> Schicke das Daten-Objekt
            print(
                f"message send. command_len = {command_len}, command = {command}, data_len = {data_len}, data = {data}")
        except Exception as e:                                                                                          # Falls ein Fehler auftritt
            print(e)                                                                                                    #   -> Fehler wird in der Konsole ausgegeben

    def handle_command(self, command: str, data : Any = None) -> None:
        """
        Funktion zum verarbeiten der empfangenen Befehle und Daten.

        Es wird der übergebene Befehl mit zu erwartenden Befehlen verglichen und bei Übereinstimmung eine entsprechende Funktion zum ausführen des Befehls aufgerufen.

        :param command: übergebener Befehl
        :param data: übergebene Daten, falls vorhanden
        :type command: str
        :type data: Any

        :return: None
        """

        if command == "connect_camera":
            self.on_connect_camera(data)
        elif command == "get_camera_options":
            self.on_get_camera_options()
        elif command == "disconnect_camera":
            self.on_disconnect_camera()
        elif command == "disconnect_client":
            self.on_disconnect_client()
        elif command == "connect_motor":
            self.on_connect_motor()
        elif command == "disconnect_motor":
            self.on_disconnect_motor()
        elif command == "connect_sensors":
            self.on_connect_sensors()
        elif command == "disconnect_sensors":
            self.on_disconnect_sensors()
        elif command == "set_slider_settings":
            self.on_set_slider_settings(data)
        elif command == "set_slider_settings_manual":
            self.on_set_slider_settings_manual(data)
        elif command == "set_camera_settings":
            self.on_set_camera_settings(data)
        elif command == "set_camera_settings_takes":
            self.on_set_camera_settings_takes(data)
        elif command == "take_picture":
            self.on_take_picture()
        elif command == "start_slider":
            self.on_start_slider()
        elif command == "measure_distance":
            self.measure_distance()
        elif command == "position_slider":
            self.on_position_slider(data)

    def on_connect_camera(self, data: int) -> None:
        """
        Funktion zum Verbinden mit einer angeschlossenen Kamera.

        Wird ausgeführt, sobald der Client die Nachricht "connect_camera" sendet.
        Funktion liest zuerst alle Verfügbaren Kameras aus.
        Sofern eine oder mehrere Kameras verfügbar sind und noch keine Kamera verbunden ist wird die Kamera des übetrragenenen Indizes verbundne.
        Sollte keine Kamera verfügbar sein, wird dem Client eine Fehlermeldung zurück geschickt.

        :param data: Index der zu verbindenden Kamera
        :type data: int

        :return: None
        """

        cameras = Camera.get_available_cameras()
        if cameras:
            if not self.camera_selected:
                self.camera_selected = Camera(data)
            self.send('camera_init', self.camera_selected.get_information())
        else:
            self.send('camera_not_available')

    def on_get_camera_options(self) -> None:
        """
        Funktion zum Versenden der verfügbaren Kamera Einstellungsmöglichkeiten.

        Wird ausgeführt, sobald der Client die Nachricht "get_camera_options" sendet.
        Liest von der verbundenen Kamera die verfügbaren Einstellungsmöglichkeiten aus.
        Anschließend werden diese an den Client gesendet.

        :return: None
        """

        options = self.camera_selected.get_options()
        self.send('camera_options', options)

    def on_disconnect_camera(self) -> None:
        """
        Funktion zum Trennen der Verbindung mit der Kamera.

        Wird ausgeführt, sobald der Client die Nachricht "disconnect_camera" sendet.
        Beendet die Verbindung mit der Kamera und schickt eine Meldung an den Client.

        :return: None
        """

        self.camera_selected.exit()
        self.camera_selected = None
        self.send('camera_disconnected')

    def on_disconnect_client(self) -> None:
        """
        Fnktion zum Trennen der Verbindung mit dem Client.

        Wird ausgeführt, sobald der Client die Nachricht "disconnect_client" sendet.
        Sendet dem Client eine Bestätigung, dass die Verbindung getrennt wird.
        Anschließend wird der Socket geschlossen und die Abbruchbedingung für die Threads auf True gesetzt.
        Dadurch terminieren die Threads und der Server beendet sich.

        :return: None
        """

        print(f"{self.conn_ip} hat die Verbindung getrennt")
        self.send("disconnect")
        sleep(0.5)
        self.exit = True
        self.conn.close()

    def on_connect_motor(self) -> None:
        """
        Funktion zum Verbinden des Schrittmotors.

        Wird ausgeführt, sobald der Server die Nachricht "connect_motor" sendet.
        Instanziiert einen neuen Schrittmotor und schickt dem Client eine Bestätigugn.

        :return: None
        """

        self.motor = StepMotor()
        self.send('motor_connected')

    def on_disconnect_motor(self) -> None:
        """
        Funktion zum Trennen der Verbindung mit dem Schrittmotor.

        Wird ausgeführt, sobald der Client die Nachricht "disconnect_motor" sendet.
        Deaktiviert den Schrittmotor, setzt die Verbindung zurück und sendet dem Client eine Bestätigung.

        :return: None
        """

        self.motor.disable()
        self.motor = None
        self.send('motor_disconnected')

    def on_connect_sensors(self) -> None:
        """
        Funktion zum Verbinden der Ultraschallsensoren.

        Wird ausgeführt, sobald der Client die Nachricht "connect_sensors" sendet.
        Stellt zuerst eine Verbindung mit den zwei Ultraschallsensoren (links, rechts) her.
        Sendet eine Bestätigung, dass die Sensoren verbunden wurden.
        Misst zum Schluß die Abstände der beiden Sensoren.

        :return: None
        """

        self.hc_sr04_left = HcSr04(Pins.Ultrasonic.LEFT_TRIGGER, Pins.Ultrasonic.LEFT_ECHO)
        self.hc_sr04_right = HcSr04(Pins.Ultrasonic.RIGHT_TRIGGER, Pins.Ultrasonic.RIGHT_ECHO)
        self.send('sensors_connected')
        sleep(0.1)
        self.measure_distance()

    def on_disconnect_sensors(self) -> None:
        """
        Funktion zum Beenden der Verbindung mit den Ultraschallsensoren.

        Wird ausgeführt, sobald der Client die Nachricht "disconnect_sensors" sendet.
        Deaktiviert zuerst die beiden Sensoren, setzt die Verbindung zurück und sendet eine Besätigung.

        :return: None
        """

        self.hc_sr04_left.stop()
        self.hc_sr04_right.stop()
        self.hc_sr04_left = None
        self.hc_sr04_right = None
        self.send('sensors_disconnected')

    def on_set_slider_settings(self, data: Dict) -> None:
        """
        Funktion zum Setzen der Slider-Einstellungen.

        Wird ausgeführt, sobald der Client die Nachricht "set_slider_settings" sendet.
        Speichert die Einstellungen in einer Variable, setzt die Frequenz des Motors und sendet eine Bestätigung.

        :param data: Einstellungen des Sliders
        :type data: dict

        :return: None
        """

        self.motor_data = data
        self.motor.set_frequency(int(self.motor_data['frequency']))
        self.send('slider_settings_set', data)

    def on_set_slider_settings_manual(self, data: Dict) -> None:
        """
        Funktion zum manuellen positionieren des Sliders.

        Wird ausgeführt, sobald der Client die Nachricht "set_slider_settings_manual" sendet.
        Erstellt zwei neue Threads. Einen Thread mit der Funktion "move_manual" als Ziel, um den Slider zu positionieren.
        Der Zweite Thread mit der Funktion "measure_distance_thread" als Ziel dient zum kontinuirlichen Messen der Abstände.
        Vor dem Starten wird an den Client gesendet, dass der Slider gestartet wurde.
        Nach erfolgreichem Beenden der Threads wird die Nachricht, dass der Slider-Lauf beendet wurde, an den Client geschickt.

        :param data: Manuelle Einstellungen des Sliders
        :type data: dict

        :return: None
        """

        self.send('slider_started')
        thread_slider = Thread(target=self.move_manual, args=(data,))
        thread_distance = Thread(target=self.measure_distance_thread)
        thread_slider.start()
        sleep(0.1)
        thread_distance.start()
        thread_slider.join()
        thread_distance.join()
        self.send('slider_finished')

    def on_start_slider(self) -> None:
        """
        Funktion zum Starten des Slider-Laufs.

        Wird ausgeführt, sobald der Client die Nachricht "start_slider" sendet.
        Sendet zuerst eine Nachricht an den Client, dass der Slider gestartet wurde.
        Erstellt anschließend zwei Threads.
        Der erste, mit der Funktion "move_camera" als Ziel, dient zum Bewegen des Sliders.
        Der zweite, mit der Funktion "measure_distance_thread" als Ziel, dient zum kontinuirlichen Messen der Abstände.
        Sobald beide Threads terminiert sind wird an den Client die Nachricht gesendet, dass der Slider-Lauf beendet ist.

        :return: None
        """

        self.send('slider_started')
        thread_camera = Thread(target=self.move_camera)
        thread_distance = Thread(target=self.measure_distance_thread)
        thread_camera.start()
        sleep(0.1)
        thread_distance.start()
        thread_camera.join()
        thread_distance.join()
        self.send('slider_finished')

    def on_set_camera_settings(self, data: Dict) -> None:
        """
        Funktion zum Setzen der neuen Kamnera Einstellungen.

        Wird ausgeführt, sobald der Client die Nachricht "set_camera_settings" sendet.
        Stellt bei der verbundenen Kamera die gesendeten Optionen ein.
        Sendet anschließend die neuen Einstellungen an den Client zurück.

        :param data: neue Einstellungen der Kamera
        :type data: dict

        :return: None
        """

        self.camera_selected.set_focal(data['focal'])
        self.camera_selected.set_shutter_speed(data['shutter'])
        self.camera_selected.set_iso(data['iso'])
        self.send('camera_values', self.camera_selected.get_information())

    def on_set_camera_settings_takes(self, data: str) -> None:
        """
        Funktion zum Einstellen der zu tätigen Aufnamhen.

        Wird ausgeführt, sobald der Client die Nachricht "set_camera_settings_sendet".

        :param data: Anzahl der zu tätigen Aufnahmen
        :type data: str

        :return: None
        """

        self.pictures_to_take = int(data)

    def on_take_picture(self) -> None:
        """
        Funktion zum Aufnehmen eines einzelnen Bildes.

        Wird ausgefführt, sobald der Client die Nachricht "take_picture" sendet.

        :return: None
        """

        self.camera_selected.take_picture()

    def on_position_slider(self, data: str) -> None:
        """
        Funktion zum automatischen Positionieren des Sliders.

        Wird ausgeführt, sobald der Client die Nachricht "position_slider" sendet.
        Sendet zuerst an den Client, dass der Slider gestartet wurde.
        Erstellt anschließend zwei Threads.
        Der erste, mit der Funktion "position_slider" als Ziel, dient zum Bewegen/Positionieren des Sliders.
        Der zweite, mit der Funktion "measure_distance_thread" als Ziel, dient zum kontinuirlichen Messen der Abstände.
        Nachdem beide Threads terminiert haben wird an den Client gesendet, dass der Slider-lauf beendet ist.

        :param data: Einstellung zum Positionieren des Sliders.
        :type data: str

        :return: None
        """

        self.send('slider_started')
        thread_position = Thread(target=self.position_slider, args=(data,))
        thread_distance = Thread(target=self.measure_distance_thread)
        thread_position.start()
        sleep(0.2)
        thread_distance.start()
        thread_position.join()
        thread_distance.join()
        self.send('slider_finished')

    def position_slider(self, new_position: str) -> None:
        """
        Funktion zum automatischen Positioneren des Sliders.

        Misst zuerst die Abstände beider Sensoren und speichert diese.
        Berechnet anhand der neuen Zielposition den Abstand zu dieser und daraus die zu fahrenden Schritte für den Motor.
        Fährt den Slider anschließend zur neuen Position.

        :param new_position: Neue Position des Sliders
        :type new_position: str

        :return: None
        """

        self.motor.set_frequency(900)                                                                                   # Setzt die Frequenz des Motors
        self.measure_distance()                                                                                         # Misst die Entfernungen neu
        distance_left = self.hc_sr04_left.get_distance()                                                                # Speichert die Entfernung des linken Sensors
        distance_right = self.hc_sr04_right.get_distance()                                                              # Speichert die Entfernung des rechten Sensors
        rotate = None                                                                                                   # Initialisiert Variable mit None
        distance = None                                                                                                 # -
        self.motor_running = True                                                                                       # Setzt "motor_running" auf True (Für Ultraschallsensoren wichtig)
        if new_position == "Links":                                                                                     # Falls neue Position "Links" ist
            rotate = self.motor.rotate_counterclockwise                                                                 #   -> weise "rotate" die Funktion "rotate_counterclockwise" des Motors zu
            distance = distance_left - 5                                                                                #   -> Berechne die zu fahrende Distanz
        elif new_position == "Rechts":                                                                                  # Falls neue Position "Rechts" ist
            rotate = self.motor.rotate_clockwise                                                                        #   -> weise "rotate" die Funktion "rotate_clockwise" des Motors zu
            distance = distance_right - 5                                                                               #   -> Berechne die zu fahrende Distanz
        elif new_position == "Mitte":                                                                                   # Falls neue Position "Mitte" ist
            if distance_left > distance_right:                                                                          #   -> Überprüfe, ob der Abstand links größer ist als rechts
                rotate = self.motor.rotate_counterclockwise                                                             #       -> weise "rotate" die Funktion "rotate_counterclockwise" des Motors zu
                distance = (distance_left - distance_right) / 2                                                         #       -> Berechne die zu fahrende Distanz
            elif distance_left < distance_right:                                                                        #   -> Überprüfe, ob der Abstand links kleiner ist als rechts
                rotate = self.motor.rotate_clockwise                                                                    #       -> weise "rotate" die Funktion "rotate_clockwise" des Motors zu
                distance = (distance_right - distance_left) / 2                                                         #       -> Berechne die zu fahrende Distanz
        if distance > 0:                                                                                                # Überprüft, ob die berechnete Distanz größer 0 ist
            steps = int(distance / 4 * 200)                                                                             #   -> Berechnet aus der Distanz die zu fahrenden Schritte

            for _ in range(0, int(steps)):                                                                              # Rotiere für die Anzahl der berechneten Schritte
                rotate()                                                                                                # -

        self.motor_running = False                                                                                      # Setze "motor_running" auf False
        self.motor.disable()                                                                                            # Stoppe den Schrittmotor

    def move_camera(self) -> None:
        """
        Funktion zum Bewegen des Sliders mit Auslösen der Kamera.

        Überprüft, in welche Richtung der Motor drehen muss.
        Nimmt anschließend das erste Bild auf und berechnet, in welchen Abständen die weiteren Bilder aufzunehmen sind.
        Bewegt den Slider an die nächste Position und nimmt ein Bild auf.
        Wiederholt die Prozedur solange, bis alle Bilder aufgenommen sind.

        :return: None
        """

        rotate = self.motor.rotate_counterclockwise if self.motor_data['direction'] == "Links" else self.motor.rotate_clockwise     # Überprüft, in welche Richtung der Motor drehen soll
        self.motor_running = True                                                                                       # Setzt "motor_running" auf True
        self.camera_selected.take_picture()                                                                             # Nimmt ein Bild auf
        self.pictures_to_take -= 1                                                                                      # Dekrementiere die Anzahl, der aufzunehmenden Bilder um eins
        steps = (int(self.motor_data['distance']) / 4) * 200                                                            # Rechne die Distanz in Schritte um
        steps_per_cycle = int(steps)//self.pictures_to_take                                                             # Berechne, wie viele Schritte bis zum nächsten Bild zu machen sind
        for _ in range(self.pictures_to_take):                                                                          # Wiederholle Vorgang, bis alle Bilder aufgenommen sind
            for _ in range(steps_per_cycle):                                                                            #   -> Rotiere die berechnete Anzahl an Schritten
                rotate()                                                                                                #   -> -
            self.motor.disable()                                                                                        # Deaktiviere den Motor
            sleep(0.5)
            self.camera_selected.take_picture()                                                                         # Machen ein Bild
        self.motor_running = False                                                                                      # Setze "motor_running" auf False
        self.motor.disable()                                                                                            # Deaktiviere den Motor

    def move_manual(self, data: Dict) -> None:
        """
        Funktion bewegt den Slider in manuellen Schritten.

        Stellt zuerst die Frequenz des Motors ein.
        Übeprüft dann, in welche Richtung der Motor sich drehen muss und rotiert anschließend für die übertragene Anzahl an Schritten.
        Zum Schluss wird der Motor deaktiviert.

        :param data: manuelle Einstellungen des Sliders
        :type data: dict

        :return: None
        """

        self.motor.set_frequency(data['frequency'])
        rotate = self.motor.rotate_counterclockwise if data['direction'] == "Links" else self.motor.rotate_clockwise
        self.motor_running = True
        steps = int(data['distance'])
        for _ in range(steps):
            rotate()
        self.motor_running = False
        self.motor.disable()

    def measure_distance(self) -> None:
        """
        Funktion zum einmaligen Messen der Abstände der beiden Sensoren.

        Misst am linken und rechten Sensor die Abstönde.
        Anschließend werden die Messungen an den Client gesendet.

        :return: None
        """

        self.hc_sr04_left.measure(samples=5)
        self.hc_sr04_right.measure(samples=5)
        self.send('distance', data={'left': self.hc_sr04_left.get_distance(), 'right': self.hc_sr04_right.get_distance()})
        sleep(0.1)

    def measure_distance_thread(self) -> None:
        """
        Funktion zum kontinuirlichen Messen der Abstände, solange "motor_running" True ist.

        Misst am linken und rechten Sensor die Abstönde.
        Anschließend werden die Messungen an den Client gesendet.

        :return: None
        """

        while self.motor_running:
            self.hc_sr04_left.measure()
            self.hc_sr04_right.measure()
            print(f"Links: {self.hc_sr04_left.get_distance()} cm/ Rechts: {self.hc_sr04_right.get_distance()} cm")
            self.send('distance', data={'left': self.hc_sr04_left.get_distance(), 'right': self.hc_sr04_right.get_distance()})
            sleep(0.1)
