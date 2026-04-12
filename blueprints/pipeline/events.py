from helpers import socketio
from flask_socketio import emit

@socketio.on("connect", namespace="/pipeline")
def pipeline_connect():
    print("Cliente conectado a /pipeline en events pipeline")
    emit("pipeline_message", {"data": "Conectado al namespace /pipeline"})
    
