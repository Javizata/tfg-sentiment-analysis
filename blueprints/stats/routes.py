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

stats_bp = Blueprint("stats", __name__)

# =====================================================
# ROUTES
# =====================================================

@stats_bp.route("/")
def index():
    return render_template(
        "init.html",
        title="Home",
        description="Application developed as a Bachelor's Final Project"
    )

@stats_bp.route("/model_info")
def model_info():
    return render_template("model_info.html", title="Models")

@stats_bp.route("/base")
def base():
    return render_template("base.html", title="Base")

# =====================================================
# LOG STREAMING
# =====================================================

job_last_size = {}

def follow_pipeline_logs(pipeline_id):
    jobs_url = f"{GITLAB_API_BASE}/pipelines/{pipeline_id}/jobs"

    while True:

        jobs_resp = requests.get(jobs_url, headers={"PRIVATE-TOKEN": GITLAB_TOKEN})
        if jobs_resp.status_code != 200:
            break

        jobs = jobs_resp.json()
        all_done = True

        for job in jobs:
            job_id = job["id"]
            job_name = job["name"]
            job_status = job["status"]

            # =========================
            # STREAM LOGS
            # =========================
            trace_url = f"{GITLAB_API_BASE}/jobs/{job_id}/trace"
            trace_resp = requests.get(trace_url, headers={"PRIVATE-TOKEN": GITLAB_TOKEN})

            if trace_resp.status_code == 200:
                log_text = trace_resp.text
                previous_size = job_last_size.get(job_id, 0)

                new_chunk = log_text[previous_size:]
                job_last_size[job_id] = len(log_text)

                if new_chunk and socketio:
                    
                    print("⚡ NEW LOG CHUNK ⚡")
                    print(new_chunk)

                    """socketio.emit(
                        "job_log",
                        {
                            "job": job_name,
                            "status": job_status,
                            "log": new_chunk
                        },
                        namespace="/pipeline"
                    )"""

            if job_status not in ["success", "failed", "canceled"]:
                all_done = False

        # =========================
        # IF EVERYTHING IS FINISHED
        # =========================
        if all_done:

            finished_job = next((j for j in jobs if j["status"] == "success"), None)

            if finished_job:
                download_artifacts(finished_job["id"])
            else:
                socketio.emit(
                    "error",
                    {"message": "The pipeline failed."},
                    namespace="/pipeline"
                )

            break

        time.sleep(2)

# =====================================================
# DOWNLOAD METRICS.JSON
# =====================================================

def download_artifacts(job_id):
    artifacts_url = f"{GITLAB_API_BASE}/jobs/{job_id}/artifacts"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

    # 📁 Create local folder if it does not exist
    os.makedirs("artifacts", exist_ok=True)

    # 📥 Download ZIP
    local_zip_path = os.path.join("artifacts", f"artifacts_job_{job_id}.zip")

    resp = requests.get(artifacts_url, headers=headers, stream=True)

    if resp.status_code == 200:
        with open(local_zip_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Artifacts downloaded: {local_zip_path}", flush=True)

        # (Optional) Emit event to Socket.IO
        socketio.emit(
            "artifacts_ready",
            {"zip_path": local_zip_path},
            namespace="/trigger-pipeline"
        )
    else:
        socketio.emit(
            "error",
            {"message": "Could not download artifacts"},
            namespace="/pipeline"
        )
# =====================================================
# TRIGGER PIPELINE
# =====================================================

@stats_bp.route("/trigger-pipeline", methods=["POST"])
def trigger_pipeline():

    if not GITLAB_TOKEN or not GITLAB_PROJECT_ID:
        raise ValueError("Missing GITLAB_TOKEN or GITLAB_PROJECT_ID in environment")

    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    data = {"ref": "main"}

    try:
        response = requests.post(GITLAB_PIPELINE_URL, headers=headers, data=data, timeout=10)

        if response.status_code != 201:
            flash(f"Error launching pipeline ({response.status_code}): {response.text}", "danger")
            return render_template("base.html")

        flash("Pipeline successfully launched.", "success")
        pipeline_id = response.json()["id"]

        # Reset log buffer
        global job_last_size
        job_last_size = {}

        # Start thread for logs + metrics
        thread = Thread(target=follow_pipeline_logs, args=(pipeline_id,))
        thread.daemon = True
        thread.start()

    except requests.exceptions.RequestException as e:
        flash(f"GitLab connection error: {str(e)}", "danger")

    return render_template("trigger-pipeline.html")