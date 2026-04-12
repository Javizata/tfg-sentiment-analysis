import numpy as np
import plotly.graph_objs as go

# =========================
# ESTILO GLOBAL PLOTLY (HMI)
# =========================

def cargar_todo():
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
        xaxis=dict(
            gridcolor="rgba(0,255,204,0.1)",
            zeroline=False
        ),
        yaxis=dict(
            gridcolor="rgba(0,255,204,0.1)",
            zeroline=False
    ))
    # -----------------
    # 1. Gráfico líneas
    # -----------------
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=[1, 2, 3],
        y=[3, 1, 6],
        mode="lines+markers",
        line=dict(color="#00ffa6", width=3),
        marker=dict(
            size=8,
            color="#00d1ff",
            line=dict(color="#0b1016", width=1)
        )
    ))

    fig1.update_layout(
        **{**HMI_LAYOUT, "title_text": "Gráfico de Líneas"}
    )
    # -----------------
    # 2. Gráfico barras
    # -----------------
    fig2 = go.Figure()
    fig2.add_bar(
        x=["A", "B", "C"],
        y=[10, 20, 15],
        marker=dict(
            color="#00d1ff",
            line=dict(color="#00ffa6", width=2)
        )
    )

    fig2.update_layout(
        **{**HMI_LAYOUT,
           "title_text": "Gráfico de Barras",
           "bargap": 0.35}
    )
    # -------------
    # 3. Tabla
    # -------------
    fig3 = go.Figure(data=[go.Table(
        header=dict(
            values=["Col 1", "Col 2", "Col 3", "Col 4", "Col 5", "Col 6"],
            fill_color="#0f1a24",
            font=dict(color="#00d1ff", size=13),
            align="left"
        ),
        cells=dict(
            values=[
                [1, 2, 3],
                ["A", "B", "C"],
                [1, 2, 2, 3],
                [1, 2, 3],
                [1, 3],
                [1, 2, 4, 5, 6, 7, 3]
            ],
            fill_color="#0b141b",
            font=dict(color="#e9f1f5", size=12),
            align="left"
        )
    )])

    fig3.update_layout(
        **{**HMI_LAYOUT, "title_text": "Tabla de Datos"}
    )
    # --------------------------
    # 4. Matriz de confusión ✅
    # --------------------------
    matriz = np.array([
        [50, 5],
        [3, 42]
    ])

    fig4 = go.Figure(data=go.Heatmap(
        z=matriz,
        x=["Pred Neg", "Pred Pos"],
        y=["Real Neg", "Real Pos"],

        # ✅ MOSTRAR NÚMEROS
        text=matriz,
        texttemplate="%{text}",
        textfont=dict(
            color="#e9f1f5",
            size=18
        ),

        colorscale=[
            [0, "#0b141b"],
            [0.5, "#00d1ff"],
            [1, "#00ffa6"]
        ],
        showscale=True,
        colorbar=dict(
            tickcolor="#e9f1f5",
            outlinecolor="rgba(0,0,0,0)"
        )
    ))

    fig4.update_layout(
        **{**HMI_LAYOUT, "title_text": "Matriz de Confusión"}
    )

    return fig1,fig2,fig3,fig4