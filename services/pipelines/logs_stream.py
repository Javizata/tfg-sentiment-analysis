import os
import requests
import time
from helpers import socketio
from services.pipelines.artifacts import download_artifacts

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")

job_last_size = {}

def follow_pipeline_logs(pipeline_id):
    base = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}"
    jobs_url = f"{base}/pipelines/{pipeline_id}/jobs"

    while True:
        resp = requests.get(jobs_url, headers={"PRIVATE-TOKEN": GITLAB_TOKEN})
        if resp.status_code != 200:
            break

        jobs = resp.json()
        all_done = True

        for job in jobs:
            job_id = job["id"]
            job_name = job["name"]
            job_status = job["status"]

            # LOGS:
            trace_url = f"{base}/jobs/{job_id}/trace"
            trace_resp = requests.get(trace_url, headers={"PRIVATE-TOKEN": GITLAB_TOKEN})

            if trace_resp.status_code == 200:
                text = trace_resp.text
                prev = job_last_size.get(job_id, 0)
                new = text[prev:]
                job_last_size[job_id] = len(text)

                if new:
                    log_to_send = new
                else:
                    log_to_send = ""

                socketio.emit(
                    "job_log",
                    {"job": job_name, "status": job_status, "log": log_to_send},
                    namespace="/pipeline"
                )

                socketio.sleep(1)


            if job_status not in ["success", "failed", "canceled"]:
                all_done = False

        if all_done:
            # Buscar job terminado con éxito
            finished = next((j for j in jobs if j["status"] == "success"), None)

            if finished:
                download_artifacts(finished["id"])
            else:
                socketio.emit(
                    "error",
                    {"message": "La pipeline falló."},
                    namespace="/pipeline"
                )            
                socketio.sleep(2)


            break

        time.sleep(2)