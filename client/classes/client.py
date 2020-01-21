import socket
import pickle
import sys
from threading import Thread
from time import sleep
from PyQt5.QtWidgets import QApplication
from classes.ui.MainWindow import MainWindow
from classes.ui.ConnectServer import ConnectServer


# folgt dem Singleton pattern
class Client:
    _instance = None

    def __init__(self):
        if Client._instance:
            raise Exception("Client already initialized")
        else:
            self.host_port = 50007
            self.host_ip = ""
            self.header_size = 10
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connected = False
            self.camera_connected = False
            self.camera_info = None
            self.camera_options = None
            self.motor_connected = False
            self._app = QApplication(sys.argv)
            self._window = MainWindow()
            self.thread_recv = Thread(target=self.receive)
            self.init_main_window_signals()

    def init_main_window_signals(self):
        self._window.connect_server_signal.connect(self.connect)
        self._window.disconnect_server_signal.connect(self.disconnect)
        self._window.connect_camera_signal.connect(self.connect_camera)
        self._window.disconnect_camera_signal.connect(self.disconnect_camera)
        self._window.connect_motor_signal.connect(self.connect_motor)
        self._window.disconnect_motor_signal.connect(self.disconnect_motor)
        self._window.connect_sensors_signal.connect(self.connect_sensors)
        self._window.disconnect_sensors_signal.connect(self.disconnect_sensors)
        self._window.set_slider_settings_singal.connect(self.set_slider_settings)
        self._window.set_kamera_settings_signal.connect(self.set_camera_settings)
        self._window.take_picture_signal.connect(self.take_picture)
        self._window.start_slider_signal.connect(self.start_slider)
        self._window.position_slider_signal.connect(self.position_slider)
    
    @staticmethod
    def get_instance():
        if not Client._instance:
            Client._instance = Client()
        return Client._instance

    def run(self):
        self._window.show()
        return self._app.exec_()

    def connect(self):
        self.host_ip = ConnectServer.get_ip()
        try:
            self.socket.connect((self.host_ip, self.host_port))
            self.connected = True
            self.thread_recv.start()
            print(f"Connected to Server on {self.host_ip}:{self.host_port}")
            self._window.set_connected(self.host_ip)
        except Exception as e:
            self._window.set_connection_failed()
            print(e)

    def disconnect(self):
        self.send("disconnect_client")
        self.connected = False
        self._window.set_not_connected()

    def connect_camera(self):
        self.send("connect_camera", 0)

    def disconnect_camera(self):
        self.send("disconnect_camera")

    def connect_motor(self):
        self.send("connect_motor")

    def disconnect_motor(self):
        self.send("disconnect_motor")

    def connect_sensors(self):
        self.send("connect_sensors")

    def disconnect_sensors(self):
        self.send("disconnect_sensors")

    def set_slider_settings(self):
        self.send("set_slider_settings", self._window.get_slider_settings())

    def set_camera_settings(self):
        self.send("set_camera_settings", self._window.get_kamera_settings())

    def take_picture(self):
        self.send("take_picture")

    def start_slider(self):
        self.send("start_slider")

    def position_slider(self):
        self.send("position_slider", self._window.get_slider_start())

    def send(self, command, data=None):
        try:
            # print(data)
            if data is not None:
                # print(data)
                data = pickle.dumps(data)
                data_len = bytes(f"{len(data):<{self.header_size}}", 'utf-8')
            else:
                data_len = bytes(f"{0:<{self.header_size}}", 'utf-8')
            command = pickle.dumps(command)
            command = data_len + command
            command_len = bytes(f"{len(command):<{self.header_size}}", 'utf-8')
            self.socket.send(command_len)
            self.socket.send(command)
            if data:
                self.socket.send(data)
            print(f"message send. command_len = {command_len}, command = {command}, data_len = {data_len}, data = {data}")
        except:
            pass

    def receive(self):
        command = None
        command_len = None
        data = None
        data_len = None

        while self.connected:
            try:
                command_len = self.socket.recv(self.header_size)
                command_len = command_len.decode().strip()
                command_len = int(command_len)
                # print(f"command_len = {command_len}")
                if command_len > 0:
                    # print("loading command")
                    command = self.socket.recv(command_len)
                    data_len = int(command[:self.header_size].decode().strip())
                    command = command[self.header_size:]
                    command = pickle.loads(command)
                    # print(f"command loaded. command = {command}, data_len = {data_len}")
                    if data_len > 0:
                        # print("loading data")
                        data = self.socket.recv(data_len)
                        data = pickle.loads(data)
                        # print(f"data loaded. data = {data}")
                        # print("message received")
                print(f"message received. command_len = {command_len}, command = {command}, data_len = {data_len}, data = {data}")
                self.handle_command(command, data)
            except:
                pass
            finally:
                command = None
                command_len = None
                data = None
                data_len = None

    def handle_command(self, command, data=None):
        if command == "camera_not_available":
            self.on_camera_not_available()
        elif command == "camera_init":
            self.on_camera_init(data)
        elif command == "camera_options":
            self.on_camera_options(data)
        elif command == "camera_values":
            self.on_camera_values(data)
        elif command == "camera_disconnected":
            self.on_camera_disconnected()
        elif command == "motor_connected":
            self.on_motor_connected()
        elif command == "motor_disconnected":
            self.on_motor_disconnected()
        elif command == "slider_settings_set":
            self.on_slider_settings_set(data)
        elif command == "slider_started":
            self.on_slider_started()
        elif command == "slider_finished":
            self.on_slider_finished()
        elif command == "sensors_connected":
            self.on_sensors_connected()
        elif command == "sensors_disconnected":
            self.on_sensors_disconnected()
        elif command == "distance":
            self.on_distance(data)
        elif command == "disconnect":
            self.on_disconnect()

    def on_disconnect(self):
        self.socket.close()
        print("Disconnected")

    def on_camera_not_available(self):
        self._window.set_camera_not_available()

    def on_camera_init(self, data):
        self.camera_connected = True
        self.camera_info = data
        self._window.set_camera_connected(data)
        self.send("get_camera_options")

    def on_camera_options(self, data):
        self.camera_options = data
        self._window.set_camera_options(data)

    def on_camera_values(self, data):
        self._window.set_camera_values(data)

    def on_camera_disconnected(self):
        self.camera_connected = False
        self._window.set_camera_disconnected()

    def on_motor_connected(self):
        self.motor_connected = True
        self._window.set_motor_connected()

    def on_motor_disconnected(self):
        self.motor_connected = False
        self._window.set_motor_disabled()

    def on_slider_settings_set(self, data):
        self._window.set_slider_info(data)

    def on_slider_started(self):
        self._window.slider_started()

    def on_slider_finished(self):
        self._window.slider_finished()

    def on_distance(self, data):
        self._window.set_distance(data)

    def on_sensors_connected(self):
        self._window.set_sensors_connected()

    def on_sensors_disconnected(self):
        self._window.set_sensors_disconnected()


if __name__ == "__main__":
    client = Client.get_instance()
    sys.exit(client.run())
