# Heart Disease Prediction Project

Este proyecto tiene como objetivo predecir el riesgo de enfermedad cardíaca utilizando técnicas de **Machine Learning supervisado**, integrando un flujo completo que va desde el análisis de datos hasta una interfaz interactiva para el usuario.

---

# Arquitectura del Proyecto

El proyecto sigue una arquitectura modular que separa claramente las etapas de experimentación, desarrollo y despliegue:

```
heart-disease-project/
│
├── data/                      # Datos (raw y procesados)
│
├── notebooks/                 # Análisis exploratorio y experimentos
│
├── src/                       # Lógica reutilizable
│   ├── preprocessing.py
│   ├── features.py
│   ├── train.py
│   ├── evaluate.py
│
├── models/                    # Modelos entrenados
│
├── backend/                   # API (FastAPI)
│   ├── main.py
│   ├── schemas.py
│
├── frontend/                  # Interfaz (Streamlit)
│   ├── streamlit_app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

### Descripción general

* **notebooks/**: desarrollo experimental (EDA, pruebas de modelos)
* **src/**: implementación formal del pipeline
* **models/**: almacenamiento del modelo final entrenado
* **backend/**: API para servir el modelo
* **frontend/**: aplicación interactiva en Streamlit

---

# Creación del entorno virtual

Se recomienda trabajar en un entorno virtual para aislar las dependencias del proyecto.

### 1. Crear entorno

```bash
python -m venv venv
```

---

### 2. Activar entorno

#### En Windows (Git Bash):

```bash
source venv/Scripts/activate
```

#### En Windows (PowerShell):

```bash
venv\Scripts\activate
```

---

### 3. Verificación

Si el entorno está activo, verás algo como:

```
(venv)
```

---

# Instalación de dependencias

Una vez activado el entorno, instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

---

# Ejecución del Frontend (Streamlit)

Para visualizar la aplicación interactiva:

```bash
streamlit run frontend/streamlit_app.py
```

---

###  Acceso

Una vez ejecutado, la aplicación se abrirá automáticamente en el navegador en:

```
http://localhost:8501
```

---

#  Flujo de uso

1. El usuario ingresa sus datos en la interfaz
2. El frontend procesa la información
3. (Opcional) Se envía al backend para predicción
4. Se muestra el riesgo estimado de enfermedad cardíaca

---

#  Tecnologías utilizadas

* Python
* Scikit-learn
* Pandas / NumPy
* Streamlit
* FastAPI (backend)
* Joblib

---

#  Notas importantes

* El entorno virtual (`venv/`) no se incluye en el repositorio


---

#  Autores

* Alejandro Gutiérrez Muñoz
* Manuela Valencia Franco
* Alejandro Vásquez Sánchez

---

#  Futuro trabajo

* Mejora de modelos (deep learning, tuning)
* Deploy en la nube
* Integración completa backend-frontend
* Interpretabilidad del modelo (SHAP, LIME)

---
