import socketio
import pickle
from classes.camera import Camera
from classes.motor import StepMotor
from time import sleep


class Server(socketio.Namespace):
    _instance = None
    port = 50007
    ip = '192.168.0.97'

    def __init__(self, sio, namespace=None):
        super().__init__(namespace or '/')
        self.sio = sio
        self.camera_selected = None
        self.motor = None
        self.motor_data = None
        self.motor_running = False

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
        cameras = Camera.get_available_cameras()
        if cameras:
            cameras = [camera[0] for camera in cameras]
            print("Sending cameras")
            self.sio.emit('send_cameras', cameras)
        else:
            print("No camera available")
            self.sio.emit('camera_not_available')

    def on_set_camera(self, sid, data):
        print(sid, data)
        if not self.camera_selected:
            self.camera_selected = Camera(data)
        self.sio.emit('camera_init', self.camera_selected.get_information())

    def on_disconnect_camera(self, sid):
        self.camera_selected.exit()
        self.camera_selected = None
        self.sio.emit('camera_disconnected')

    def on_connect_motor(self, sid):
        self.motor = StepMotor()
        self.sio.emit('motor_connected')

    def on_disconnect_motor(self, sid):
        self.motor.disable()
        self.motor = None
        self.sio.emit('motor_disconnected')

    def on_set_slider_settings(self, sid, data):
        self.motor_data = data
        self.motor.set_frequence(int(self.motor_data['frequency']))
        data.update({'running': self.motor_running})
        self.sio.emit('slider_settings_set', data)

    def on_start_slider(self, sid):
        self.sio.emit('slider_started')
        rotate = self.motor.rotate_clockwise if self.motor_data['direction'] == "Rechts" else self.motor.rotate_counterclockwise
        for _ in range(int(self.motor_data['steps'])):
            rotate()
        self.motor.disable()
        self.sio.emit('slider_finished')
