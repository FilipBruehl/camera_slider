import socketio
import eventlet
import pickle
from classes.camera import Camera
from classes.motor import StepMotor
from classes.hc_sr04 import HcSr04
from classes.pins import Pins


class Server(socketio.Namespace):
    _instance = None
    port = 50007
    ip = '192.168.0.97'

    def __init__(self, sio, namespace=None):
        super().__init__(namespace or '/')
        self.sio = sio
        self.camera_selected = None
        self.pictures_to_take = None
        self.motor = None
        self.motor_data = None
        self.motor_running = False
        self.hc_sr04_left = None
        self.hc_sr04_right = None
        self.distance_left = None
        self.distance_right = None
        print(f"Server successfully started on {Server.ip}:{Server.port}")

    @staticmethod
    def get_instance(sio=None, namespace=None):
        if not Server._instance:
            Server._instance = Server(sio, namespace)
        return Server._instance

    def on_connect(self, sid, environ):
        print(f"{sid} connected")

    def on_disconnect(self, sid):
        print(f'{sid} disconnected')

    def on_connect_camera(self, sid, data):
        cameras = Camera.get_available_cameras()
        if cameras:
            if not self.camera_selected:
                self.camera_selected = Camera(data)
            self.sio.emit('camera_init', self.camera_selected.get_information())
        else:
            print("No camera available")
            self.sio.emit('camera_not_available')

    # def on_get_cameras(self, sid):
    #     cameras = Camera.get_available_cameras()
    #     if cameras:
    #         cameras = [camera[0] for camera in cameras]
    #         print("Sending cameras")
    #         self.sio.emit('send_cameras', cameras)
    #     else:
    #         print("No camera available")
    #         self.sio.emit('camera_not_available')
    #
    # def on_set_camera(self, sid, data):
    #     print(sid, data)
    #     if not self.camera_selected:
    #         self.camera_selected = Camera(data)
    #     self.sio.emit('camera_init', self.camera_selected.get_information())

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

    def on_connect_sensors(self, id):
        self.hc_sr04_left = HcSr04(Pins.Ultrasonic.LEFT_TRIGGER, Pins.Ultrasonic.LEFT_ECHO)
        self.hc_sr04_right = HcSr04(Pins.Ultrasonic.RIGHT_TRIGGER, Pins.Ultrasonic.RIGHT_ECHO)
        self.sio.emit('sensors_connected')
        eventlet.sleep(0.1)
        self.measure_distance()

    def on_disconnect_sensors(self, id):
        self.hc_sr04_left = None
        self.hc_sr04_right = None
        self.sio.emit('sensors_disconnected')

    def on_set_slider_settings(self, sid, data):
        self.motor_data = data
        self.motor.set_frequency(int(self.motor_data['frequency']))
        data.update({'running': self.motor_running})
        self.sio.emit('slider_settings_set', data)

    def on_start_slider(self, sid):
        self.sio.emit('slider_started')
        self.sio.start_background_task(self.move_camera)
        self.sio.emit('slider_finished')

    def on_set_camera_settings(self, sid, data):
        self.pictures_to_take = int(data['takes'])

    def on_take_picture(self, sid):
        self.camera_selected.take_picture()

    def move_camera(self):
        rotate = self.motor.rotate_counterclockwise if self.motor_data['direction'] == "Links" else self.motor.rotate_clockwise
        self.motor_running = True
        eventlet.spawn(self.measure_distance_thread)
        self.sio.start_background_task(self.camera_selected.take_picture)
        self.pictures_to_take -= 1
        steps_per_cycle = int(self.motor_data['steps'])//self.pictures_to_take
        print(f"Pictures: {self.pictures_to_take}, steps: {steps_per_cycle}")
        for x in range(self.pictures_to_take):
            for _ in range(steps_per_cycle):
                rotate()
            # eventlet.sleep(0.1)
            self.sio.start_background_task(self.camera_selected.take_picture)
            # self.sio.start_background_task(self.measure_distance)
        self.motor_running = False
        self.motor.disable()

    def measure_distance(self):
        self.distance_left = self.hc_sr04_left.samples()
        self.distance_right = self.hc_sr04_right.samples()
        print(f"Links: {self.distance_left} cm/ Rechts: {self.distance_right} cm")
        self.sio.emit('distance', data={'left': self.distance_left, 'right': self.distance_right})
        #eventlet.sleep(0.01)

    def measure_distance_thread(self):
        while self.motor_running:
            self.distance_left = self.hc_sr04_left.measure_distance()
            self.distance_right = self.hc_sr04_right.measure_distance()
            print(f"Links: {self.distance_left} cm/ Rechts: {self.distance_right} cm")
            self.sio.emit('distance', data={'left': self.distance_left, 'right': self.distance_right})
            eventlet.sleep(0.2)
