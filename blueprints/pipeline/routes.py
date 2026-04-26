
import os
from flask import Blueprint, render_template, flash, send_from_directory, abort
from services.pipelines.runner import launch_pipeline
from services.models.distilbert_upload import upload_distilbert_zip

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
pipeline_bp = Blueprint("pipeline", __name__)

@pipeline_bp.route("/trigger-pipeline", methods=["POST"])
def trigger_pipeline_route():

    ok, message = launch_pipeline()

    if not ok:
        flash(message, "danger")
        return render_template("pipeline_running.html")

    flash("Pipeline lanzada correctamente.", "success")
    return render_template("pipeline_running.html")


@pipeline_bp.route("/upload_distilbert", methods=["POST"])
def upload_distilbert():
    return upload_distilbert_zip()


@pipeline_bp.route("/download_distilbert_notebook", methods=["GET"])
def download_distilbert_notebook():
    filename = "Sentiment_Analysis_training_DistilBERT.ipynb"  

    file_path = os.path.join(ARTIFACTS_DIR, filename)

    if not os.path.exists(file_path):
        abort(404, description="Notebook no encontrado")

    return send_from_directory(
        ARTIFACTS_DIR,
        filename,
        as_attachment=True
    )
