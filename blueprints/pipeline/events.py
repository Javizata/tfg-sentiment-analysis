from helpers import socketio
from flask_socketio import emit

@socketio.on("connect", namespace="/pipeline")
def pipeline_connect():
    print("Client connected to /pipeline in pipeline events")
    emit("pipeline_message", {"data": "Connected to /pipeline namespace"})