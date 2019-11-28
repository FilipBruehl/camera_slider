import socketio
import asyncio
import pickle
import sys
from PyQt5.QtWidgets import QApplication
from classes.ui.MainWindow import MainWindow
from classes.ui.ConnectServer import ConnectServer
from classes.ui.ConnectCamera import ConnectCamera

sio = socketio.Client('eventlet')


# Folgt dem Singleton Pattern
# Ist der Controller im MVC Pattern
class Client(socketio.ClientNamespace):
    _instance = None
    port = 50007
    ip = None

    def __init__(self, sio, app, namespace=None):
        super().__init__(namespace or '/')
        self.sio = sio
        self.app = app
        self.connected = False
        self._app = QApplication(sys.argv)
        self._window = MainWindow()
        self.init_window()

    def init_window(self):
        self._window.connect_server_signal.connect(self.start)
        self._window.disconnect_server_signal.connect(self.disconnect)
        self._window.connect_camera_signal.connect(self.get_available_cameras)
        # self._window.close_signal.connect()

    def run(self):
        self._window.show()
        return self._app.exec_()

    def start(self):
        print("Connecting")
        Client.ip = ConnectServer.get_ip()
        self.sio.connect(f'http://{Client.ip}:{Client.port}')
        # await self.sio.wait(1)

    def disconnect(self):
        self.sio.disconnect()
        print("Disconnected")
        self.connected = False
        self._window.set_not_connected()

    def get_available_cameras(self):
        self.sio.emit("get_cameras")

    @staticmethod
    def get_instance(sio=None, app=None, namespace=None):
        if not Client._instance:
            Client._instance = Client(sio, app, namespace)
        return Client._instance

    @sio.event
    def on_connect(self):
        print("Connected")
        self.connected = True
        self._window.set_connected(Client.ip)

    @sio.event
    def on_connect_error(self):
        print("Connection Failed")
        self.connected = False
        self._window.set_connection_failed()

    @sio.event
    def on_disconnect(self):
        print("Disconnected")
        self.connected = False
        self._window.set_not_connected()

    @sio.event
    def on_send_cameras(self, data):
        print(data)
        if data:
            self.sio.emit('set_camera', 0)
        else:
            self._window.set_camera_not_available()

    @sio.event
    def on_camera_init(self, data):
        print(data)
        self._window.set_camera_connected(data)


if __name__ == "__main__":
    client = Client.get_instance(sio, '/')
    sio.register_namespace(client)
    print("running")