import streamlit as st
import base64
import requests
from pathlib import Path
import os

# ─── Config ────────────────────────────────────────────────────────────────────
BACKEND_URL = "http://localhost:8000/predict"

st.set_page_config(
    page_title="Snoopy CardioCheck",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Imágenes ─────────────────────────────────────────────────────────────────
def img_to_b64(path: str) -> str:
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except Exception:
        return ""

_DIR        = os.path.dirname(os.path.abspath(__file__))
IMG_DOCTOR  = img_to_b64(os.path.join(_DIR, "images/snoopy_doctor.png"))
IMG_HAPPY   = img_to_b64(os.path.join(_DIR, "images/snoopy_happy.jpeg"))
IMG_WORRIED = img_to_b64(os.path.join(_DIR, "images/snoopy_worried.jpeg"))

# ─── CSS (idéntico al tuyo) ────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700;800;900&family=Patrick+Hand&display=swap');

  :root {
    --cream:  #FDF6E3;
    --beige:  #F0E6C8;
    --brown:  #5C3D1E;
    --red:    #D94F3D;
    --sky:    #A8D8EA;
    --skydk:  #6BB5D6;
    --warm:   #F2A65A;
    --green:  #7DBF82;
    --text:   #3A2A1A;
    --shadow: rgba(92,61,30,0.18);
  }

  html, body, [class*="css"] {
    font-family: 'Patrick Hand', cursive !important;
    font-size: 18px !important;
    color: var(--text) !important;
    background-color: var(--cream) !important;
  }

  .stApp {
    background-color: var(--cream) !important;
    background-image: radial-gradient(circle, #c8b89a 1.2px, transparent 1.2px);
    background-size: 26px 26px;
    min-height: 100vh;
  }

  .main .block-container { max-width: 1200px; padding: 2rem 2rem 4rem 2rem; }

  .snoopy-header { text-align: center; margin-bottom: 1.5rem; }
  .snoopy-title {
    font-family: 'Baloo 2', cursive !important;
    font-weight: 900;
    font-size: 3.8rem !important;
    color: var(--brown);
    text-shadow: 4px 4px 0 var(--warm), 7px 7px 0 var(--shadow);
    letter-spacing: 2px; line-height: 1.1;
  }
  .snoopy-subtitle {
    font-family: 'Patrick Hand', cursive;
    font-size: 1.3rem !important;
    color: #7a5c3a;
    background: var(--beige);
    display: inline-block;
    padding: 5px 20px; border-radius: 20px;
    border: 2px solid var(--warm);
    margin-top: 0.4rem;
  }

  .snoopy-card {
    background: white;
    border-radius: 28px;
    border: 3px solid var(--brown);
    box-shadow: 6px 6px 0 var(--brown);
    padding: 1.8rem 1.2rem 1.5rem 1.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .snoopy-card::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 9px;
    background: repeating-linear-gradient(90deg, var(--red) 0, var(--red) 16px, white 16px, white 24px);
  }
  .snoopy-img-wrap {
    width: 210px; height: 210px;
    margin: 0 auto 1rem auto;
    border-radius: 50%; overflow: hidden;
    border: 4px solid var(--brown);
    box-shadow: 4px 4px 0 var(--shadow);
    background: var(--beige);
    display: flex; align-items: center; justify-content: center;
  }
  .snoopy-img-wrap img {
    width: 100%; height: 100%;
    object-fit: cover; object-position: top center;
    transition: transform 0.4s ease;
  }
  .snoopy-img-wrap img:hover { transform: scale(1.08); }

  .snoopy-name {
    font-family: 'Baloo 2', cursive !important;
    font-weight: 800; font-size: 1.6rem !important; color: var(--brown);
  }
  .mood-happy   { color: var(--green);  font-weight: 800; font-size: 1.15rem !important; line-height: 1.5; }
  .mood-worried { color: var(--red);    font-weight: 800; font-size: 1.15rem !important; line-height: 1.5; }
  .mood-waiting { color: var(--skydk);  font-weight: 800; font-size: 1.15rem !important; line-height: 1.5; }

  .bubble {
    border-radius: 18px; padding: 1rem 1.2rem;
    margin-top: 1.2rem; font-size: 1.1rem !important;
    line-height: 1.5; position: relative;
    box-shadow: 3px 3px 0 #ddd;
  }
  .bubble-happy   { background: #e8f8ea; border: 3px solid var(--green); color: #2a6b30; }
  .bubble-worried { background: #fff0ee; border: 3px solid var(--red);   color: #8b1a0e; }
  .bubble-waiting { background: #edf6fc; border: 3px solid var(--skydk); color: #1a5a7a; }
  .bubble::before {
    content: ""; position: absolute;
    top: -17px; left: 50%; transform: translateX(-50%);
    border-width: 0 10px 17px 10px; border-style: solid;
  }
  .bubble-happy::before   { border-color: transparent transparent var(--green) transparent; }
  .bubble-worried::before { border-color: transparent transparent var(--red) transparent; }
  .bubble-waiting::before { border-color: transparent transparent var(--skydk) transparent; }

  .fsec {
    background: white; border-radius: 22px;
    border: 3px solid var(--brown); box-shadow: 5px 5px 0 var(--shadow);
    padding: 0.8rem 1.6rem 1.2rem 1.6rem; margin-bottom: 1.5rem;
  }
  .fsec-title {
    font-family: 'Baloo 2', cursive !important;
    font-weight: 800; font-size: 1.4rem !important; color: var(--brown);
    margin-bottom: 0.6rem; padding-bottom: 0.3rem;
    border-bottom: 3px dashed var(--beige);
  }

  .vtag {
    display: inline-block; background: var(--beige); color: var(--brown);
    border: 1.5px solid var(--warm); border-radius: 8px;
    padding: 3px 12px;
    font-family: 'Patrick Hand', cursive;
    font-size: 1rem !important;
    font-weight: 700; margin-bottom: 4px;
  }

  input[disabled] {
      opacity: 1 !important;
      color: white !important;
      -webkit-text-fill-color: white !important;
      cursor: default !important;
  }
  div[data-testid="stNumberInput"]:has(input[disabled]) button {
      display: none !important;
  }

  label, .stSlider label, .stNumberInput label,
  .stCheckbox label, .stSelectbox label, .stRadio label, .stSelectSlider label {
    font-family: 'Patrick Hand', cursive !important;
    font-size: 1.15rem !important; color: var(--text) !important; font-weight: 600 !important;
  }
  .stCheckbox label { font-size: 1.1rem !important; }

  .stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; flex-wrap: wrap; }
  .stTabs [data-baseweb="tab"] {
    background: white; border-radius: 14px 14px 0 0 !important;
    border: 2px solid var(--brown) !important; border-bottom: none !important;
    font-family: 'Baloo 2', cursive !important; font-weight: 700 !important;
    font-size: 1.25rem !important; color: var(--brown) !important;
    padding: 12px 28px !important;
  }
  .stTabs [aria-selected="true"] { background: var(--brown) !important; color: white !important; }
  .stTabs [data-baseweb="tab-panel"] {
    border: 2px solid var(--brown); border-radius: 0 16px 16px 16px;
    background: white; padding: 1.2rem;
  }

  .stButton > button {
    font-family: 'Baloo 2', cursive !important; font-weight: 900 !important;
    font-size: 1.4rem !important; background: var(--brown) !important;
    color: white !important; border: 3px solid var(--brown) !important;
    border-radius: 50px !important; padding: 0.65rem 2rem !important;
    box-shadow: 5px 5px 0 var(--warm) !important;
    transition: all 0.15s ease !important; width: 100%; letter-spacing: 1px;
  }
  .stButton > button:hover {
    background: var(--red) !important; border-color: var(--red) !important;
    transform: translate(-2px,-2px) !important; box-shadow: 7px 7px 0 var(--warm) !important;
  }
  .stButton > button:active {
    transform: translate(2px,2px) !important; box-shadow: 2px 2px 0 var(--warm) !important;
  }

  .stAlert { border-radius: 14px !important; border: 2px solid var(--warm) !important; font-size: 1rem !important; }

  footer { visibility: hidden; }
  .snp-footer {
    text-align: center; color: #a08060; font-size: 1rem;
    margin-top: 2rem; padding-top: 1rem;
    border-top: 2px dashed var(--beige);
  }

  div[data-testid="stRadio"] label { color: var(--text) !important; font-size: 1.1rem !important; }
  div[data-testid="stRadio"] label span { color: var(--text) !important; }
  div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p { color: var(--text) !important; }

  div[data-testid="stAlert"] { background-color: #edf6fc !important; border: 2px solid var(--skydk) !important; border-radius: 14px !important; }
  div[data-testid="stAlert"] p, div[data-testid="stAlert"] span, div[data-testid="stAlert"] div { color: #1a5a7a !important; font-size: 1rem !important; }
  div[data-testid="stAlert"] svg { color: var(--skydk) !important; fill: var(--skydk) !important; }
  div[data-testid="stSliderTickBar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MAPAS DE TRADUCCIÓN: español del formulario → valores exactos del dataset
# ═══════════════════════════════════════════════════════════════════════════════

GENERAL_HEALTH_MAP = {
    "Muy mala":  "Poor",
    "Mala":      "Fair",
    "Regular":   "Good",
    "Buena":     "Very good",
    "Excelente": "Excellent",
}

AGE_CATEGORY_MAP = {
    "18-24": "Age 18 to 24", "25-29": "Age 25 to 29", "30-34": "Age 30 to 34",
    "35-39": "Age 35 to 39", "40-44": "Age 40 to 44", "45-49": "Age 45 to 49",
    "50-54": "Age 50 to 54", "55-59": "Age 55 to 59", "60-64": "Age 60 to 64",
    "65-69": "Age 65 to 69", "70-74": "Age 70 to 74", "75-79": "Age 75 to 79",
    "80+":   "Age 80 or older",
}

LAST_CHECKUP_MAP = {
    "En el último año":      "Within past year (anytime less than 12 months ago)",
    "En los últimos 2 años": "Within past 2 years (1 year but less than 2 years ago)",
    "En los últimos 5 años": "Within past 5 years (2 years but less than 5 years ago)",
    "Hace más de 5 años":    "5 or more years ago",
}

RACE_MAP = {
    "Blanco, no hispano":      "White only, Non-Hispanic",
    "Negro, no hispano":       "Black only, Non-Hispanic",
    "Hispano":                 "Hispanic",
    "Multirracial, no hispano":"Multiracial, Non-Hispanic",
    "Otra raza, no hispano":   "Other race only, Non-Hispanic",
}

SEX_MAP = {
    "Masculino": "Male",
    "Femenino":  "Female",
}

# Variables binarias del formulario actual que usan checkbox (True/False → "Yes"/"No")
def yn(val: bool) -> str:
    return "Yes" if val else "No"

# Variables multi-categoría: en tu formulario actual son checkbox simples,
# por lo que las mapeamos a los valores del dataset según si están marcadas o no.
# SmokerStatus y ECigaretteUsage tienen 4 niveles en el dataset — con checkbox
# solo podemos capturar "fuma/no fuma". Si quieres más granularidad en el futuro,
# cámbialos por st.selectbox.
SMOKER_MAP = {
    True:  "Current smoker - now smokes every day",
    False: "Never smoked",
}
ECIGARETTE_MAP = {
    True:  "Use them every day",
    False: "Never used e-cigarettes in my entire life",
}
# TetanusLast10Tdap y CovidPos también son checkbox en tu formulario actual
TETANUS_MAP = {
    True:  "Yes, received Tdap",
    False: "No, did not receive any tetanus shot in the past 10 years",
}
COVIDPOS_MAP = {
    True:  "Yes",
    False: "No",
}
# RemovedTeeth era checkbox "Dientes extraídos" en tab 3 (test_map)
REMOVED_TEETH_MAP = {
    True:  "6 or more, but not all",
    False: "None of them",
}
# HadDiabetes era checkbox en chronic_map
DIABETES_MAP = {
    True:  "Yes",
    False: "No",
}


# ─── Estado ────────────────────────────────────────────────────────────────────
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "probability" not in st.session_state:
    st.session_state.probability = None
if "error_msg" not in st.session_state:
    st.session_state.error_msg = None


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="snoopy-header">
  <div class="snoopy-title">Snoopy CardioCheck</div>
  <div class="snoopy-subtitle">¡Snoopy cuida tu corazón! · Ingresa tus datos y descubre tu riesgo</div>
</div>
""", unsafe_allow_html=True)


# ─── Layout ───────────────────────────────────────────────────────────────────
col_char, col_form = st.columns([1, 2.6], gap="large")

# ══════ SNOOPY ════════════════════════════════════════════════════════════════
with col_char:
    result = st.session_state.prediction_result

    if result is None:
        img_b64  = IMG_DOCTOR
        mood_cls = "mood-waiting"
        mood_txt = "¡Hola! Soy el<br>Dr. Snoopy"
        bub_cls  = "bubble bubble-waiting"
        bub_body = "Completa el formulario y presiona <b>¡Predecir!</b> para conocer tu riesgo cardíaco."
    elif result == "low":
        img_b64  = IMG_HAPPY
        mood_cls = "mood-happy"
        mood_txt = "¡Todo bien!<br>¡Sigue así!"
        bub_cls  = "bubble bubble-happy"
        prob_pct = round(st.session_state.probability * 100, 1)
        bub_body = f"<b>Bajo riesgo</b> de ataque cardíaco<br><br>Probabilidad estimada: <b>{prob_pct}%</b><br><br>¡Snoopy está muy orgulloso de ti!"
    else:
        img_b64  = IMG_WORRIED
        mood_cls = "mood-worried"
        mood_txt = "¡Atención!<br>Consulta a tu médico"
        bub_cls  = "bubble bubble-worried"
        prob_pct = round(st.session_state.probability * 100, 1)
        bub_body = f"<b>Alto riesgo</b> de ataque cardíaco<br><br>Probabilidad estimada: <b>{prob_pct}%</b><br><br>Snoopy te pide que consultes a un especialista cuanto antes."

    img_tag = f'<img src="data:image/png;base64,{img_b64}" alt="Snoopy"/>' if img_b64 else "🐶"
    st.markdown(f"""
    <div class="snoopy-card">
      <div class="snoopy-img-wrap">{img_tag}</div>
      <div class="snoopy-name">Dr. Snoopy</div>
      <div class="{mood_cls}">{mood_txt}</div>
      <div class="{bub_cls}">{bub_body}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.error_msg:
        st.error(f"🚨 {st.session_state.error_msg}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Esta herramienta es **solo orientativa** y no reemplaza el diagnóstico médico profesional.")


# ══════ FORMULARIO ════════════════════════════════════════════════════════════
with col_form:
    tab1, tab2, tab3, tab4 = st.tabs([
        "Métricas Físicas",
        "Condiciones de Salud",
        "Hábitos & Tests",
        "Demografía",
    ])

    # ── TAB 1 ──────────────────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="fsec"><div class="fsec-title">Medidas Corporales</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<span class="vtag">Peso (kg)</span>', unsafe_allow_html=True)
            weight = st.number_input("Peso", min_value=20.0, max_value=300.0, value=70.0, step=0.5, key="weight", label_visibility="collapsed")
        with c2:
            st.markdown('<span class="vtag">Altura (m)</span>', unsafe_allow_html=True)
            height = st.number_input("Altura", min_value=1.0, max_value=2.5, value=1.70, step=0.01, key="height", label_visibility="collapsed")
        with c3:
            bmi = round(weight / (height ** 2), 1)
            st.markdown('<span class="vtag">Índice de Masa Corporal</span>', unsafe_allow_html=True)
            st.number_input("IMC", value=bmi, disabled=True, key="bmi", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fsec"><div class="fsec-title">Bienestar Diario</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<span class="vtag">Días con malestar físico (últimos 30)</span>', unsafe_allow_html=True)
            physical_days = st.slider("Dias fisicos", 0, 30, 0, key="phys_days", label_visibility="collapsed")
        with c2:
            st.markdown('<span class="vtag">Días con malestar mental (últimos 30)</span>', unsafe_allow_html=True)
            mental_days = st.slider("Dias mentales", 0, 30, 0, key="ment_days", label_visibility="collapsed")
        with c3:
            st.markdown('<span class="vtag">Horas de sueño</span>', unsafe_allow_html=True)
            sleep = st.slider("Horas sueno", 1, 24, 7, key="sleep", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2 ──────────────────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="fsec"><div class="fsec-title">Condiciones Crónicas</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        chronic_friendly = {
            "HadStroke":             "Derrame cerebral",
            "HadDiabetes":           "Diabetes",
            "HadAsthma":             "Asma",
            "HadCOPD":               "Enfermedad pulmonar",
            "HadDepressiveDisorder": "Depresión",
            "HadKidneyDisease":      "Enfermedad renal",
            "HadArthritis":          "Artritis",
            "HadSkinCancer":         "Cáncer de piel",
        }
        chronic_vals = {}
        cols3 = [c1, c2, c3]
        for i, (k, v) in enumerate(chronic_friendly.items()):
            with cols3[i % 3]:
                st.markdown(f'<span class="vtag">{v}</span>', unsafe_allow_html=True)
                chronic_vals[k] = st.checkbox(v, key=f"chr_{k}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fsec"><div class="fsec-title">Dificultades Físicas</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        diff_friendly = {
            "DifficultyWalking":        "Dificultad al caminar",
            "DifficultyConcentrating":  "Dificultad al concentrarse",
            "DifficultyDressingBathing":"Dificultad al vestirse",
            "DifficultyErrands":        "Dificultad para diligencias",
            "DeafOrHardOfHearing":      "Dificultad auditiva",
            "BlindOrVisionDifficulty":  "Dificultad visual",
        }
        diff_vals = {}
        cols2 = [c1, c2]
        for i, (k, v) in enumerate(diff_friendly.items()):
            with cols2[i % 2]:
                st.markdown(f'<span class="vtag">{v}</span>', unsafe_allow_html=True)
                diff_vals[k] = st.checkbox(v, key=f"dif_{k}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 3 ──────────────────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="fsec"><div class="fsec-title">Hábitos de Vida</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<span class="vtag">Actividad física</span>', unsafe_allow_html=True)
            physical_activities = st.checkbox("Realiza actividad física regularmente")
            st.markdown('<span class="vtag">Fumador</span>', unsafe_allow_html=True)
            smoker = st.checkbox("Fumador/a")
        with c2:
            st.markdown('<span class="vtag">Cigarrillo electrónico</span>', unsafe_allow_html=True)
            ecigarette = st.checkbox("Usa cigarrillos electrónicos")
            st.markdown('<span class="vtag">Consumo de alcohol</span>', unsafe_allow_html=True)
            alcohol = st.checkbox("Consume alcohol")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fsec"><div class="fsec-title">Pruebas y Vacunación</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        test_friendly = {
            "ChestScan":        "Escaneo de tórax",
            "HIVTesting":       "Prueba de VIH",
            "FluVaxLast12":     "Vacuna gripe",
            "PneumoVaxEver":    "Vacuna neumococo",
            "TetanusLast10Tdap":"Vacuna tétanos",
            "CovidPos":         "COVID-19 positivo",
            "HighRiskLastYear": "Alto riesgo reciente",
            "RemovedTeeth":     "Extracción dental",
        }
        test_vals = {}
        cols3b = [c1, c2, c3]
        for i, (k, v) in enumerate(test_friendly.items()):
            with cols3b[i % 3]:
                st.markdown(f'<span class="vtag">{v}</span>', unsafe_allow_html=True)
                test_vals[k] = st.checkbox(v, key=f"tst_{k}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 4 ──────────────────────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="fsec"><div class="fsec-title">Información Personal</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<span class="vtag">Último chequeo médico</span>', unsafe_allow_html=True)
            last_checkup = st.selectbox("Ultimo chequeo", [
                "En el último año",
                "En los últimos 2 años",
                "En los últimos 5 años",
                "Hace más de 5 años",
            ], key="last_checkup", label_visibility="collapsed")
            st.markdown('<span class="vtag">Grupo de edad</span>', unsafe_allow_html=True)
            age_category = st.selectbox("Grupo edad", [
                "18-24","25-29","30-34","35-39","40-44","45-49",
                "50-54","55-59","60-64","65-69","70-74","75-79","80+"
            ], key="age_cat", label_visibility="collapsed")
            st.markdown('<span class="vtag">Salud general</span>', unsafe_allow_html=True)
            general_health = st.select_slider("Salud general",
                options=["Muy mala", "Mala", "Regular", "Buena", "Excelente"],
                value="Regular", key="gen_health", label_visibility="collapsed")
        with c2:
            st.markdown('<span class="vtag">Raza / Etnia</span>', unsafe_allow_html=True)
            race = st.selectbox("Raza etnia", [
                "Blanco, no hispano",
                "Negro, no hispano",
                "Hispano",
                "Multirracial, no hispano",
                "Otra raza, no hispano",
            ], key="race", label_visibility="collapsed")
            st.markdown('<span class="vtag">Sexo biológico</span>', unsafe_allow_html=True)
            sex = st.radio("Sexo", ["Masculino", "Femenino"], horizontal=True, key="sex", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fsec"><div class="fsec-title">Estado / Territorio</div>', unsafe_allow_html=True)
        st.markdown('<span class="vtag">Estado</span>', unsafe_allow_html=True)
        state = st.selectbox("Estado", [
            "Alabama","Alaska","Arizona","Arkansas","California","Colorado",
            "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho",
            "Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana",
            "Maine","Maryland","Massachusetts","Michigan","Minnesota",
            "Mississippi","Missouri","Montana","Nebraska","Nevada",
            "New Hampshire","New Jersey","New Mexico","New York",
            "North Carolina","North Dakota","Ohio","Oklahoma","Oregon",
            "Pennsylvania","Rhode Island","South Carolina","South Dakota",
            "Tennessee","Texas","Utah","Vermont","Virginia","Washington",
            "West Virginia","Wisconsin","Wyoming","District of Columbia",
            "Guam","Puerto Rico","Virgin Islands",
        ], key="state", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)


# ─── Botón ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<style>
  div[data-testid="column"]:has(div[data-testid="stButton"]) {
    display: flex;
    justify-content: center;
  }
  div[data-testid="stButton"] button { width: 480px !important; }
</style>
""", unsafe_allow_html=True)
_, bcol, _ = st.columns([1.8, 2, 1.8])
with bcol:
    if st.button("¡Predecir mi Riesgo Cardíaco!"):

        # ── Traducir valores del formulario al formato exacto del dataset ──────
        payload = {
            # Numéricas
            "PhysicalHealthDays": float(physical_days),
            "MentalHealthDays":   float(mental_days),
            "SleepHours":         float(sleep),
            "BMI":                float(bmi),
            "WeightInKilograms":  float(weight),
            "HeightInMeters":     float(height),

            # Sex
            "Sex": SEX_MAP[sex],

            # Binarias simples (checkbox → Yes/No)
            "PhysicalActivities":      yn(physical_activities),
            "AlcoholDrinkers":         yn(alcohol),
            "HadStroke":               yn(chronic_vals["HadStroke"]),
            "HadAsthma":               yn(chronic_vals["HadAsthma"]),
            "HadSkinCancer":           yn(chronic_vals["HadSkinCancer"]),
            "HadCOPD":                 yn(chronic_vals["HadCOPD"]),
            "HadDepressiveDisorder":   yn(chronic_vals["HadDepressiveDisorder"]),
            "HadKidneyDisease":        yn(chronic_vals["HadKidneyDisease"]),
            "HadArthritis":            yn(chronic_vals["HadArthritis"]),
            "DifficultyWalking":       yn(diff_vals["DifficultyWalking"]),
            "DifficultyConcentrating": yn(diff_vals["DifficultyConcentrating"]),
            "DifficultyDressingBathing": yn(diff_vals["DifficultyDressingBathing"]),
            "DifficultyErrands":       yn(diff_vals["DifficultyErrands"]),
            "DeafOrHardOfHearing":     yn(diff_vals["DeafOrHardOfHearing"]),
            "BlindOrVisionDifficulty": yn(diff_vals["BlindOrVisionDifficulty"]),
            "ChestScan":               yn(test_vals["ChestScan"]),
            "HIVTesting":              yn(test_vals["HIVTesting"]),
            "FluVaxLast12":            yn(test_vals["FluVaxLast12"]),
            "PneumoVaxEver":           yn(test_vals["PneumoVaxEver"]),
            "HighRiskLastYear":        yn(test_vals["HighRiskLastYear"]),

            # Multi-categoría: checkbox → valor más representativo del dataset
            "HadDiabetes":      DIABETES_MAP[chronic_vals["HadDiabetes"]],
            "SmokerStatus":     SMOKER_MAP[smoker],
            "ECigaretteUsage":  ECIGARETTE_MAP[ecigarette],
            "TetanusLast10Tdap": TETANUS_MAP[test_vals["TetanusLast10Tdap"]],
            "CovidPos":         COVIDPOS_MAP[test_vals["CovidPos"]],
            "RemovedTeeth":     REMOVED_TEETH_MAP[test_vals["RemovedTeeth"]],

            # Ordinales (traducción español → inglés del dataset)
            "GeneralHealth":   GENERAL_HEALTH_MAP[general_health],
            "AgeCategory":     AGE_CATEGORY_MAP[age_category],
            "LastCheckupTime": LAST_CHECKUP_MAP[last_checkup],

            # Nominales
            "RaceEthnicityCategory": RACE_MAP[race],
            "State": state,
        }

        with st.spinner("Snoopy está analizando tus datos..."):
            try:
                response = requests.post(BACKEND_URL, json=payload, timeout=10)
                response.raise_for_status()
                data = response.json()
                st.session_state.prediction_result = data["risk_level"]
                st.session_state.probability       = data["probability"]
                st.session_state.error_msg         = None

            except requests.exceptions.ConnectionError:
                st.session_state.error_msg = (
                    "No se pudo conectar con el backend. "
                    "Asegúrate de que FastAPI esté corriendo en http://localhost:8000"
                )
            except requests.exceptions.Timeout:
                st.session_state.error_msg = "El backend tardó demasiado en responder."
            except requests.exceptions.HTTPError as e:
                st.session_state.error_msg = (
                    f"Error del servidor ({e.response.status_code}): {e.response.text}"
                )
            except Exception as e:
                st.session_state.error_msg = f"Error inesperado: {str(e)}"

        st.rerun()

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="snp-footer">
  Snoopy CardioCheck · Proyecto académico de Machine Learning ·
  Los resultados son simulados y <b>no constituyen diagnóstico médico</b>.
</div>
""", unsafe_allow_html=True)