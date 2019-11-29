import pigpio
from time import sleep
from collections import deque
from os import system


class StepMotor:
    # slider length = 31cm
    # schlitten length = 5cm
    # drive distance = 31 - 5 = 27cm
    # steps/rotation = 200
    # s/rotation = 4 cm
    # full sequence = 1315 steps = 6.575 rotations

    output_pins = [25, 17]
    step_pins = [24, 23, 27, 22]
    step_sequene = [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1]
    ]

    def __init__(self):
        # if not isinstance(pi, pigpio.pi):
        #     raise TypeError("Daemon not started")
        self.pi = pigpio.pi()
        for pin in self.output_pins:
            self.pi.write(pin, pigpio.OUTPUT)
        for pin in self.step_pins:
            self.pi.set_mode(pin, pigpio.OUTPUT)
        self.deque = deque(self.step_sequene)
        self.__delay = None

    def set_frequence(self, freq):
        if 0 < freq < 1500:
            self.__delay = 1.0 / freq

    def rotate_counterclockwise(self):
        self.deque.rotate(-1)
        self.step(self.deque[0])

    def rotate_clockwise(self):
        self.deque.rotate(1)
        self.step(self.deque[0])

    def step(self, step):
        for index, pin in enumerate(self.step_pins):
            self.pi.write(pin, step[index])
        sleep(self.__delay)

    def disable(self):
        for pin in self.step_pins:
            self.pi.write(pin, 0)


if __name__ == "__main__":
    system("sudo systemctl disable pigpiod")
    sleep(0.5)
    system("sudo systemctl start pigpiod")
    print("Daemon started")

    # pi = pigpio.pi()
    # motor = StepMotor(pi)
    motor = StepMotor()
    motor.set_frequence(500)
    print("Rotating clockwise")
    for _ in range(1315):
        motor.rotate_clockwise()
    # print("Rotating counterclockwise")
    # for _ in range(2048):
    #     motor.rotate_counterclockwise()
    motor.disable()
    print("Finished")
