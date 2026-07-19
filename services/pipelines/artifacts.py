import os
import requests
import zipfile
from helpers import socketio
from services.models.artifact_state import update_app_state
from services.models.model_registry import load_classic_models, clean_old_classic_models

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

def download_artifacts(job_id):
    url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/jobs/{job_id}/artifacts"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

    #Download ZIP
    resp = requests.get(url, headers=headers, stream=True)
    
    if resp.status_code != 200:
        socketio.emit(
            "error",
            {"message": "Could not download artifacts."},
            namespace="/pipeline"
        )
        return
    
    clean_old_classic_models()

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    zip_path = os.path.join(
        ARTIFACTS_DIR,
        f"artifacts_job_{job_id}.zip"
    )

    with open(zip_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    #Create destination folder with the same name
    extract_dir = os.path.join(
        ARTIFACTS_DIR,
        f"artifacts_job_{job_id}"
    )
    os.makedirs(extract_dir, exist_ok=True)

    #Extract ZIP INTO THAT FOLDER
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)

    #Delete ZIP
    os.remove(zip_path)

    #Update state + load models
    update_app_state()
    load_classic_models()
    socketio.emit(
        "artifacts_ready",
        {"job_id": job_id},
        namespace="/pipeline"
    )
    
