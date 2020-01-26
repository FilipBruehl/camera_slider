import pigpio
from time import sleep
from collections import deque
from typing import List
from classes.pins import Pins


class SchrittMotor:
    """
    Klasse SchrittMotor dient zum Ansteuern eines 17HS4401S Schrittmotors.
    """

    def __init__(self):
        """
        Konstruktor der Klasse SchrittMotor.

        Initialisiert die notwendigen Pins am Raspberry und die Schrittsequenz.
        """

        self.pi = pigpio.pi()
        for pin in Pins.Motor.OUTPUT:
            self.pi.write(pin, pigpio.OUTPUT)
        for pin in Pins.Motor.STEPS:
            self.pi.set_mode(pin, pigpio.OUTPUT)
        self.deque = deque(Pins.Motor.SEQUENCE)
        self._delay = None

    def set_frequency(self, freq: int) -> None:
        """
        Funktion zum Setzen der Frequenz des Motors.

        :param freq: Frequenz in Schritten pro Sekunde
        :type freq: int

        :return: None
        """

        if 0 < freq < 1500:
            self._delay = 1.0 / freq

    def rotate_counterclockwise(self) -> None:
        """
        Funktion zum Rotieren des Motors einen Schritt gegen den Uhrzeigersinn.

        Geht einen Schritt in der Deque mit der Schrittsequenz zurück.
        Ruft dann die Funktion zum Drehen des Motors mit dem aktuellen Schritt auf.

        :return: None
        """

        self.deque.rotate(-1)
        self.step(self.deque[0])

    def rotate_clockwise(self) -> None:
        """
        Funktion zum Rotieren des Motors einen Schritt im Uhrzeigersinn.

        Geht einen Schritt in der Deque mit der Schrittsequenz vor.
        Ruft dann die Funktion zum Drehen des Motors mit dem aktuellen Schritt auf.

        :return: None
        """

        self.deque.rotate(1)
        self.step(self.deque[0])

    def step(self, step: List) -> None:
        """
        Funktion zum Bewegen des Schrittmotors um einen Schritt.

        Iteriert über die einzelnen Pole bzw. Pins des Motors und weist jedem ihren jeweiligen Schritt aus der Sequenz zu.

        :param step: Schrittsequenz für die Pins
        :type step: list

        :return: None
        """

        for index, pin in enumerate(Pins.Motor.STEPS):
            self.pi.write(pin, step[index])
        sleep(self._delay)

    def disable(self) -> None:
        """
        Funktion zum Deaktivieren des Motors.

        Iteriert über alle Pins und deaktiviert die Ausgänge.

        :return: None
        """

        for pin in Pins.Motor.STEPS:
            self.pi.write(pin, 0)
