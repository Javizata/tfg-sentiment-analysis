import os
import glob
import joblib
import spacy
from app_state import APP_STATE

# === REGISTRO EN MEMORIA ===
NLP = None
VECTORIZER = None
MODELS = {}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")


def load_classic_models():
    global NLP, VECTORIZER, MODELS

    APP_STATE["classic_models"] = False

    # 1️⃣ Cargar spaCy una sola vez
    if NLP is None:
        print("🔹 Loading spaCy model")
        NLP = spacy.load("en_core_web_sm")

    # 2️⃣ Buscar artefactos
    artifact_jobs = sorted(
        glob.glob(os.path.join(ARTIFACTS_DIR, "artifacts_job_*")),
        key=os.path.getmtime,
        reverse=True
    )

    if not artifact_jobs:
        print("⚠️ No classic models found")
        _update_ready_state()
        return

    latest = artifact_jobs[0]
    model_dir = os.path.join(latest, "model")

    # 3️⃣ Vectorizador
    if VECTORIZER is None:
        VECTORIZER = joblib.load(
            os.path.join(model_dir, "vectorizer_imdb.pkl")
        )

    # 4️⃣ Modelos clásicos
    for file in os.listdir(model_dir):
        if file.endswith(".pkl") and file != "vectorizer_imdb.pkl":
            model_name = file.replace(".pkl", "")
            if model_name not in MODELS:
                MODELS[model_name] = joblib.load(
                    os.path.join(model_dir, file)
                )
                print(f"✅ Classic model loaded: {model_name}")

    APP_STATE["classic_models"] = len(MODELS) > 0
    _update_ready_state()


def _update_ready_state():
    APP_STATE["ready"] = (
        APP_STATE["classic_models"] or APP_STATE["distilbert_models"]
    )