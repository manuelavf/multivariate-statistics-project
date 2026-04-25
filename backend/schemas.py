from pydantic import BaseModel, Field
from typing import Literal, Optional


class PatientFeatures(BaseModel):
    """Payload de entrada — todos los campos tal como vienen del formulario."""

    # ── Numéricas continuas ──────────────────────────────────────────────────
    PhysicalHealthDays: float = Field(..., ge=0, le=30)
    MentalHealthDays:   float = Field(..., ge=0, le=30)
    SleepHours:         float = Field(..., ge=1,  le=24)
    BMI:                float = Field(..., ge=10, le=80)
    WeightInKilograms:  float = Field(..., ge=20, le=300)
    HeightInMeters:     float = Field(..., ge=1.0, le=2.5)

    # ── Sex ──────────────────────────────────────────────────────────────────
    Sex: Literal["Male", "Female"]

    # ── Binarias Yes/No ──────────────────────────────────────────────────────
    PhysicalActivities:      Literal["Yes", "No"]
    HadStroke:               Literal["Yes", "No"]
    HadAsthma:               Literal["Yes", "No"]
    HadSkinCancer:           Literal["Yes", "No"]
    HadCOPD:                 Literal["Yes", "No"]
    HadDepressiveDisorder:   Literal["Yes", "No"]
    HadKidneyDisease:        Literal["Yes", "No"]
    HadArthritis:            Literal["Yes", "No"]
    DeafOrHardOfHearing:     Literal["Yes", "No"]
    BlindOrVisionDifficulty: Literal["Yes", "No"]
    DifficultyConcentrating: Literal["Yes", "No"]
    DifficultyWalking:       Literal["Yes", "No"]
    DifficultyDressingBathing: Literal["Yes", "No"]
    DifficultyErrands:       Literal["Yes", "No"]
    ChestScan:               Literal["Yes", "No"]
    AlcoholDrinkers:         Literal["Yes", "No"]
    HIVTesting:              Literal["Yes", "No"]
    FluVaxLast12:            Literal["Yes", "No"]
    PneumoVaxEver:           Literal["Yes", "No"]
    HighRiskLastYear:        Literal["Yes", "No"]

    # ── Ordinales ────────────────────────────────────────────────────────────
    GeneralHealth: Literal["Poor", "Fair", "Good", "Very good", "Excellent"]

    AgeCategory: Literal[
        "Age 18 to 24", "Age 25 to 29", "Age 30 to 34", "Age 35 to 39",
        "Age 40 to 44", "Age 45 to 49", "Age 50 to 54", "Age 55 to 59",
        "Age 60 to 64", "Age 65 to 69", "Age 70 to 74", "Age 75 to 79",
        "Age 80 or older",
    ]

    LastCheckupTime: Literal[
        "5 or more years ago",
        "Within past 5 years (2 years but less than 5 years ago)",
        "Within past 2 years (1 year but less than 2 years ago)",
        "Within past year (anytime less than 12 months ago)",
    ]

    RemovedTeeth: Literal["None of them", "1 to 5", "6 or more, but not all", "All"]

    # ── Multi-categoría ──────────────────────────────────────────────────────
    HadDiabetes: Literal[
        "No",
        "No, pre-diabetes or borderline diabetes",
        "Yes, but only during pregnancy (female)",
        "Yes",
    ]

    SmokerStatus: Literal[
        "Never smoked",
        "Former smoker",
        "Current smoker - now smokes some days",
        "Current smoker - now smokes every day",
    ]

    ECigaretteUsage: Literal[
        "Never used e-cigarettes in my entire life",
        "Not at all (right now)",
        "Use them some days",
        "Use them every day",
    ]

    TetanusLast10Tdap: Literal[
        "No, did not receive any tetanus shot in the past 10 years",
        "Yes, received tetanus shot but not sure what type",
        "Yes, received tetanus shot, but not Tdap",
        "Yes, received Tdap",
    ]

    CovidPos: Literal[
        "No",
        "Yes",
        "Tested positive using home test without a health professional",
    ]

    # ── Nominales ────────────────────────────────────────────────────────────
    RaceEthnicityCategory: Literal[
        "White only, Non-Hispanic",
        "Black only, Non-Hispanic",
        "Hispanic",
        "Multiracial, Non-Hispanic",
        "Other race only, Non-Hispanic",
    ]

    State: str  # 54 valores — validados en preprocessing.py


class PredictionResponse(BaseModel):
    """Respuesta del endpoint /predict."""
    prediction:  int    # 0 = bajo riesgo · 1 = alto riesgo
    probability: float  # probabilidad de clase positiva
    risk_level:  Literal["low", "high"]
    message:     str