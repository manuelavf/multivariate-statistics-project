from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Any, Dict, List


# Binarias Yes/No
BINARY_COLS = [
    "PhysicalActivities", "HadStroke", "HadAsthma",
    "HadSkinCancer", "HadCOPD", "HadDepressiveDisorder", "HadKidneyDisease",
    "HadArthritis", "DeafOrHardOfHearing", "BlindOrVisionDifficulty",
    "DifficultyConcentrating", "DifficultyWalking", "DifficultyDressingBathing",
    "DifficultyErrands", "ChestScan", "AlcoholDrinkers", "HIVTesting",
    "FluVaxLast12", "PneumoVaxEver", "HighRiskLastYear",
]

# Ordinales con orden clínico
ORDINAL_MAPS: Dict[str, Dict[str, int]] = {
    "GeneralHealth": {
        "Poor": 0, "Fair": 1, "Good": 2, "Very good": 3, "Excellent": 4,
    },
    "AgeCategory": {
        "Age 18 to 24": 0, "Age 25 to 29": 1, "Age 30 to 34": 2,
        "Age 35 to 39": 3, "Age 40 to 44": 4, "Age 45 to 49": 5,
        "Age 50 to 54": 6, "Age 55 to 59": 7, "Age 60 to 64": 8,
        "Age 65 to 69": 9, "Age 70 to 74": 10, "Age 75 to 79": 11,
        "Age 80 or older": 12,
    },
    "LastCheckupTime": {
        "5 or more years ago": 0,
        "Within past 5 years (2 years but less than 5 years ago)": 1,
        "Within past 2 years (1 year but less than 2 years ago)": 2,
        "Within past year (anytime less than 12 months ago)": 3,
    },
    "RemovedTeeth": {
        "None of them": 0, "1 to 5": 1, "6 or more, but not all": 2, "All": 3,
    },
}

# Multi-categoría con semántica clínica
MULTI_CAT_MAPS: Dict[str, Dict[str, int]] = {
    "HadDiabetes": {
        "No": 0,
        "No, pre-diabetes or borderline diabetes": 1,
        "Yes, but only during pregnancy (female)": 1,
        "Yes": 2,
    },
    "SmokerStatus": {
        "Never smoked": 0,
        "Former smoker": 1,
        "Current smoker - now smokes some days": 2,
        "Current smoker - now smokes every day": 3,
    },
    "ECigaretteUsage": {
        "Never used e-cigarettes in my entire life": 0,
        "Not at all (right now)": 1,
        "Use them some days": 2,
        "Use them every day": 3,
    },
    "TetanusLast10Tdap": {
        "No, did not receive any tetanus shot in the past 10 years": 0,
        "Yes, received tetanus shot but not sure what type": 1,
        "Yes, received tetanus shot, but not Tdap": 2,
        "Yes, received Tdap": 3,
    },
    "CovidPos": {
        "No": 0,
        "Yes": 1,
        "Tested positive using home test without a health professional": 1,
    },
}

def preprocess(raw: Dict[str, Any], columnas_esperadas: List[str]) -> pd.DataFrame:
    row: Dict[str, Any] = {}

    # ── 1. Numéricas continuas ────────────────────────────────────────────────
    row["PhysicalHealthDays"] = float(raw["PhysicalHealthDays"])
    row["MentalHealthDays"]   = float(raw["MentalHealthDays"])
    row["SleepHours"]         = float(raw["SleepHours"])
    row["BMI"]                = float(raw["BMI"])
    row["WeightInKilograms"]  = float(raw["WeightInKilograms"])
    row["HeightInMeters"]     = float(raw["HeightInMeters"])

    # ── 2. Binarias Yes/No → 1/0 ──────────────────────────────────────────────
    for col in BINARY_COLS:
        val = raw.get(col, "No")
        if isinstance(val, bool):
            row[col] = int(val)
        elif isinstance(val, str):
            row[col] = 1 if val.strip().lower() == "yes" else 0
        else:
            row[col] = int(val)

    # ── 3. Sex (Female=0, Male=1) ──────────────────────────────────────────────
    sex_val = raw.get("Sex", "Female")
    if isinstance(sex_val, bool):
        row["Sex"] = int(sex_val)
    elif isinstance(sex_val, str):
        row["Sex"] = 1 if sex_val.strip().lower() == "male" else 0
    else:
        row["Sex"] = int(sex_val)

    # ── 4. Ordinales ──────────────────────────────────────────────────────────
    for col, mapping in ORDINAL_MAPS.items():
        val = raw.get(col, "")
        if val not in mapping:
            raise ValueError(
                f"Valor '{val}' no reconocido para '{col}'. "
                f"Válidos: {list(mapping.keys())}"
            )
        row[col] = mapping[val]

    # ── 5. Multi-categoría ────────────────────────────────────────────────────
    for col, mapping in MULTI_CAT_MAPS.items():
        val = raw.get(col, "")
        if isinstance(val, bool):
            row[col] = int(val)
        elif val not in mapping:
            raise ValueError(
                f"Valor '{val}' no reconocido para '{col}'. "
                f"Válidos: {list(mapping.keys())}"
            )
        else:
            row[col] = mapping[val]

    # ── 6. OHE State ──────────────────────────────────────────────────────────
    state_val = raw.get("State", "")
    for col in columnas_esperadas:
        if col.startswith("State_"):
            cat = col[len("State_"):]
            row[col] = 1 if state_val == cat else 0

    # ── 7. OHE RaceEthnicityCategory ──────────────────────────────────────────
    race_val = raw.get("RaceEthnicityCategory", "")
    for col in columnas_esperadas:
        if col.startswith("RaceEthnicityCategory_"):
            cat = col[len("RaceEthnicityCategory_"):]
            row[col] = 1 if race_val == cat else 0

    # ── 8. Construir DataFrame y reindexar con el orden exacto del modelo ─────
    df = pd.DataFrame([row])

    # reindex garantiza: columnas en orden correcto + rellena 0 en ausentes
    df = df.reindex(columns=columnas_esperadas, fill_value=0)

    return df