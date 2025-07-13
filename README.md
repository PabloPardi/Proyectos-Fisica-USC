# Proyectos-Fisica-USC

Este repositorio contiene proyectos desarrollados en el marco del Grado en Física en la Universidad Santiago de Compostela (USC). Cada proyecto aplica herramientas computacionales para simular fenómenos físicos o aplicar modelos de aprendizaje automático.

---

## 📁 Estructura del repositorio

### 1. `Simulacion-Historia-Biofisica-Tierra`

Proyecto de simulación visual que representa distintas etapas de la historia biofísica de la Tierra, desde su formación hasta la aparición de vida compleja.

#### 📂 Contenido

- `Simulacion_Historia_Biofisica_Tierra.pdf`: Informe explicativo detallado del proyecto (metodología, desarrollo y resultados).
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

- `GTZAN_Clasificacion_musical.ipynb`: Notebook de Jupyter con todo el código fuente, incluyendo:
  - Extracción de características del audio (MFCC, Chroma, etc.).
  - Preprocesamiento de datos.
  - Construcción y entrenamiento del modelo.
  - Evaluación y visualización de resultados.

- `GTZAN_Clasificacion_musical_Output.pdf`: Versión en PDF del notebook, útil para revisión sin necesidad de ejecutar el entorno.

> ⚠️ **Nota**: Este proyecto requiere el dataset [GTZAN](https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification), que **no está incluido en el repositorio** por motivos de licencia y tamaño. Debes descargarlo manualmente y ubicarlo en la ruta esperada por el notebook (ver instrucciones dentro del mismo).

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

1. Descarga el dataset [GTZAN](https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification).
2. Ejecuta el notebook:

```bash
cd Machine-Learning-GTZAN-Clasificacion_Generos_Musicales
jupyter notebook Clasificacion_GTZAN.ipynb
```

### 3. `Estudio_de_la_decoherencia_y_determinismo_con_blancos_activos`

**Trabajo de Fin de Grado (TFG)** en Física presentado en la Universidad de Santiago de Compostela. Este estudio aborda en profundidad el fenómeno de la **decoherencia cuántica** y su relación con el **determinismo**, mediante el análisis de interferometría de onda-materia y la propuesta de implementación experimental en sistemas con **blancos activos**.

#### 📂 Contenido

- `Estudio_de_la_decoherencia_y_determinismo_con_blancos_activos.pdf`: Documento completo del TFG, incluyendo desarrollo teórico, cálculos, simulaciones y propuesta experimental.

#### 📄 Descripción

- Análisis detallado de la **decoherencia inducida por colisiones**.
- Aplicación del modelo teórico de Hornberger et al. a moléculas de fullereno y haces de electrones.
- Propuesta de experimento dentro del detector **ACTAR TPC** como entorno controlado para estudiar la pérdida de coherencia cuántica.
- Discusión sobre aplicaciones tecnológicas: computación cuántica, interferometría electrónica, holografía, etc.

#### 👤 Autoría

- **Autor**: Pablo Pardiñas Busto  
- **Tutora**: Beatriz Fernández Domínguez  
- Departamento de Física de Partículas, IGFAE – Universidade de Santiago de Compostela

