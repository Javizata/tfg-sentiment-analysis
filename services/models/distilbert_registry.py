import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import gc

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

DISTILBERT_MODELS = {}
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_distilbert_models():
    for folder in os.listdir(ARTIFACTS_DIR):
        if folder.startswith("distilbert") and folder.endswith("_model"):
            model_path = os.path.join(ARTIFACTS_DIR, folder)

            if folder in DISTILBERT_MODELS:
                continue

            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForSequenceClassification.from_pretrained(model_path)
            model.to(DEVICE)
            model.eval()

            DISTILBERT_MODELS[folder] = {
                "tokenizer": tokenizer,
                "model": model
            }
def unload_distilbert_models():
    """
    Libera todos los modelos DistilBERT de memoria
    (NECESARIO en Windows antes de borrar archivos)
    """
    global DISTILBERT_MODELS

    for entry in DISTILBERT_MODELS.values():
        model = entry.get("model")
        if model is not None:
            del model

    DISTILBERT_MODELS.clear()

    torch.cuda.empty_cache()
    gc.collect()

    print("🧹 DistilBERT liberado de memoria")
    
def predict_distilbert(text, model_key):
    entry = DISTILBERT_MODELS[model_key]

    tokenizer = entry["tokenizer"]
    model = entry["model"]

    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(DEVICE)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1).cpu().numpy()[0]

    sentiment = "Positive" if probs[1] > probs[0] else "Negative"
    confidence = float(max(probs))

    return sentiment, confidence, probs.tolist()