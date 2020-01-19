from os import system
from time import sleep
import socketio
import eventlet.wsgi
import logging
from classes.socketio_server import Server


sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio)

if __name__ == "__main__":
    eventlet.monkey_patch()
    system("sudo systemctl disable pigpiod")
    sleep(0.5)
    system("sudo systemctl start pigpiod")
    print("Daemon started")
    
    sio.register_namespace(Server.get_instance(sio, '/'))
    eventlet.wsgi.server(eventlet.listen((Server.ip, Server.port)), app, log_output=False)

