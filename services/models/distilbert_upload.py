import os, time
import shutil
import zipfile

from flask import request, jsonify
from services.models.distilbert_registry import load_distilbert_models, unload_distilbert_models
from services.models.artifact_state import update_app_state
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

ALLOWED_EXTENSIONS = {"zip"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_old_distilbert_models():
    """
    Elimina todas las carpetas DistilBERT existentes en artifacts/
    """
    unload_distilbert_models()
    time.sleep(2)
    for entry in os.listdir(ARTIFACTS_DIR):
        if entry.startswith("distilbert_") and os.path.isdir(
            os.path.join(ARTIFACTS_DIR, entry)
        ):
            shutil.rmtree(os.path.join(ARTIFACTS_DIR, entry))
            print(f"🗑️ Eliminado modelo DistilBERT antiguo: {entry}")


def upload_distilbert_zip():
    clean_old_distilbert_models()
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only ZIP files are allowed"}), 400

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    zip_path = os.path.join(ARTIFACTS_DIR, file.filename)
    file.save(zip_path)

    # 🔓 Extraer ZIP en artifacts/
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(ARTIFACTS_DIR)

    os.remove(zip_path)
    load_distilbert_models()
    update_app_state()

    return jsonify({
        "message": "DistilBERT models uploaded and extracted successfully"
    }), 200