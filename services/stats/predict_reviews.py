import re
import emoji
import services.models.model_registry as registry

def clean_text(text):
    text = text.lower()
    text = emoji.demojize(text)
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text


def preprocess(text):
    doc = registry.NLP(text)
    return " ".join(
        t.lemma_ for t in doc
        if not t.is_stop and t.is_alpha and len(t) > 1
    )


def predict_review(text, model_name):
    
    if registry.NLP is None or registry.VECTORIZER is None or not registry.MODELS:
        registry.load_classic_models()

    if model_name not in registry.MODELS:
        raise ValueError(f"Model not loaded: {model_name}")

    if model_name not in registry.MODELS:
        raise ValueError(f"Model not loaded: {model_name}")
    print("text",text)
    cleaned = clean_text(text)
    processed = preprocess(cleaned)

    X = registry.VECTORIZER.transform([processed])
    model = registry.MODELS[model_name]

    pred = model.predict(X)[0]
    sentiment = "Positive" if pred == 1 else "Negative"

    probs = model.predict_proba(X)[0] if hasattr(model, "predict_proba") else None
    confidence = float(max(probs)) if probs is not None else None

    return sentiment, confidence, probs