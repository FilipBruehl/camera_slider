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
        self.camera_connected = False
        self.motor_connected = False
        self._app = QApplication(sys.argv)
        self._window = MainWindow()
        self.init_window()

    def init_window(self):
        self._window.connect_server_signal.connect(self.start)
        self._window.disconnect_server_signal.connect(self.disconnect)
        self._window.connect_camera_signal.connect(self.connect_camera)
        self._window.disconnect_camera_signal.connect(self.disconnect_camera)
        self._window.connect_motor_signal.connect(self.connect_motor)
        self._window.disconnect_motor_signal.connect(self.disconnect_motor)
        self._window.connect_sensors_signal.connect(self.connect_sensors)
        self._window.disconnect_sensors_signal.connect(self.disconnect_sensors)
        self._window.set_slider_settings_signal.connect(self.set_slider_settings)
        self._window.set_camera_settings_signal.connect(self.set_camera_settings)
        self._window.take_picture_signal.connect(self.take_picture)
        self._window.start_slider_signal.connect(self.start_slider)

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

    def connect_camera(self):
        self.sio.emit('connect_camera', 0)

    # def get_available_cameras(self):
    #     self.sio.emit('get_cameras')

    def disconnect_camera(self):
        self.sio.emit('disconnect_camera')

    def connect_motor(self):
        self.sio.emit('connect_motor')

    def disconnect_motor(self):
        self.sio.emit('disconnect_motor')

    def connect_sensors(self):
        self.sio.emit('connect_sensors')

    def disconnect_sensors(self):
        self.sio.emit('disconnect_sensors')

    def set_slider_settings(self):
        self.sio.emit('set_slider_settings', self._window.get_slider_settings())

    def start_slider(self):
        self.sio.emit('start_slider')

    def set_camera_settings(self):
        self.sio.emit('set_camera_settings', self._window.get_camera_settings())

    def take_picture(self):
        self.sio.emit('take_picture')

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
    def on_camera_not_available(self, data):
        self._window.set_camera_not_available()

    # @sio.event
    # def on_send_cameras(self, data):
    #     self.sio.emit('set_camera', 0)

    @sio.event
    def on_camera_init(self, data):
        self.camera_connected = True
        self._window.set_camera_connected(data)

    @sio.event
    def on_camera_disconnected(self, data):
        self.camera_connected = False
        self._window.set_camera_disconnected()

    @sio.event
    def on_motor_connected(self, data):
        self.motor_connected = True
        self._window.set_motor_connected()

    @sio.event
    def on_motor_disconnected(self, data):
        self.motor_connected = False
        self._window.set_motor_disabled()

    @sio.event
    def on_slider_settings_set(self, data):
        self._window.set_slider_info(data)

    @sio.event
    def on_slider_started(self, data):
        self._window.slider_started()

    @sio.event
    def on_slider_finished(self, data):
        self._window.slider_finished()

    @sio.event
    def on_distance(self, data):
        self._window.set_distance(data)

    @sio.event
    def on_sensors_connected(self, data):
        self._window.set_sensors_connected()

    @sio.event
    def on_sensors_disconnected(self, data):
        self._window.set_sensors_disconnected()


if __name__ == "__main__":
    client = Client.get_instance(sio, '/')
    sio.register_namespace(client)
    print("running")