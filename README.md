# Proyectos-Fisica-USC

Este repositorio contiene proyectos desarrollados en el marco del Grado en Física en la Universidad Santiago de Compostela (USC). Cada proyecto aplica herramientas computacionales para simular fenómenos físicos o aplicar modelos de aprendizaje automático.

---

## 📁 Estructura del repositorio

### 1. `Simulacion-Historia-Biofisica-Tierra`

Proyecto de simulación visual que representa distintas etapas de la historia biofísica de la Tierra, desde su formación hasta la aparición de vida compleja.

#### 📂 Contenido

- `Trabajo_Simulacion_Historia_Biofisica_Tierra.pdf`: Informe explicativo detallado del proyecto (metodología, desarrollo y resultados).
- `Códigos/`: Carpeta con los scripts de Python que implementan la simulación usando `pygame`.

#### 🛠 Tecnologías utilizadas

- Python 3.x  
- Librerías: `pygame`, `random`, `math`

#### ▶️ Cómo ejecutar

```bash
cd Simulacion-Historia-Biofisica-Tierra/codigos
python main.py
```


### 2. `Machine-Learning-GTZAN-Clasificacion_Generos_Musicales`

Proyecto de clasificación automática de géneros musicales utilizando técnicas de aprendizaje automático y redes neuronales, con el dataset **GTZAN**. El desarrollo se realiza en un entorno de Jupyter Notebook.

#### 📂 Contenido

- `Clasificacion_GTZAN.ipynb`: Notebook de Jupyter con todo el código fuente, incluyendo:
  - Extracción de características del audio (MFCC, Chroma, etc.).
  - Preprocesamiento de datos.
  - Construcción y entrenamiento del modelo.
  - Evaluación y visualización de resultados.

- `Clasificacion_GTZAN_Output.pdf`: Versión en PDF del notebook, útil para revisión sin necesidad de ejecutar el entorno.

> ⚠️ **Nota**: Este proyecto requiere el dataset [GTZAN](http://marsyas.info/downloads/datasets.html), que **no está incluido en el repositorio** por motivos de licencia y tamaño. Debes descargarlo manualmente y ubicarlo en la ruta esperada por el notebook (ver instrucciones dentro del mismo).

#### 🎧 Géneros musicales clasificados

- blues
- classical
- country
- disco
- hiphop
- jazz
- metal
- pop
- reggae
- rock

#### 🧰 Tecnologías utilizadas

- Python 3.x
- Jupyter Notebook
- Librerías:
  - `librosa` (procesamiento de audio)
  - `tensorflow` / `keras` (modelos de deep learning)
  - `scikit-learn` (modelos tradicionales y métricas)
  - `numpy`, `matplotlib`, `seaborn` (visualización y manipulación de datos)

#### ▶️ Cómo ejecutar

1. Descarga el dataset GTZAN desde [marsyas.info](http://marsyas.info/downloads/datasets.html).
2. Extrae el contenido en una carpeta (por ejemplo: `./genres/`) tal como se indica en el notebook.
3. Ejecuta el notebook:

```bash
cd Machine-Learning-GTZAN-Clasificacion_Generos_Musicales
jupyter notebook Clasificacion_GTZAN.ipynb

