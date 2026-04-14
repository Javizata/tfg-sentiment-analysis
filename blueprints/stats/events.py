import json
from flask_socketio import emit
from helpers import socketio
from plotly.utils import PlotlyJSONEncoder
from app_state import APP_STATE
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
    results = []
    for model in APP_STATE["models_to_use"]:
        sentiment, conf, probs = predict_review(text["text"], model)
        results.append({
            "model": model,
            "sentiment": sentiment,
            "confidence": conf,
            "probabilities": probs.tolist() if probs is not None else None
        })
        print(sentiment, conf, probs)
    emit("result", {"results": results}, namespace="/stats")
    
def emit_plot(event, fig):
    emit(
        event,
        json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
    )

    