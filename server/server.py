import socket


class Server:
    def __init__(self):
        self.port = 50007
        self.ip = ""
        self.buffer_size = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        print("Server gestartet")
        self.conn, (self.conn_ip, self.conn_port) = self.socket.accept()
        print(f"{self.conn_ip} verbunden")


if __name__ == "__main__":
    server = Server()
