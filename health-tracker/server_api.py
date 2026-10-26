"""
FastAPI Backend Server for Height-Weight Health Tracker
Serves predictions directly from your trained `.pkl` models or fallback weights.
Deployable to Render, Railway, AWS, Fly.io, or Heroku.

Usage:
  pip install fastapi uvicorn pydantic
  uvicorn server_api:app --reload --port 8000
"""

import os
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Height-Weight Health Tracker API",
    description="Machine Learning & Anthropometric Health Diagnostics API",
    version="1.0.0"
)

# Enable CORS for seamless deployment on ANY frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models
linear_model = None
logistic_model = None

# Default mathematical fallback coefficients (trained on 10,000 samples)
FALLBACK_LINEAR = {"slope": 1.4211, "intercept": -166.2791}
FALLBACK_LOGISTIC = {"coef_h": 0.1991, "coef_w": -0.3856, "intercept": -5.3558}

@app.on_event("startup")
def load_saved_models():
    global linear_model, logistic_model
    linear_pkl = "weight_height_linear.pkl"
    logistic_pkl = "gender_classification.pkl"

    if os.path.exists(linear_pkl):
        try:
            with open(linear_pkl, "rb") as f:
                linear_model = pickle.load(f)
            print(f" Loaded {linear_pkl}")
        except Exception as e:
            print(f" Could not load {linear_pkl}: {e}")

    if os.path.exists(logistic_pkl):
        try:
            with open(logistic_pkl, "rb") as f:
                logistic_model = pickle.load(f)
            print(f" Loaded {logistic_pkl}")
        except Exception as e:
            print(f" Could not load {logistic_pkl}: {e}")


class BiometricRequest(BaseModel):
    height_cm: float = Field(..., ge=80, le=250, description="Height in centimeters")
    weight_kg: float = Field(..., ge=20, le=350, description="Weight in kilograms")
    age: int = Field(25, ge=10, le=120, description="Age in years")
    biological_sex: str = Field("male", description="'male' or 'female'")
    activity_multiplier: float = Field(1.375, ge=1.0, le=2.5, description="Physical activity factor")


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Height-Weight Health Tracker API",
        "docs_url": "/docs"
    }


@app.post("/api/diagnostics")
def run_diagnostics(data: BiometricRequest):
    h_cm = data.height_cm
    w_kg = data.weight_kg
    h_m = h_cm / 100.0

    # 1. BMI Calculation & Category
    bmi = round(w_kg / (h_m * h_m), 1)
    if bmi < 18.5:
        category = "Underweight"
        risk = "Potential nutrient deficiency / lower bone mineral density"
    elif bmi < 25.0:
        category = "Normal Weight"
        risk = "Lowest statistical risk for cardiovascular & metabolic diseases"
    elif bmi < 30.0:
        category = "Overweight"
        risk = "Elevated risk; moderate lifestyle adjustments recommended"
    elif bmi < 35.0:
        category = "Obesity Class I"
        risk = "High risk for hypertension, insulin resistance, and joint stress"
    else:
        category = "Obesity Class II/III"
        risk = "Significantly elevated risk; medical supervision advised"

    # 2. Healthy Weight Range (WHO BMI 18.5 to 24.9)
    min_ideal_kg = round(18.5 * (h_m ** 2), 1)
    max_ideal_kg = round(24.9 * (h_m ** 2), 1)

    # 3. BMR (Mifflin-St Jeor Equation)
    bmr = (10 * w_kg) + (6.25 * h_cm) - (5 * data.age)
    if data.biological_sex.lower() == "female":
        bmr -= 161
    else:
        bmr += 5
    bmr = int(round(bmr))

    # 4. TDEE & Calorie Targets
    tdee = int(round(bmr * data.activity_multiplier))
    caloric_targets = {
        "aggressive_fat_loss": tdee - 500,
        "mild_fat_loss": tdee - 250,
        "maintenance": tdee,
        "muscle_gain": tdee + 300
    }

    # 5. Body Fat % (Deurenberg Formula)
    sex_factor = 1 if data.biological_sex.lower() == "male" else 0
    body_fat = round((1.20 * bmi) + (0.23 * data.age) - (10.8 * sex_factor) - 5.4, 1)

    # 6. Hydration
    water_liters = round(w_kg * 0.035, 1)

    # 7. ML Predictions: Logistic Regression for Anthropometric Frame
    if logistic_model is not None:
        prob = logistic_model.predict_proba([[h_cm, w_kg]])[0]
        prob_male = round(float(prob[0]) * 100, 1)
        prob_female = round(float(prob[1]) * 100, 1)
    else:
        # Exact mathematical inference
        z = (FALLBACK_LOGISTIC["coef_h"] * h_cm) + (FALLBACK_LOGISTIC["coef_w"] * w_kg) + FALLBACK_LOGISTIC["intercept"]
        p_female = 1.0 / (1.0 + np.exp(-z))
        prob_female = round(float(p_female) * 100, 1)
        prob_male = round(100.0 - prob_female, 1)

    # 8. ML Predictions: Linear Regression for Population Mean Weight
    if linear_model is not None:
        expected_kg = round(float(linear_model.predict([[h_cm]])[0]), 1)
    else:
        expected_kg = round(FALLBACK_LINEAR["slope"] * h_cm + FALLBACK_LINEAR["intercept"], 1)

    return {
        "inputs": {
            "height_cm": h_cm,
            "weight_kg": w_kg,
            "age": data.age,
            "sex": data.biological_sex
        },
        "bmi": {
            "value": bmi,
            "category": category,
            "risk_assessment": risk
        },
        "healthy_weight_range_kg": {
            "min": min_ideal_kg,
            "max": max_ideal_kg
        },
        "metabolism": {
            "bmr_kcal": bmr,
            "tdee_kcal": tdee,
            "targets": caloric_targets
        },
        "body_composition": {
            "estimated_body_fat_pct": max(3.0, body_fat),
            "hydration_liters": water_liters
        },
        "machine_learning": {
            "anthropometric_frame_prob": {
                "male_pct": prob_male,
                "female_pct": prob_female
            },
            "population_baseline_weight_kg": expected_kg,
            "variance_from_baseline_kg": round(w_kg - expected_kg, 1)
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server_api:app", host="0.0.0.0", port=8000, reload=True)
