import pickle
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.preprocessing import preprocess
from backend.schemas import PatientFeatures, PredictionResponse

# ── Importar src/ ─────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ── Cargar paquete del modelo ─────────────────────────────────────────────────
MODEL_PATH = ROOT / "model" / "best_model.pkl"

try:
    with open(MODEL_PATH, "rb") as f:
        paquete = pickle.load(f)

    model             = paquete["modelo"]
    nombre_modelo     = paquete["nombre_modelo"]
    THRESHOLD         = paquete["umbral"]
    COLUMNAS_ESPERADAS = paquete["columnas_esperadas"]   

    print(f"Modelo cargado  : {nombre_modelo}")
    print(f"Umbral          : {THRESHOLD:.4f}")
    print(f"Columnas        : {len(COLUMNAS_ESPERADAS)}")

except FileNotFoundError:
    raise RuntimeError(
        f"Modelo no encontrado en {MODEL_PATH}.\n"
        "Coloca el archivo .pkl dentro de la carpeta models/."
    )

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Snoopy CardioCheck API 🐾",
    description=f"Predicción de riesgo cardíaco · modelo: {nombre_modelo}",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "modelo": nombre_modelo,
        "umbral": THRESHOLD,
        "columnas": len(COLUMNAS_ESPERADAS),
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionResponse, tags=["Predicción"])
def predict(patient: PatientFeatures):
    try:
        # 1. Preprocesar — pasa las columnas esperadas para garantizar el orden
        X = preprocess(patient.model_dump(), COLUMNAS_ESPERADAS)

        # 2. Probabilidad de clase positiva (ataque cardíaco = 1)
        probability = float(model.predict_proba(X)[0][1])

        # 3. Clasificar con el umbral extraído del paquete
        prediction = 1 if probability >= THRESHOLD else 0
        risk_level = "high" if prediction == 1 else "low"

        message = (
            "Alto riesgo detectado. Consulta a un médico especialista."
            if risk_level == "high"
            else "Bajo riesgo detectado. ¡Sigue con tus hábitos saludables!"
        )

        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            risk_level=risk_level,
            message=message,
        )

    except ValueError as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")