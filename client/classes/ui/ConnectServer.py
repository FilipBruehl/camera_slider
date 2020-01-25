from ipaddress import ip_address
from PyQt5.QtWidgets import QDialog
from classes.ui.designer.connect_server import Ui_Dialog


class ConnectServer(QDialog):
    """
    QDialog-Fenster zum Eingeben der IP-Adresse des Servers.
    """

    def __init__(self):
        """
        Konstruktor der Klasse ConnectServer.

        Erstellt das User Interface und weißt einzelnen UI-Elementen Listener und Callback-Methoden zu.
        """

        super().__init__()                                                                                              # Ruft Konstruktor der vererbenden Klasse QDialog auf
        self._ui = Ui_Dialog()                                                                                          # Erstelle Instanz der vom Designer erstellten GUI-Klasse
        self._ui.setupUi(self)                                                                                          # Erstellen des generierten UIs
        self._ui.pushButton_ok.clicked.connect(self.terminate)                                                          # Weise dem Button "pushButton_ok" die Funktion "terminate" als Callback-Funktion für den OnClickListener zu
        self._ui.lineEdit_ip.textEdited.connect(self.check_input)                                                       # Weise dem TextFeld "lineEdit_ip" die Funktion "check_input" Callback-Funktion für den TextEditedListener zu

    def terminate(self) -> None:
        """
        Methode zum Schließen des Fensters.

        Überprüft, ob ein Inhalt im Eingebefeld der IP-Adresse steht und terminiert.
        Falls nicht wird visuell auf das Fehlen der Eingabe hingewiesen.

        :return: None
        """

        if self._ui.lineEdit_ip.text():                                                                                 # Überprüft, ob im Eingabefeld der IP-Adresse Inhalt steht
            self.close()                                                                                                #   -> Schließe das Fenster
        else:                                                                                                           # Falls keine Eingabe im Feld steht
            self.no_input()                                                                                             #   -> Zeige einen Fehler an

    def check_input(self, input: str) -> None:
        """
        Überprüft, ob die Eingabe des Textfeldes eine valide IP-Adresse ist.

        Falls eine valide IP-Adresse eingegeben wurde, wird dem Nutzer eine positive visuelle Rückmeldung gegeben.
        Falls nicht wird visuell auf die fehlerhafte Eingabe hingewiesen.

        :param input: Eingabe des Textfeldes
        :type input: str

        :return: None
        """

        try:
            ip_address(input)                                                                                           # Überprüfe die Eingabe auf eine valide IP-Adresse. Verursacht eine Exception, falls eine falsche Eingabe stattgefunden hat
            self._ui.lineEdit_ip.setProperty("valid", True)                                                             # Setze die Property "valid" des Textfeldes auf True
            self._ui.lineEdit_ip.style().unpolish(self._ui.lineEdit_ip)                                                 # Lade die Styles des Textfeldes neu, um auf die Veränderung der Property zu reagieren
            self._ui.lineEdit_ip.style().polish(self._ui.lineEdit_ip)                                                   # -
            self._ui.lineEdit_ip.update()                                                                               # -
            self._ui.pushButton_ok.setEnabled(True)                                                                     # Aktiviere den Button zum Bestätigen der Eingabe
        except:                                                                                                         # Fange die potentielle Exception der Funktion "ip_address" ab, um auf eine falsche Eingabe zu reagieren
            self.no_input()                                                                                             #   -> Zeige einen Fehler an

    def no_input(self) -> None:
        """
        Zeigt visuell einen Fehler bei falscher Eingabe an.

        Der Button zum Bestätigen der Eingabe wird deaktiviert und das Eingabefeld wird rot umrandet.

        :return: None
        """

        self._ui.pushButton_ok.setDisabled(True)                                                                        # Deaktiviere den Button zum Bestätigen der Eingabe
        self._ui.lineEdit_ip.setProperty("valid", False)                                                                # Setze die Property "valid" des Textfeldes auf False
        self._ui.lineEdit_ip.style().unpolish(self._ui.lineEdit_ip)                                                     # Lade die Styles des Textfeldes neu, um auf die Veränderung der Property zu reagieren
        self._ui.lineEdit_ip.style().polish(self._ui.lineEdit_ip)                                                       # -
        self._ui.lineEdit_ip.update()                                                                                   # -

    @staticmethod
    def get_ip() -> str:
        """
        Statische Methode zum Erstellen des Fenster mit Rückgabe der eingegebenen IP-Adresse.

        :return: Eingegebene IP-Adresse
        :rtype: str
        """

        dialog = ConnectServer()                                                                                        # Erstelle eine Instanz der Klasse ConnectServer
        dialog.exec_()                                                                                                  # Führe die Instanz aus
        return dialog._ui.lineEdit_ip.text()                                                                            # Gib die eingegebene IP-Adresse zurück
