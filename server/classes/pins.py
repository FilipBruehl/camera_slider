class Pins:
    class Ultrasonic:
        LEFT_TRIGGER = 26
        LEFT_ECHO = 19

        RIGHT_TRIGGER = 20
        RIGHT_ECHO = 21

    class Motor:
        OUTPUT = [17, 25]
        STEPS = [27, 22, 23, 24]
        SEQUENCE = [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [1, 0, 0, 1]
        ]
