import sys
from classes.client import Client


if __name__ == "__main__":
    client = Client()
    sys.exit(client.run())
