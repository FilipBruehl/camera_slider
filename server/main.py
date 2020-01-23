from os import system
from time import sleep
from classes.server import Server


if __name__ == "__main__":
    system("sudo systemctl disable pigpiod")
    sleep(0.5)
    system("sudo systemctl start pigpiod")
    print("Daemon started")

    server = Server()
    try:
        server.run()
    except KeyboardInterrupt:
        server.stop()

