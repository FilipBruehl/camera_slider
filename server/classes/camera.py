import gphoto2 as gp
import subprocess
import os
import signal
from typing import Dict


class Camera:
    """
    Klasse Camera zur Kommunikation und Konfiguration einer angeschlossenen Spiegelreflexkamera.
    """

    # Öffentliche statische Variable, in der die verfügbaren Kameras gespeichert werden
    available_cameras = None

    @staticmethod
    def kill_gphoto_process() -> None:
        """
        Statische Funktion zum Beenden eines laufenden gphoto2 Prozesses.

        Dies ist notwendig, da es zu Fehlern kommt, wenn bereits ein gphoto2 Prozess läuft und ein neuer gestartet wird.

        :return: None
        """

        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, error = p.communicate()

        for line in out.splitlines():
            if b'gvfsd-gphoto2' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    @staticmethod
    def get_available_cameras() -> gp.CameraList:
        """
        Statische Funktion zum Auslesen der angeschlossenen und verfügbaren Kameras am Gerät.

        :return: Verfügbare Kameras
        :rtype: gp.CameraList
        """

        if hasattr(gp, 'gp_camera_autodetect'):
            Camera.available_cameras = gp.check_result(gp.gp_camera_autodetect())
        return Camera.available_cameras

    def __init__(self, index):
        """
        Konstruktor der Klasse Camera.

        Beendet alle laufenden gphoto2 Prozesse.
        Nimmt einen Index entgegen und erstellt mit diesem aus der Liste der verfügbaren Kameras die ausgewählte Kamera.
        Weist die Kamera zum Schluss an, die aufgenommen Bilder auf der SD-Karte zu speichern.

        :param index: Index der ausgewählten Kamera.
        :rtype: int
        """

        self.index = index                                                                                              # Speichere den übergebenen Index
        Camera.kill_gphoto_process()                                                                                    # Beende alle laufenden gphoto2 Prozesse

        self.name, self.addr = Camera.available_cameras[index]                                                          # Entnehme den Namen und den Port der gewählten Kamera aus der Liste der verfügbaren Kameras
        self.camera = gp.Camera()                                                                                       # Erstelle ein neues Objekt vom Typ "gp.Camera"

        port_info_list = gp.PortInfoList()                                                                              # Lese die verfügbaren Ports (Usb) aus
        port_info_list.load()                                                                                           # Lade die Liste der Usb-Ports
        idx = port_info_list.lookup_path(self.addr)                                                                     # Lade den Pfad der Kamera aus der Liste
        self.camera.set_port_info(port_info_list[idx])                                                                  # Setze den Port des erstellen Kamera-Objektes auf den geladenen Pfad
        self.camera.init()                                                                                              # Initialisiere die Kamera

        self.set_capture_target()                                                                                       # Weise die Kamera an, Bilder auf der SD KArte zu speichern
        print("Kamera initialisiert")

    def take_picture(self) -> gp.CameraFilePath:
        """
        Funktion zum Aufnehmen eines Bildes.

        :return: Der Pfad zum aufgenommenen Bild auf der Kamera.
        :rtype: gp.CameraFilePath
        """
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        return file_path

    def set_capture_target(self) -> None:
        """
        Funktion zum Speichern der Bilder auf der SD-Karte.

        Liest die aktuelle Konfiguration für den Speicherort aus und überschreibt diese mit der SD-Karte als neuer Speicherort.
        Dies ist notwendig, da standardmäßig der interne-RAM der Kamera als Speicherort festgelegt ist, sobald eine USB-Verbindung vorhanden ist.

        :return: None
        """

        config = self.camera.get_config()                                                                               # Lädt die Konfiguration der Kamera
        capture_target = config.get_child_by_name('capturetarget')                                                      # Lädt die Einstellung zum Speicherort aus der geladenen Konfiguration
        choice = capture_target.get_choice(1)                                                                           # Speichere die SD-Karte als neuen Speicherort
        capture_target.set_value(choice)                                                                                # Schreibe die SD-Karten Einstellung in die Konfiguration
        self.camera.set_config(config)                                                                                  # Speichere die Konfiguration in der Kamera

    def get_information(self) -> Dict:
        """
        Funktion gibt die Konfiguration der Kamera zurück.

        :return: Konfiguration der Kamera
        :rtype: dict
        """

        return {
            'name': self.name,
            'battery': self.get_battery().get_value(),
            'focal': self.get_focal().get_value(),
            'shutter': self.get_shutter_speed().get_value(),
            'iso': self.get_iso().get_value(),
            'focus': self.get_focus().get_value(),
            'quality': self.get_image_quality().get_value()
        }

    def get_options(self) -> Dict:
        """
        Funktion zum zurückgeben der verfügbaren Einstellungsmöglichkeiten der Kamera.

        :return: Einstellungsmöglichkeiten der Kamera
        :rtype: dict
        """

        focal = self.get_focal()
        shutter = self.get_shutter_speed()
        iso = self.get_iso()
        return {
            'focal': [f for f in focal.get_choices()],
            'shutter': [s for s in shutter.get_choices()],
            'iso': [i for i in iso.get_choices()]
        }

    def list_config(self) -> None:
        """
        Funktion zum Auflisten der Kamera-Konfiguration.

        :return: None
        """

        config = self.camera.list_config()
        for con in config:
            print(con)

    def get_shutter_speed(self) -> gp.CameraWidget:
        """
        Funktion liest die Verschlusszeit aus und gibt diese zurück.

        :return: Objekt mit Informationen der Verschlusszeit
        :rtype: gp.CameraWidget
        """

        config = self.camera.get_config()
        shutter_speed = config.get_child_by_name('shutterspeed2')
        return shutter_speed

    def set_shutter_speed(self, value: str) -> None:
        """
        Funktion zum Setzen einer neuen Verschlusszeit.

        :param value: neue Verschluszeit
        :type value: str

        :return: None
        """

        config = self.camera.get_config()
        shutter_speed = config.get_child_by_name('shutterspeed2')
        shutter_speed.set_value(str(value))
        self.camera.set_config(config)

    def get_battery(self):
        """
        Funktion zum Auslesen des Batteriestatus.

        :return: Objekt mit Informationen zum Akkustatus
        :rtype: gp.CameraWidget
        """

        config = self.camera.get_config()
        battery = config.get_child_by_name('batterylevel')
        return battery

    def get_focal(self) -> gp.CameraWidget:
        """
        Funktion liest die Blende aus und gibt diese zurück.

        :return: Objekt mit Informationen der Blende
        :rtype: gp.CameraWidget
        """

        config = self.camera.get_config()
        focal = config.get_child_by_name('f-number')
        return focal

    def set_focal(self, value: str) -> None:
        """
        Funktion zum Setzen einer neuen Blende.

        :param value: neue Blende
        :type value: str

        :return: None
        """

        config = self.camera.get_config()
        focal = config.get_child_by_name('f-number')
        focal.set_value(str(value))
        self.camera.set_config(config)

    def get_focus(self) -> gp.CameraWidget:
        """
        Funktion liest den Fokustyp aus und gibt diese zurück.

        :return: Objekt mit Informationen zum Fokus
        :rtype: gp.CameraWidget
        """

        config = self.camera.get_config()
        fm = config.get_child_by_name('focusmode')
        return fm

    def get_image_quality(self) -> gp.CameraWidget:
        """
        Funktion liest die Bildqualität aus und gibt diese zurück.

        :return: Objekt mit Informationen zur Bildqualität
        :rtype: gp.CameraWidget
        """

        config = self.camera.get_config()
        qual = config.get_child_by_name('imagequality')
        return qual

    def get_iso(self) -> gp.CameraWidget:
        """
        Funktion liest den ISO-Wert aus und gibt diese zurück.

        :return: Objekt mit Informationen zum ISO
        :rtype: gp.CameraWidget
        """

        config = self.camera.get_config()
        iso = config.get_child_by_name('iso')
        return iso

    def set_iso(self, value: str) -> None:
        """
        Funktion zum Setzen eines neuen ISO-Wertes.

        :param value: neuer ISO-Wert
        :type value: str

        :return: None
        """

        config = self.camera.get_config()
        iso = config.get_child_by_name('iso')
        iso.set_value(str(value))
        self.camera.set_config(config)

    def exit(self):
        """
        Funktion zum Deaktivieren der Kamera.
        :return:
        """
        self.camera.exit()
        self.camera = None
