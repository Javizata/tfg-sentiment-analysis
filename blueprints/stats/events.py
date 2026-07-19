import json
from flask_socketio import emit
from helpers import socketio
from plotly.utils import PlotlyJSONEncoder
from app_state import APP_STATE
from services.stats.charts import cargar_todo
from services.stats.predict_reviews import predict_review
from services.models.distilbert_registry import predict_distilbert


@socketio.on("connect", namespace="/stats")
def handle_connect():
    print("Client connected for stats")
    emit("server_message", {"data": "Connected to the server"})

@socketio.on("report", namespace="/stats")
def generate_graphs():
    print("📊 Graphs requested")

    # 1️⃣ Models selected by the user
    models_selected = APP_STATE.get("models_to_use", [])

    if not models_selected:
        emit("error", {"message": "No models selected"})
        return

    # 2️⃣ Generate graphs dynamically
    (
        fig_barras,
        fig_radar,
        fig_tabla,
        fig_heatmap,
        fig_ranking,
        fig_precision_recall
    ) = cargar_todo(models_selected)

    # 3️⃣ Emit each graph to the frontend
    emit_plot("grafico_barras", fig_barras)
    emit_plot("radar", fig_radar)
    emit_plot("tabla", fig_tabla)
    emit_plot("heatmap", fig_heatmap)
    emit_plot("ranking", fig_ranking)
    emit_plot("precision_recall", fig_precision_recall)


@socketio.on("analizar_resena", namespace="/stats")
def generate_review(text):
    print("Review requested")
    print(text)
    results = []
    for model in APP_STATE["models_to_use"]:
        
        if model.startswith("distilbert"):
            sentiment, conf, probs = predict_distilbert(text["text"], model)
        else:
            sentiment, conf, probs = predict_review(text["text"], model)
        results.append({
            "model": model,
            "sentiment": sentiment,
            "confidence": conf,
            "probabilities": probs if probs is not None else None
        })
        print(sentiment, conf, probs)
    emit("result", {"results": results}, namespace="/stats")
    
def emit_plot(event, fig):
    emit(
        event,
        json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
    )