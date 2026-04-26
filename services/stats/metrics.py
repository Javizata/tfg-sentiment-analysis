import os, json
from app_state import APP_STATE

def load_classic_metrics(path):
    
    metrics_path = os.path.join(
        path, "metrics.json"
    )

    if not os.path.exists(metrics_path):
        return []

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    APP_STATE["metrics"]["logistic_imdb"] = metrics[0]
    APP_STATE["metrics"]["nb_imdb"] = metrics[1]
    APP_STATE["metrics"]["svm_imdb"] = metrics[2]    

    
def load_distilbert_metrics(path):
    
    metrics_path = os.path.join(
        path, "metrics.json"
    )

    if not os.path.exists(metrics_path):
        return []

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    
    APP_STATE["metrics"]["distilbert_imdb_model"] = metrics[0]
    
    metrics_path = os.path.join(
        path, "metrics_sst2_finetuned.json"
    )

    if not os.path.exists(metrics_path):
        return []

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    APP_STATE["metrics"]["distilbert_sst2_finetuned_model"] = metrics[0]

