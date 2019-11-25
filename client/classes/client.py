import socket
import pickle
#import ghoto2 as gp
from threading import Thread
from classes.ui.ConnectCamera import ConnectCamera
from classes.DataContainer import DataContainer


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
            self.thread_recv = Thread(target=self.receive)
            self.data = DataContainer.get_instance()
            print(self.data)
    
    @staticmethod
    def get_instance():
        if not Client._instance:
            Client._instance = Client()
        return Client._instance

    def connect(self, ip: str) -> bool:
        self.host_ip = ip
        try:
            self.socket.connect((self.host_ip, self.host_port))
            self.connected = True
            self.thread_recv.start()
            return True
        except:
            return False

    def send(self, command, data=None):
        try:
            print(data)
            if data != None:
                print(data)
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
                print(f"command_len = {command_len}")
                if command_len > 0:
                    print("loading command")
                    command = self.socket.recv(command_len)
                    data_len = int(command[:self.header_size].decode().strip())
                    command = command[self.header_size:]
                    command = pickle.loads(command)
                    print(f"command loaded. command = {command}, data_len = {data_len}")
                    if data_len > 0:
                        print("loading data")
                        data = self.socket.recv(data_len)
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

    def handle_command(self, command, data=None):
        if command == "send cameras":
            self.add_data("cameras", data)

    def get_cameras(self):
        self.send("get cameras")

    def get_data(self, key):
        return self.data.get_data(key)

    def add_data(self, key, data):
        self.data.add_data(key, data)

    def disconnect(self):
        self.send("disconnect client")
        self.socket.close()
        self.connected = False