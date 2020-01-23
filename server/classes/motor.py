import pigpio
from time import sleep
from collections import deque
from classes.pins import Pins


class StepMotor:
    def __init__(self):
        # if not isinstance(pi, pigpio.pi):
        #     raise TypeError("Daemon not started")
        self.pi = pigpio.pi()
        for pin in Pins.Motor.OUTPUT:
            self.pi.write(pin, pigpio.OUTPUT)
        for pin in Pins.Motor.STEPS:
            self.pi.set_mode(pin, pigpio.OUTPUT)
        self.deque = deque(Pins.Motor.SEQUENCE)
        self.__delay = None

    def set_frequency(self, freq):
        if 0 < freq < 1500:
            self.__delay = 1.0 / freq

    def rotate_counterclockwise(self):
        self.deque.rotate(-1)
        self.step(self.deque[0])

    def rotate_clockwise(self):
        self.deque.rotate(1)
        self.step(self.deque[0])

    def step(self, step):
        for index, pin in enumerate(Pins.Motor.STEPS):
            self.pi.write(pin, step[index])
        sleep(self.__delay)

    def disable(self):
        for pin in Pins.Motor.STEPS:
            self.pi.write(pin, 0)
