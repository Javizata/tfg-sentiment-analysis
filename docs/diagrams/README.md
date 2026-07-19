# Diagramas de Ingeniería del Software

Aplicación de Análisis de Sentimiento de reseñas de cine (Flask + Flask-SocketIO)
que compara modelos clásicos de ML (Logistic Regression, Naive Bayes, SVM) frente
a una red neuronal (DistilBERT IMDB / SST-2).

## Contenido

| Archivo | Diagrama |
|---|---|
| [01_actores.md](01_actores.md) | Diagrama de actores |
| [02_casos_uso.md](02_casos_uso.md) / [02_casos_uso.puml](02_casos_uso.puml) | Casos de uso |
| [03_paquetes.md](03_paquetes.md) | Paquetes |
| [04_componentes.md](04_componentes.md) | Componentes |
| [05_clases.md](05_clases.md) / [05_clases.puml](05_clases.puml) | Clases / módulos |
| [06_despliegue.md](06_despliegue.md) | Despliegue |
| [07_secuencia.md](07_secuencia.md) / [07_secuencia.puml](07_secuencia.puml) | Secuencia |
| [08_actividad.md](08_actividad.md) | Actividad |
| [09_estados.md](09_estados.md) | Estados (`APP_STATE`) |

## Imágenes generadas (PNG)

Las imágenes ya renderizadas están en la carpeta [img/](img/):

| Diagrama | Imagen |
|---|---|
| Actores | [img/actores.png](img/actores.png) |
| Casos de uso | [img/casos_uso.png](img/casos_uso.png) |
| Paquetes | [img/paquetes.png](img/paquetes.png) |
| Componentes | [img/componentes.png](img/componentes.png) |
| Clases / módulos | [img/clases.png](img/clases.png) |
| Despliegue | [img/despliegue.png](img/despliegue.png) |
| Secuencia · Analizar reseña | [img/secuencia_analizar_resena.png](img/secuencia_analizar_resena.png) |
| Secuencia · Lanzar pipeline | [img/secuencia_lanzar_pipeline.png](img/secuencia_lanzar_pipeline.png) |
| Secuencia · Subir DistilBERT | [img/secuencia_subir_distilbert.png](img/secuencia_subir_distilbert.png) |
| Actividad | [img/actividad.png](img/actividad.png) |
| Estados (`APP_STATE`) | [img/estados.png](img/estados.png) |

Cada diagrama está disponible también en **SVG** (vectorial) en la misma carpeta
`img/`, recomendado para insertar en Word con máxima calidad.

Las explicaciones detalladas de cada diagrama (con su origen en el código) están
en [explicaciones_diagramas.txt](explicaciones_diagramas.txt).

Para regenerarlas tras editar cualquier `.puml`:

```powershell
cd docs/diagramas
# PNG alta resolución
java -jar plantuml.jar -charset UTF-8 -config "_estilo.puml" -tpng -o "img" "0*.puml"
# SVG vectorial
java -jar plantuml.jar -charset UTF-8 -config "_estilo.puml" -tsvg -o "img" "0*.puml"
```

El estilo visual común está en `_estilo.puml`; aumenta `skinparam dpi` para más
resolución en PNG.

## Cómo visualizarlos / exportarlos

- **Mermaid (`.md`)**: instala la extensión *Markdown Preview Mermaid Support* en
  VS Code y abre la vista previa (`Ctrl+Shift+V`). También puedes pegar el código en
  https://mermaid.live para exportar a PNG/SVG.
- **PlantUML (`.puml`)**: instala la extensión *PlantUML* (requiere Graphviz/Java) o
  pega el código en https://www.plantuml.com/plantuml.

Para la memoria del TFG se recomienda exportar a SVG (vectorial) o PNG de alta
resolución.
