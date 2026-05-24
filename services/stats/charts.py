import numpy as np
import plotly.graph_objs as go
from app_state import APP_STATE

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

def cargar_todo(models_selected:list = ["logistic_imdb","nb_imdb","svm_imdb","distilbert_imdb_model","distilbert_sst2_finetuned_model"]):
    models_selected = APP_STATE["models_to_use"]

    metrics_list = [
        APP_STATE["metrics"][k]
        for k in models_selected
        if k in APP_STATE["metrics"]
    ]
    
    valid_keys = [
        k for k in models_selected
        if k in APP_STATE["metrics"]
    ]

    NAME_MAP = {
        "logistic_imdb": "LogReg",
        "svm_imdb": "SVM",
        "nb_imdb": "NB",
        "distilbert_imdb_model": "DistilBERT",
        "distilbert_sst2_finetuned_model": "DistilBERT FT"
    }

    models = [NAME_MAP.get(k, APP_STATE["metrics"][k]["model"]) for k in valid_keys]
    accuracy = [v["accuracy"] for v in metrics_list]
    precision = [v["precision"] for v in metrics_list]
    recall = [v["recall"] for v in metrics_list]
    f1 = [v["f1_score"] for v in metrics_list]
    
    #BARRAS AGRUPADAS
    fig1 = go.Figure()
    fig1.add_bar(x=models, y=accuracy, name="Accuracy")
    fig1.add_bar(x=models, y=precision, name="Precision")
    fig1.add_bar(x=models, y=recall, name="Recall")
    fig1.add_bar(x=models, y=f1, name="F1-score")

    fig1.update_layout(
        **HMI_LAYOUT,
        title_text="Model Metrics Comparison",
        barmode="group",
        yaxis=dict(range=[0.8, 0.92])
    )

    #RADAR
    radar_metrics = ["Accuracy", "Precision", "Recall", "F1-score"]
    fig2 = go.Figure()

    for v in metrics_list:
        fig2.add_trace(go.Scatterpolar(
            r=[v["accuracy"], v["precision"], v["recall"], v["f1_score"]],
            theta=radar_metrics,
            fill="toself",
            name=v["model"]
        ))

    fig2.update_layout(
        **HMI_LAYOUT,
        title_text="Model Performance Profile",
        polar=dict(radialaxis=dict(range=[0.8, 0.92]))
    )
    
    #TABLA COMPARATIVA
    fmt = lambda x: f"{x:.3f}"

    fig3 = go.Figure(data=[go.Table(

        columnorder=[1, 2, 3, 4, 5],
        columnwidth=[100, 90, 90, 90, 90],  

        header=dict(
            values=[
                "<b>Model</b>",
                "Acc",
                "Prec",
                "Rec",
                "<b>F1</b>"
            ],
            fill_color=[
                "#0f2430",  
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
                models,
                [fmt(v) for v in accuracy],
                [fmt(v) for v in precision],
                [fmt(v) for v in recall],
                [fmt(v) for v in f1]
            ],
            align=["left", "center", "center", "center", "center"],
            font=dict(size=12),

            fill_color=[
                ["rgba(0,209,255,0.18)"] * len(models),  
                ["#0b141b"] * len(models),
                ["#0b141b"] * len(models),
                ["#0b141b"] * len(models),
                ["rgba(0,255,166,0.15)"] * len(models)   
            ],
            font_color=[
                ["#00d1ff"] * len(models), 
                ["#e9f1f5"] * len(models),
                ["#e9f1f5"] * len(models),
                ["#e9f1f5"] * len(models),
                ["#e9f1f5"] * len(models)
            ],
            height=30
        )
    )])

    fig3.update_layout(
        **HMI_LAYOUT,
        title_text="Model Metrics Comparison Table"
    )

    #HEATMAP DE MÉTRICAS
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
        title_text="Metrics Heatmap by Model"
    )

    #RANKING POR F1-SCORE 
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
        title_text="Model Ranking by F1 Score"
    )

    #PRECISION vs RECALL
    fig6 = go.Figure()

    fig6.add_trace(go.Scatter(
        x=recall,
        y=precision,
        mode="markers",
        marker=dict(size=14, color="#00ffa6"),
        name="Modelos"
    ))

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
