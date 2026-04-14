import os
import glob
from app_state import APP_STATE


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

def update_app_state():
    classic_zips = glob.glob(
        os.path.join(ARTIFACTS_DIR, "artifacts_job_*.zip")
    )

    classic_folders = [
        f for f in glob.glob(os.path.join(ARTIFACTS_DIR, "artifacts_job_*"))
        if os.path.isdir(f)
    ]

    distilbert_folders = [
        f for f in glob.glob(os.path.join(ARTIFACTS_DIR, "distilbert_*_model"))
        if os.path.isdir(f)
    ]

    APP_STATE["classic_zip_pending"] = len(classic_zips) > 0
    APP_STATE["classic_ready"] = len(classic_folders) > 0
    APP_STATE["distilbert_ready"] = len(distilbert_folders) > 0
    
    print("PID:", os.getpid())
    print("APP_STATE:", APP_STATE)

    APP_STATE["ready"] = (
        APP_STATE["classic_ready"] or APP_STATE["distilbert_ready"]
    )