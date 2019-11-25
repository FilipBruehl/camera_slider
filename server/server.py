import sys
import socket
import pickle
import gphoto2 as gp
from threading import Thread
from helpers.camera import init_camera


class Server:
    def __init__(self):
        self.port = 50007
        self.ip = ""
        self.header_size = 10
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        print("Server gestartet")
        self.conn, (self.conn_ip, self.conn_port) = self.socket.accept()
        print(f"{self.conn_ip} verbunden")
        self.exit = False
        self.thread_recv = Thread(target=self.receive)
        self.thread_recv.start()
        self.cameras_available = None
        self.camera_selected_index = None
        self.camera_selected = None

    def receive(self):
        command = None
        command_len = None
        data = None
        data_len = None

        while not self.exit:
            try:
                command_len = self.conn.recv(self.header_size)
                command_len = command_len.decode().strip()
                command_len = int(command_len)
                print(f"command_len = {command_len}")
                if command_len > 0:
                    print("loading command")
                    command = self.conn.recv(command_len)
                    data_len = int(command[:self.header_size].decode().strip())
                    command = command[self.header_size:]
                    command = pickle.loads(command)
                    print(f"command loaded. command = {command}, data_len = {data_len}")
                    if data_len > 0:
                        print("loading data")
                        data = self.conn.recv(data_len)
                        data = pickle.loads(data)
                        print(f"data loaded. data = {data}")
                print("message received")
                self.handle_command(command, data)
            except:
                pass
            finally:
                command = None
                command_len = None
                data = None
                data_len = None

    def send(self, command, data=None):
        try:
            if data:
                data = pickle.dumps(data)
                data_len = bytes(f"{len(data):<{self.header_size}}", 'utf-8')
            else:
                data_len = bytes(f"{0:<{self.header_size}}", 'utf-8')
            command = pickle.dumps(command)
            command = data_len + command
            command_len = bytes(f"{len(command):<{self.header_size}}", 'utf-8')
            self.conn.send(command_len)
            self.conn.send(command)
            if data:
                self.conn.send(data)
            print(f"message send. command_len = {command_len}, command = {command}, data_len = {data_len}, data = {data}")
        except:
            pass

    def handle_command(self, command, data=None):
        if command == "get cameras":
            if hasattr(gp, 'gp_camera_autodetect'):
                self.cameras_available = gp.check_result(gp.gp_camera_autodetect())
                cameras_send = [camera[0] for camera in self.cameras_available]
                self.send("send cameras", cameras_send)
        elif command == "set camera":
            self.camera_selected_index = data
            self.camera_selected = init_camera(self.cameras_available[self.camera_selected_index])
        elif command == "disconnect client":
            print(f"{self.conn_ip} disconnected")
            self.conn.close()


if __name__ == "__main__":
    server = Server()
