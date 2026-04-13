import re
import emoji
import joblib
import spacy

def cargar_modelo(modelo: str ="logistic_imdb.pkl" ):
    print("Loading spaCy model...")
    nlp = spacy.load("en_core_web_sm")

    print("Loading trained model and vectorizer...")

    import os
    import glob

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

    artifact_jobs = sorted(
        glob.glob(os.path.join(ARTIFACTS_DIR, "artifacts_job_*")),
        key=os.path.getmtime,
        reverse=True
    )

    if not artifact_jobs:
        raise FileNotFoundError("No se encontraron carpetas artifacts_job_*")

    LATEST_JOB_DIR = artifact_jobs[0]

    VECTOR_PATH = os.path.join(
        LATEST_JOB_DIR,
        "model",
        "vectorizer_imdb.pkl"
    )
    MODEL_PATH = os.path.join(
    LATEST_JOB_DIR,
    "model",
    modelo
    )
    
    print("Model and vectorizer loaded successfully.")
    vectorizer = joblib.load(VECTOR_PATH)
    model = joblib.load(MODEL_PATH)
    return nlp,vectorizer, model

def clean_text(text):
    text = text.lower()
    text = emoji.demojize(text)
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text

def preprocess(text, nlp):
    doc = nlp(text)
    return " ".join(
        t.lemma_ for t in doc
        if not t.is_stop and t.is_alpha and len(t) > 1
    )

def predict_review(review, modelo:str = "logistic_imdb.pkl"):
    nlp,vectorizer, model = cargar_modelo(modelo)
    cleaned = clean_text(review)
    processed = preprocess(cleaned, nlp)

    X = vectorizer.transform([processed])
    prediction = model.predict(X)[0]

    sentiment = "Positive" if prediction == 1 else "Negative"

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X)[0]
        confidence = max(probabilities)
    else:
        probabilities = None
        confidence = None

    return sentiment, confidence, probabilities

