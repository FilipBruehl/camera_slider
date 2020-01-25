import sys
from classes.client import Client


if __name__ == "__main__":
    """Main-Funktion des Clients"""

    client = Client()                                                                                                   # Erstelle neue Instanz der Klasse Client
    sys.exit(client.run())                                                                                              # Führe den Client aus
