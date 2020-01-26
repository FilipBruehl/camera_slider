class Pins:
    """
    Klasse Pins zum Speichern der Pin-Nummern
    """

    class Ultrasonic:
        LEFT_TRIGGER = 20
        LEFT_ECHO = 21

        RIGHT_TRIGGER = 26
        RIGHT_ECHO = 19

    class Motor:
        OUTPUT = [17, 25]
        STEPS = [27, 22, 23, 24]
        SEQUENCE = [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [1, 0, 0, 1]
        ]