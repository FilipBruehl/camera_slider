# Import necessary libraries.
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
    speed_of_sound = 343
    samples = 5

    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        self.echo = Echo(self.trigger, self.echo)

    def measure_distance(self):
        return self.echo.read('cm', HcSr04.samples)

    def stop(self):
        self.echo.stop()


if __name__ == "__main__":
    left = HcSr04(Pins.Ultrasonic.LEFT_TRIGGER, Pins.Ultrasonic.LEFT_ECHO)
    right = HcSr04(Pins.Ultrasonic.RIGHT_TRIGGER, Pins.Ultrasonic.RIGHT_ECHO)

    # for _ in range(10):
    #     print(f"Links: {left.measure_distance()} cm, rechts: {right.measure_distance()} cm.")

    echo = [left, right]

    for _ in range(10):
        for x in range(0, len(echo)):
            result = echo[x].measure_distance()
            print(f"Sensor {x} - {round(result, 2)} cm")

    left.stop()
    right.stop()
