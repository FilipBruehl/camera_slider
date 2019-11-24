import socket


class Client:
    def __init__(self):
        self.host_port = 50007
        self.host_ip = ""
        self.buffer_size = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip: str) -> bool:
        self.host_ip = ip
        try:
            self.socket.connect((self.host_ip, self.host_port))
            return True
        except:
            return False

    def disconnect(self):
        self.socket.close()