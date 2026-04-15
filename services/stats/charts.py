import numpy as np
import plotly.graph_objs as go

# =========================
# ESTILO GLOBAL PLOTLY (HMI)
# =========================
HMI_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Segoe UI, Arial",
        color="#e9f1f5",
        size=13
    ),
    title=dict(
        font=dict(size=18, color="#00d1ff"),
        x=0.03
    ),
    margin=dict(l=50, r=30, t=60, b=40),
)

# =========================
# MÉTRICAS BASE (SIMULADAS)
# =========================
ALL_METRICS = {
    "logistic_imdb": {
        "name": "Logistic Regression",
        "accuracy": 0.8786,
        "precision": 0.8662,
        "recall": 0.8938,
        "f1": 0.8798
    },
    "svm_imdb": {
        "name": "Linear SVM",
        "accuracy": 0.8696,
        "precision": 0.8650,
        "recall": 0.8740,
        "f1": 0.8695
    },
    "nb_imdb": {
        "name": "Naive Bayes",
        "accuracy": 0.8472,
        "precision": 0.8347,
        "recall": 0.8636,
        "f1": 0.8489
    }
}

# =========================
# FUNCIÓN PRINCIPAL
# =========================
def cargar_todo(models_selected:list = ["logistic_imdb","nb_imdb","svm_imdb"]):
    metrics = {k: v for k, v in ALL_METRICS.items() if k in models_selected}

    models = [v["name"] for v in metrics.values()]
    accuracy = [v["accuracy"] for v in metrics.values()]
    precision = [v["precision"] for v in metrics.values()]
    recall = [v["recall"] for v in metrics.values()]
    f1 = [v["f1"] for v in metrics.values()]

    # =================================================
    # 1. BARRAS AGRUPADAS (COMPARACIÓN DIRECTA)
    # =================================================
    fig1 = go.Figure()
    fig1.add_bar(x=models, y=accuracy, name="Accuracy")
    fig1.add_bar(x=models, y=precision, name="Precision")
    fig1.add_bar(x=models, y=recall, name="Recall")
    fig1.add_bar(x=models, y=f1, name="F1-score")

    fig1.update_layout(
        **HMI_LAYOUT,
        title_text="Comparación de Métricas por Modelo",
        barmode="group",
        yaxis=dict(range=[0.8, 0.92])
    )

    # =================================================
    # 2. RADAR (PERFIL DE RENDIMIENTO)
    # =================================================
    radar_metrics = ["Accuracy", "Precision", "Recall", "F1-score"]
    fig2 = go.Figure()

    for v in metrics.values():
        fig2.add_trace(go.Scatterpolar(
            r=[v["accuracy"], v["precision"], v["recall"], v["f1"]],
            theta=radar_metrics,
            fill="toself",
            name=v["name"]
        ))

    fig2.update_layout(
        **HMI_LAYOUT,
        title_text="Perfil de Rendimiento por Modelo",
        polar=dict(radialaxis=dict(range=[0.8, 0.92]))
    )
    # =========================
    # 3. TABLA COMPARATIVA (ABREVIADA + RESALTADA ✅)
    # =========================

    model_labels = ["LogReg", "SVM", "NB"]

    fmt = lambda x: f"{x:.3f}"

    fig3 = go.Figure(data=[go.Table(

        columnorder=[1, 2, 3, 4, 5],
        columnwidth=[100, 90, 90, 90, 90],  # control claro

        header=dict(
            values=[
                "<b>Modelo</b>",
                "Acc",
                "Prec",
                "Rec",
                "<b>F1</b>"
            ],
            fill_color=[
                "#0f2430",  # ✅ color distinto para header "Modelo"
                "#0f1a24",
                "#0f1a24",
                "#0f1a24",
                "#0f1a24"
            ],
            font=dict(color="#00d1ff", size=13),
            align="center",
            height=36
        ),

        cells=dict(
            values=[
                model_labels,
                [fmt(v) for v in accuracy],
                [fmt(v) for v in precision],
                [fmt(v) for v in recall],
                [fmt(v) for v in f1]
            ],
            align=["left", "center", "center", "center", "center"],
            font=dict(size=12),

            fill_color=[
                ["rgba(0,209,255,0.18)"] * len(model_labels),  # ✅ columna Modelo
                ["#0b141b"] * len(model_labels),
                ["#0b141b"] * len(model_labels),
                ["#0b141b"] * len(model_labels),
                ["rgba(0,255,166,0.15)"] * len(model_labels)   # ✅ resaltar F1
            ],
            font_color=[
                ["#00d1ff"] * len(model_labels),  # ✅ texto Modelo
                ["#e9f1f5"] * len(model_labels),
                ["#e9f1f5"] * len(model_labels),
                ["#e9f1f5"] * len(model_labels),
                ["#e9f1f5"] * len(model_labels)
            ],
            height=30
        )
    )])

    fig3.update_layout(
        **HMI_LAYOUT,
        title_text="Tabla Comparativa de Métricas"
    )


    # =================================================
    # 4. HEATMAP DE MÉTRICAS
    # =================================================
    metric_matrix = np.array([accuracy, precision, recall, f1])

    fig4 = go.Figure(data=go.Heatmap(
        z=metric_matrix,
        x=models,
        y=radar_metrics,
        colorscale=[[0, "#0b141b"], [0.5, "#00d1ff"], [1, "#00ffa6"]],
        text=np.round(metric_matrix, 3),
        texttemplate="%{text}",
        colorbar=dict(title="Score")
    ))
    fig4.update_layout(
        **HMI_LAYOUT,
        title_text="Heatmap de Métricas por Modelo"
    )

    # =================================================
    # 5. RANKING POR F1-SCORE ✅ NUEVO
    # =================================================
    order = np.argsort(f1)[::-1]
    fig5 = go.Figure(
        go.Bar(
            x=[f1[i] for i in order],
            y=[models[i] for i in order],
            orientation="h"
        )
    )
    fig5.update_layout(
        **HMI_LAYOUT,
        title_text="Ranking de Modelos por F1-score"
    )

    # =================================================
    # 6. PRECISION vs RECALL ✅ NUEVO
    # =================================================
    fig6 = go.Figure()

    # 1️⃣ Puntos SIN texto
    fig6.add_trace(go.Scatter(
        x=recall,
        y=precision,
        mode="markers",
        marker=dict(size=14, color="#00ffa6"),
        name="Modelos"
    ))

    # 2️⃣ Etiquetas COMO annotations (NO se recortan)
    annotations = []
    for x, y, label in zip(recall, precision, models):
        annotations.append(dict(
            x=x,
            y=y,
            text=label,
            showarrow=True,
            arrowhead=7,
            ax=20,     # desplazamiento horizontal
            ay=-20,    # desplazamiento vertical
            font=dict(size=12, color="#e9f1f5"),
            bgcolor="rgba(15,26,36,0.85)",
            borderpad=4
        ))

    fig6.update_layout(
        **HMI_LAYOUT,
        title_text="Precision vs Recall",
        xaxis=dict(title="Recall"),
        yaxis=dict(title="Precision"),
        annotations=annotations
    )



    return fig1, fig2, fig3, fig4, fig5, fig6
