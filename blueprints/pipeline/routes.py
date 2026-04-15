from flask import Blueprint, render_template, flash
from services.pipelines.runner import launch_pipeline
from services.models.distilbert_upload import upload_distilbert_zip


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

