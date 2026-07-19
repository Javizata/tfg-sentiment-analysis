import os, time
import shutil
import glob
import joblib
import spacy
import gc
from app_state import APP_STATE
from services.stats.metrics import load_classic_metrics

# === IN-MEMORY REGISTRY ===
NLP = None
VECTORIZER = None
MODELS = {}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")


def load_classic_models():
    global NLP, VECTORIZER, MODELS

    APP_STATE["classic_models"] = False

    # Load spaCy only once
    if NLP is None:
        print("Loading spaCy model")
        NLP = spacy.load("en_core_web_sm")

    # Search for artifacts
    artifact_jobs = sorted(
        glob.glob(os.path.join(ARTIFACTS_DIR, "artifacts_job_*")),
        key=os.path.getmtime,
        reverse=True
    )

    if not artifact_jobs:
        print(" No classic models found")
        _update_ready_state()
        return

    latest = artifact_jobs[0]
    model_dir = os.path.join(latest, "model")

    # Vectorizer
    if VECTORIZER is None:
        VECTORIZER = joblib.load(
            os.path.join(model_dir, "vectorizer_imdb.pkl")
        )

    # Classic models
    for file in os.listdir(model_dir):
        if file.endswith(".pkl") and file != "vectorizer_imdb.pkl":
            model_name = file.replace(".pkl", "")
            if model_name not in MODELS:
                MODELS[model_name] = joblib.load(
                    os.path.join(model_dir, file)
                )
                print(f" Classic model loaded: {model_name}")

    APP_STATE["classic_models"] = len(MODELS) > 0
    
    load_classic_metrics(model_dir)
    _update_ready_state()

def unload_classic_models():
    """
    Frees all classic models and the vectorizer from memory.
    Useful when a new artifacts_job arrives to force reload.
    """
    global VECTORIZER, MODELS

    # Remove classic models from memory
    for name in list(MODELS.keys()):
        del MODELS[name]
    MODELS.clear()

    # Remove vectorizer
    if VECTORIZER is not None:
        del VECTORIZER
        VECTORIZER = None

    # Note: NLP (spaCy) remains loaded since it does not change between jobs

    APP_STATE["classic_models"] = False
    _update_ready_state()

    gc.collect()
    print(" Classic models and vectorizer unloaded")

def clean_old_classic_models():
    """
    Removes all job folders in artifacts/
    """
    unload_classic_models()
    time.sleep(2)
    for entry in os.listdir(ARTIFACTS_DIR):
        if entry.startswith("artifacts_job_") and os.path.isdir(
            os.path.join(ARTIFACTS_DIR, entry)
        ):
            shutil.rmtree(os.path.join(ARTIFACTS_DIR, entry))
            print(f" Removed old classic model: {entry}")
            
def _update_ready_state():
    APP_STATE["ready"] = (
        APP_STATE["classic_ready"] or APP_STATE["distilbert_ready"]
    )