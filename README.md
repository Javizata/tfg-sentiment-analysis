# Sentiment Analysis Platform

A web application for training, deploying and comparing sentiment classification models for movie reviews. It combines classic Machine Learning models (Logistic Regression, Linear SVM, Naive Bayes) with Transformer models (DistilBERT), and integrates a GitLab CI/CD pipeline for remote training and artifact management.

Developed as a Bachelor's Final Project (TFG).

## Description

The application covers the full model lifecycle within a single interface:

- Remote training of the classic models through a GitLab CI/CD pipeline, with live log streaming to the browser.
- Automatic download and installation of the resulting artifacts (models and evaluation metrics) once the pipeline completes.
- Upload of DistilBERT models, trained separately in a notebook, as a `.zip` package.
- Comparison of model performance through interactive dashboards.
- Real-time inference: a review can be evaluated by several models simultaneously, returning sentiment, confidence and probability distribution.

## Models

Two families of models are supported:

- **Classic ML** — Logistic Regression, Linear SVM and Naive Bayes, trained on IMDB with a TF-IDF representation and spaCy-based text preprocessing (cleaning and lemmatization).
- **Transformers** — DistilBERT fine-tuned on IMDB, and a second DistilBERT fine-tuned on SST-2.

### Evaluation metrics

Results on the held-out test sets:

| Model | Type | Accuracy | Precision | Recall | F1-score |
|-------|------|:--------:|:---------:|:------:|:--------:|
| DistilBERT (IMDB) | Transformer | 0.914 | 0.905 | 0.924 | 0.914 |
| DistilBERT (SST-2 fine-tuned) | Transformer | 0.906 | 0.895 | 0.923 | 0.909 |
| Logistic Regression | Classic ML | 0.877 | 0.865 | 0.893 | 0.879 |
| Linear SVM | Classic ML | 0.870 | 0.866 | 0.874 | 0.870 |
| Naive Bayes | Classic ML | 0.846 | 0.832 | 0.864 | 0.848 |

## Architecture

The application is built with Flask and Flask-SocketIO. HTTP routing is organized into Blueprints, while business logic is isolated in a dedicated services layer. Real-time communication (pipeline logs, state updates and inference results) uses Socket.IO namespaces (`/pipeline`, `/model_info`, `/stats`). A shared in-memory `APP_STATE` tracks which models are available and loaded.

```
App/
├── app.py                 # Application factory and entry point
├── config.py              # Configuration
├── app_state.py           # Shared in-memory application state
├── helpers.py             # Socket.IO instance
├── blueprints/            # HTTP routes and Socket.IO event handlers
│   ├── main/              # Pages (home, model info, graphs, review)
│   ├── pipeline/          # Training trigger and model upload
│   ├── models/            # Model selection and state
│   └── stats/             # Dashboards and inference events
├── services/              # Business logic
│   ├── models/            # Classic and DistilBERT registries, upload, state
│   ├── pipelines/         # GitLab runner, log streaming, artifact handling
│   └── stats/             # Plotly charts, metrics loading, prediction
├── templates/             # Jinja2 views
├── static/                # CSS and images
├── artifacts/             # Trained models, metrics and training notebook
└── docs/diagramas/        # UML diagrams
```

## Tech Stack

- **Backend:** Flask, Flask-SocketIO, eventlet
- **Classic ML:** scikit-learn, spaCy, joblib
- **Deep Learning:** Transformers, PyTorch (DistilBERT)
- **Data and visualization:** pandas, NumPy, Plotly, matplotlib, datasets
- **MLOps:** GitLab CI/CD and GitLab REST API
- **Frontend:** Jinja2, HTML/CSS, Socket.IO client

## Requirements

- Python 3.10 or higher
- pip and a virtual environment (recommended)

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd App

# Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download the spaCy English model
python -m spacy download en_core_web_sm
```

## Configuration

The GitLab CI/CD integration (remote training) requires the following environment variables:

```bash
# Windows (PowerShell)
$env:GITLAB_TOKEN = "your_gitlab_token"
$env:GITLAB_PROJECT_ID = "your_project_id"

# macOS / Linux
export GITLAB_TOKEN="your_gitlab_token"
export GITLAB_PROJECT_ID="your_project_id"
```

These variables are only needed to launch the remote training pipeline. The application can still run, load uploaded DistilBERT models and perform inference without them. For production, set a `SECRET_KEY` environment variable instead of relying on the default value.

## Usage

```bash
python app.py
```

The application is served at `http://localhost:5000`.

Typical workflow:

1. From the home page, choose to train classic models (via GitLab) or upload DistilBERT models.
2. Trigger a GitLab pipeline (logs are streamed live) or upload a `.zip` of Transformer models.
3. Select the models to work with.
4. Analyze a review to obtain predictions from every selected model, or open the dashboards to compare performance.

## Model Training

The DistilBERT models are trained in `artifacts/Sentiment_Analysis_training_DistilBERT.ipynb`, which can be downloaded from the application. The classic models are trained in the GitLab CI/CD pipeline and exported as `.pkl` artifacts together with a `metrics.json` report.

## Documentation

UML diagrams (actors, use cases, packages, components, classes, deployment, sequence, activity and state) are available under `docs/diagrams/`.
