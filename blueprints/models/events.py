from flask_socketio import emit
from helpers import socketio

# Cambiar namespaces


@socketio.on("connect", namespace="/model_info")
def handle_connect():
    print("Cliente conectado en models")
    emit("server_message", {"data": "Conectado al servidor"})

@socketio.on("mensaje_cliente", namespace="/base")
def handle_message(data):
    print("Mensaje recibido:", data)
    emit("server_message", {"data": data})

socketio.on("trigger_pipeline", namespace="/trigger-pipeline")
def trigger_pipeline():
    print("Cliente")
