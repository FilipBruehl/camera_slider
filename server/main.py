import socketio
import eventlet.wsgi
from classes.socketio_server import Server


sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio)

if __name__ == "__main__":
    sio.register_namespace(Server.get_instance(sio, '/'))
    eventlet.wsgi.server(eventlet.listen((Server.ip, Server.port)), app)

