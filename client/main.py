import sys
import socketio
from classes.ClientSocketio import Client


sio = socketio.Client('eventlet')

if __name__ == "__main__":
    client = Client.get_instance(sio, '/')
    sio.register_namespace(client)
    print(client)
    sys.exit(client.run())