from flask import Blueprint, render_template, flash
from flask_socketio import emit
import os
import requests
import time
from threading import Thread
from helpers import socketio

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")

GITLAB_API_BASE = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}"
GITLAB_PIPELINE_URL = f"{GITLAB_API_BASE}/pipeline"

models_bp = Blueprint("models_bp", __name__)

# =====================================================
# ROUTES
# =====================================================


