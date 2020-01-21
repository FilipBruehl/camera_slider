import socket
import pickle
import sys
from threading import Thread
from time import sleep
from os import system
from classes.camera import Camera
from classes.motor import StepMotor
from classes.hc_sr04 import HcSr04
from classes.pins import Pins


class Server:
    def __init__(self):
        self.port = 50007
        self.ip = ""
        self.header_size = 10
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.conn, self.conn_ip, self.conn_port = None, None, None
        self.exit = False
        self.thread_recv = Thread(target=self.receive)
        self.camera_selected = None
        self.pictures_to_take = None
        self.motor = None
        self.motor_running = False
        self.motor_data = None
        self.hc_sr04_left, self.hc_sr04_right = None, None
        self.distance_left, self.distance_right = None, None

    def run(self):
        self.socket.listen(1)
        print("Server gestartet")
        self.conn, (self.conn_ip, self.conn_port) = self.socket.accept()
        print(f"{self.conn_ip} verbunden")
        try:
            self.thread_recv.start()
        except:
            pass

    def stop(self):
        if self.conn:
            self.on_disconnect_client()
        self.socket.close()
        sys.exit()

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
                # print(f"command_len = {command_len}")
                if command_len > 0:
                    # print("loading command")
                    command = self.conn.recv(command_len)
                    data_len = int(command[:self.header_size].decode().strip())
                    command = command[self.header_size:]
                    command = pickle.loads(command)
                    # print(f"command loaded. command = {command}, data_len = {data_len}")
                    if data_len > 0:
                        # print("loading data")
                        data = self.conn.recv(data_len)
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
        if command == "connect_camera":
            self.on_connect_camera(data)
        elif command == "get_camera_options":
            self.on_get_camera_options()
        elif command == "disconnect_camera":
            self.on_disconnect_camera()
        elif command == "disconnect_client":
            self.on_disconnect_client()
        elif command == "connect_motor":
            self.on_connect_motor()
        elif command == "disconnect_motor":
            self.on_disconnect_motor()
        elif command == "connect_sensors":
            self.on_connect_sensors()
        elif command == "disconnect_sensors":
            self.on_disconnect_sensors()
        elif command == "set_slider_settings":
            self.on_set_slider_settings(data)
        elif command == "set_camera_settings":
            self.on_set_camera_settings(data)
        elif command == "take_picture":
            self.on_take_picture()
        elif command == "start_slider":
            self.on_start_slider()
        elif command == "position_slider":
            self.on_position_slider(data)

    def on_connect_camera(self, data):
        cameras = Camera.get_available_cameras()
        if cameras:
            if not self.camera_selected:
                self.camera_selected = Camera(data)
            self.send('camera_init', self.camera_selected.get_information())
        else:
            print("No camera available")
            self.send('camera_not_available')

    def on_get_camera_options(self):
        options = self.camera_selected.get_options()
        self.send('camera_options', options)

    def on_disconnect_camera(self):
        self.camera_selected.exit()
        self.camera_selected = None
        self.send('camera_disconnected')

    def on_disconnect_client(self):
        print(f"{self.conn_ip} disconnected")
        self.send("disconnect")
        sleep(0.5)
        self.exit = True
        self.conn.close()

    def on_connect_motor(self):
        self.motor = StepMotor()
        self.send('motor_connected')

    def on_disconnect_motor(self):
        self.motor.disable()
        self.motor = None
        self.send('motor_disconnected')

    def on_connect_sensors(self):
        self.hc_sr04_left = HcSr04(Pins.Ultrasonic.LEFT_TRIGGER, Pins.Ultrasonic.LEFT_ECHO)
        self.hc_sr04_right = HcSr04(Pins.Ultrasonic.RIGHT_TRIGGER, Pins.Ultrasonic.RIGHT_ECHO)
        self.send('sensors_connected')
        sleep(0.1)
        self.measure_distance()

    def on_disconnect_sensors(self):
        self.hc_sr04_left = None
        self.hc_sr04_right = None
        self.send('sensors_disconnected')

    def on_set_slider_settings(self, data):
        self.motor_data = data
        print(self.motor_data)
        self.motor.set_frequency(int(self.motor_data['frequency']))
        # data.update({'running': self.motor_running})
        self.send('slider_settings_set', data)

    def on_start_slider(self):
        self.send('slider_started')
        thread_camera = Thread(target=self.move_camera)
        thread_distance = Thread(target=self.measure_distance_thread)
        thread_camera.start()
        sleep(0.1)
        thread_distance.start()
        thread_camera.join()
        thread_distance.join()
        self.send('slider_finished')

    def on_set_camera_settings(self, data):
        self.pictures_to_take = int(data['takes'])
        self.camera_selected.set_focal(data['focal'])
        self.camera_selected.set_shutter_speed(data['shutter'])
        self.camera_selected.set_iso(data['iso'])
        self.send('camera_values', self.camera_selected.get_information())

    def on_take_picture(self):
        self.camera_selected.take_picture()

    def on_position_slider(self, data):
        self.send('slider_started')
        thread_position = Thread(target=self.position_slider, args=(data,))
        thread_distance = Thread(target=self.measure_distance_thread)
        thread_position.start()
        sleep(0.2)
        thread_distance.start()
        thread_position.join()
        thread_distance.join()
        self.send('slider_finished')

    def position_slider(self, new_position):
        print(new_position)
        rotate = None
        distance = None
        steps = None
        self.motor_running = True
        if new_position == "Links":
            rotate = self.motor.rotate_counterclockwise
            distance = self.distance_left - 5
        elif new_position == "Rechts":
            rotate = self.motor.rotate_clockwise
            distance = self.distance_right - 5
        elif new_position == "Mitte":
            if self.distance_left > self.distance_right:
               rotate = self.motor.rotate_clockwise
               distance = self.distance_left - self.distance_right
            elif self.distance_left < self.distance_right:
                rotate = self.motor.rotate_counterclockwise
                distance = self.distance_right - self.distance_left
        steps = distance // 4 * 200
        print(steps)

        for _ in range(0, int(steps)):
            rotate()

        self.motor_running = False
        self.motor.disable()

    def move_camera(self):
        rotate = self.motor.rotate_counterclockwise if self.motor_data['direction'] == "Links" else self.motor.rotate_clockwise
        self.motor_running = True
        self.camera_selected.take_picture()
        # self.measure_distance()
        self.pictures_to_take -= 1
        steps = None
        cm = None
        if self.motor_data['type'] == 'automatic':
            steps = (int(self.motor_data['distance']) / 4) * 200
            cm = int(self.motor_data['distance'])
        elif self.motor_data['type'] == 'manual':
            steps = int(self.motor_data['distance'])
            cm = (int(self.motor_data['distance']) / 200) * 4
        steps_per_cycle = int(steps)//self.pictures_to_take
        print(f"Pictures: {self.pictures_to_take}, steps: {steps_per_cycle}")
        for x in range(self.pictures_to_take):
            for _ in range(steps_per_cycle):
                rotate()
            sleep(0.5)
            self.camera_selected.take_picture()
            # self.measure_distance()
        self.motor_running = False
        self.motor.disable()

    def measure_distance(self):
        self.distance_left = self.hc_sr04_left.samples()
        self.distance_right = self.hc_sr04_right.samples()
        print(f"Links: {self.distance_left} cm/ Rechts: {self.distance_right} cm")
        self.send('distance', data={'left': self.distance_left, 'right': self.distance_right})
        sleep(0.1)

    def measure_distance_thread(self):
        while self.motor_running:
            self.distance_left = self.hc_sr04_left.measure_distance()
            self.distance_right = self.hc_sr04_right.measure_distance()
            print(f"Links: {self.distance_left} cm/ Rechts: {self.distance_right} cm")
            self.send('distance', data={'left': self.distance_left, 'right': self.distance_right})
            sleep(0.1)


if __name__ == "__main__":
    system("sudo systemctl disable pigpiod")
    sleep(0.5)
    system("sudo systemctl start pigpiod")
    print("Daemon started")

    server = Server()
    try:
        server.run()
    except KeyboardInterrupt:
        server.stop()
