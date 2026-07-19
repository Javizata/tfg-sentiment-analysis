# 1. Diagrama de actores

Identifica las entidades (humanas y externas) que interactúan con el sistema.

- **Analista / Usuario**: actor humano principal, usa la interfaz web.
- **GitLab CI/CD**: sistema externo que ejecuta el pipeline de entrenamiento de los
  modelos clásicos y devuelve los artefactos.
- **Hugging Face**: fuente externa de datasets y modelos preentrenados (usada en el
  notebook de entrenamiento de DistilBERT).

```mermaid
flowchart LR
    Analista([" Analista / Usuario"]):::human
    System["Sistema de Análisis de Sentimiento"]
    GitLab(["GitLab CI/CD"]):::ext
    HF(["Hugging Face"]):::ext

    Analista --> System
    System <--> GitLab
    System <-.-> HF

    classDef human fill:#cdeffd,stroke:#0077b6,color:#023047;
    classDef ext fill:#ffe5b4,stroke:#e07a00,color:#3a2a00;
```
