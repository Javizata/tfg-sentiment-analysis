import os
import requests
from helpers import socketio
from services.pipelines.logs_stream import follow_pipeline_logs

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")

def launch_pipeline():
    if not GITLAB_TOKEN or not GITLAB_PROJECT_ID:
        return False, "Faltan variables de entorno GITLAB_TOKEN o GITLAB_PROJECT_ID"

    url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/pipeline"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

    try:
        response = requests.post(url, headers=headers, data={"ref": "main"})

        if response.status_code != 201:
            return False, f"Error lanzando pipeline: {response.text}"

        pipeline_id = response.json()["id"]

        # Lanzar hilo del log
       
        socketio.start_background_task(follow_pipeline_logs, pipeline_id)


        return True, "Pipeline iniciada"

    except Exception as e:
        return False, f"Error interno: {e}"