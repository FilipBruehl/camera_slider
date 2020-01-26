import time
from RPi import GPIO


class HcSr04:
    """
    Klasse HcSr04 für die Kommunikation mit einem Ultraschallsensor
    """

    def __init__(self, trigger_pin: int, echo_pin: int):
        """
        Konstruktor der Klasse HcSr04.

        Stellt die GPIO-Pins für die Verwendung des Ultraschallsensors ein.
        Instanziiert notwendige Variablen für die Verwendung des Sensors.

        :param trigger_pin: Trigger-Pin für den Sensor
        :type trigger_pin: int
        :param echo_pin: Echo-Pin für den Sensor
        :type echo_pin: int
        """

        self.trigger_pin = trigger_pin                                                                                  # Speichert den übergebenen trigger_pin
        self.echo_pin = echo_pin                                                                                        # Speichert den übergebenen echo_pin
        self._distance = 0.0                                                                                            # Varioble für die gemessene Distanz mit 0 initialisieren
        self._last_measure_time = time.monotonic()                                                                      # Variable für den timestamp der letzen Messung initialisieren
        self._delay = 0.06                                                                                              # Variable für den Delay zwischen den Messungen mit 0.06 Sekunden initalisieren

        GPIO.setwarnings(False)                                                                                         # Deaktiviert die GPIO Warnungen
        GPIO.setmode(GPIO.BCM)                                                                                          # Weist GPIO an, die GPIO Pinnummerierung zu nutzen
        GPIO.setup(self.trigger_pin, GPIO.OUT)                                                                          # Trigger-Pin als Ausgang erstellen
        GPIO.setup(self.echo_pin, GPIO.IN)                                                                              # Echo-Pin als Eingang erstellen

    def _measure_distance(self) -> float:
        """
        Private Funktion zum Messen der Distanz.

        Überprüft zuerst, ob seit der letzten Messung genug Zeit vergangen ist.
        Schickt über den Trigger-Pin ein kurzes Signal, welches das Echo des Sensors startet.
        Die Funktion speichert die Zeit, wann das Trigger-Signal geschickt wurde und lauscht dann auf dem Echo-Pin, bis dort ein Signal empfangen wird.
        Die Zeit des Empfangs des Echo-Signals wird gespeichert.
        Aus der zeitlicnen Differenz zwischen dem Empfang des Echos und dem Senden des Triggers wird anschließend die Distanz berechnet.

        :return: Gemessene Distanz
        :rtype: float
        """

        if (time.monotonic() - self._last_measure_time) > self._delay:
            GPIO.output(self.trigger_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, False)

            start_time = time.monotonic()
            stop_time = time.monotonic()
            self._last_measure_time = time.monotonic()

            while GPIO.input(self.echo_pin) == 0:
                start_time = time.monotonic()

            while GPIO.input(self.echo_pin) == 1:
                stop_time = time.monotonic()

            time_delta = stop_time - start_time

            self._distance = time_delta / 0.000058

            return round(self._distance, 2)

    def measure(self, *, samples: int = 1) -> None:
        """
        Öffentliche Funktion zum Messen der Distanz.

        Die Funktion nimmt einen Parameter "samples" entgegen, welcher angibt, wie viele Messungen durchgeführt werden sollen.
        Sollte der Samples-Parameter nicht übergeben werden oder die Anzahl 1 betragen, wird nur eine einzige Messung durchgeführt.
        Sollte der Samples-Parameter größer als 1 sein, werden so viele Messungen gemacht, wie im Parameter stehen und anschließend wird der Mittelwert der Messungen berechnet.
        Die berechnete Distanz wird anschließend in der Variable "_distance" gespeichert.

        :param samples: Anzahl der Messungen
        :type samples: int

        :return: None
        """

        if samples < 2:
            self._distance = self._measure_distance()
        else:
            result = 0
            samples_taken = 0
            for _ in range(0, samples):
                echo = self._measure_distance()
                if echo > 0:
                    result += echo
                    samples_taken += 1
                time.sleep(self._delay)
            if samples_taken > 0:
                self._distance = round((result / samples_taken), 2)

    def get_distance(self) -> float:
        """
        Getter für die Distanz.

        :return: Gemessene Distanz
        :rtype: float
        """

        return round(self._distance, 2)

    @staticmethod
    def stop() -> None:
        """
        Statische Methode zum Deaktivieren des Sensors und Zurücksetzen der GPIO-Pins.

        :return: None
        """

        GPIO.cleanup()
