import time
from RPi import GPIO


class HcSr04:
    """
    Klasse HcSr04 für die Kommunikation mit einem Ultraschallsensor
    """

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
