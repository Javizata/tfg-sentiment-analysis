import json
from flask_socketio import emit
from helpers import socketio
from plotly.utils import PlotlyJSONEncoder

from services.stats.charts import cargar_todo
from services.stats.predict_reviews import predict_review

@socketio.on("connect", namespace="/stats")
def handle_connect():
    print("Cliente conectado para stats")
    emit("server_message", {"data": "Conectado al servidor"})

@socketio.on("report", namespace="/stats")
def generate_graphs():
    print("Gráficos solicitados")
    fg1,fg2,fg3,fg4 = cargar_todo()
    
    emit_plot("grafico_lineas", fg1)

    emit_plot("grafico_barras", fg2)

    emit_plot("tabla", fg3)

    emit_plot("matriz_confusion", fg4)

@socketio.on("analizar_resena", namespace="/stats")
def generate_resena(text):
    print("Reseña solicitada")
    print(text)
    sentiment, confidence, probabilities = predict_review(text["text"])
    print(sentiment, confidence, probabilities)
    emit(
        "result",
        {
            "sentiment": sentiment,
            "confidence": float(confidence) if confidence is not None else None,
            "probabilities": probabilities.tolist() if probabilities is not None else None
        },
        namespace="/stats"
    )

def emit_plot(event, fig):
    emit(
        event,
        json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
    )

    