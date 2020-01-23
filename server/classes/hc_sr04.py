# Import necessary libraries.
import time
from RPi import GPIO
from Bluetin_Echo import Echo
from classes.pins import Pins

# Define GPIO pin constants.
# TRIGGER_PIN = 26
# ECHO_PIN = 19
# Initialise Sensor with pins, speed of sound.
# speed_of_sound = 343
# echo = Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound)
# Measure Distance 5 times, return average.
# samples = 5
# Take multiple measurements.
# for counter in range(0, 10):
#     result = echo.read('cm', samples)
    # Print result.
#     print(f"{result} cm. error: {echo.error_code}")

# Reset GPIO Pins.
# echo.stop()


class HcSr04:
    # speed_of_sound = 343
    #
    # def __init__(self, trigger, echo, samples):
    #     self.trigger = trigger
    #     self.echo = echo
    #     self.echo = Echo(self.trigger, self.echo)
    #     self.samples = samples
    #
    # def measure_distance(self):
    #     return round(self.echo.send(), 2)
    #
    # def stop(self):
    #     self.echo.stop()

    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self._distance = 0.0
        self._last_measure_time = time.monotonic()
        self._delay = 0.06

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def _measure_distance(self, format="cm"):
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

            if format == "cm":
                self._distance = time_delta / 0.000058
            elif format == "in":
                self._distance = time_delta / 0.000148

            return round(self._distance, 2)

    def measure(self, *, samples=1, format="cm"):
        if samples < 2:
            return self._measure_distance(format)
        else:
            result = 0
            samples_taken = 0
            for _ in range(0, samples):
                echo = self._measure_distance(format)
                if echo > 0:
                    result += echo
                    samples_taken += 1
                time.sleep(self._delay)
            if samples_taken > 0:
                self._distance = round((result / samples_taken), 2)

    def get_distance(self):
        return round(self._distance, 2)

    def stop(self):
        GPIO.cleanup()


if __name__ == "__main__":
    left = HcSr04(Pins.Ultrasonic.LEFT_TRIGGER, Pins.Ultrasonic.LEFT_ECHO)
    right = HcSr04(Pins.Ultrasonic.RIGHT_TRIGGER, Pins.Ultrasonic.RIGHT_ECHO)
    time.sleep(0.1)
    # for _ in range(10):
    #     print(f"Distanz Rechts: {right.measure_distance()} cm")
    #     time.sleep(0.06)

    for _ in range(10):
        left.measure(samples=5)
        right.measure(samples=5)
        print(f"Links: {left.get_distance()} cm, rechts: {right.get_distance()} cm.")
        time.sleep(0.1)

    # echo = [left, right]
    #
    # for _ in range(10):
    #     for x in range(0, len(echo)):
    #         result = echo[x].measure_distance()
    #         print(f"Sensor {x} - {round(result, 2)} cm")

    left.stop()
    right.stop()
