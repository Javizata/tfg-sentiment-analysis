import os
import requests
from helpers import socketio

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")

def download_artifacts(job_id):
    url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/jobs/{job_id}/artifacts"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

    os.makedirs("artifacts", exist_ok=True)
    path = f"artifacts/job_{job_id}.zip"

    resp = requests.get(url, headers=headers, stream=True)

    if resp.status_code == 200:
        with open(path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        socketio.emit(
            "artifacts_ready",
            {"zip_path": path},
            namespace="/pipeline"
        )
    else:
        socketio.emit(
            "error",
            {"message": "No se pudieron descargar los artifacts."},
            namespace="/pipeline"
        )