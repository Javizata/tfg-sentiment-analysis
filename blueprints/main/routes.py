from flask import Blueprint, render_template, flash
from flask_socketio import emit
import os
import requests
import time
from threading import Thread
from helpers import socketio


main = Blueprint(
    "main",
    __name__,
)

@main.route("/")
def index():
    return render_template(
        "init.html",
        title="Inicio",
        description="Aplicación desarrollada como Trabajo Fin de Grado"
    )

@main.route("/model_info")
def model_info():
    return render_template("model_info.html", title="Models")

@main.route("/base")
def base():
    return render_template("base.html", title="Base")

@main.route("/graphs")
def graphs():
    return render_template("graphs.html", title="Gráficos")

@main.route("/review")
def review():
    return render_template("review.html", title="Analisis")
