import socketio
import pickle
from classes.camera import Camera


class Server(socketio.Namespace):
    _instance = None
    port = 50007
    ip = '192.168.0.97'

    def __init__(self, sio, namespace=None):
        super().__init__(namespace or '/')
        self.sio = sio
        self.camera_selected = None

    @staticmethod
    def get_instance(sio=None, namespace=None):
        if not Server._instance:
            Server._instance = Server(sio, namespace)
        return Server._instance

    def on_connect(self, sid, environ):
        print(f"{sid} connected")

    def on_disconnect(self, sid):
        print(f'{sid} disconnected')

    def on_get_cameras(self, sid):
        print("Sending cameras")
        cameras = Camera.get_available_cameras()
        cameras = [camera[0] for camera in cameras]
        self.sio.emit('send_cameras', cameras)

    def on_set_camera(self, sid, data):
        print(sid, data)
        if not self.camera_selected:
            self.camera_selected = Camera(data)
        self.sio.emit('camera_init', self.camera_selected.get_information())
