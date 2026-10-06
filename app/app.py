from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template

BASE_DIR = Path(__file__).resolve().parent.parent

pipeline = joblib.load(BASE_DIR / "model" / "diabetes_pipeline.joblib")
with open(BASE_DIR / "model" / "model_info.json") as f:
    model_info = json.load(f)

FEATURES = model_info["feature_names"]
THRESHOLD = model_info["threshold"]

LIMITS = {
    "Pregnancies": (0, 20),
    "Glucose": (40, 400),
    "BloodPressure": (30, 200),
    "SkinThickness": (5, 100),
    "Insulin": (10, 900),
    "BMI": (10, 70),
    "DiabetesPedigreeFunction": (0.05, 2.5),
    "Age": (1, 120),
}
OPTIONAL = {"BloodPressure", "SkinThickness", "Insulin"}

app = Flask(__name__)


def parse_input(data):
    row, errors = {}, []
    for feat in FEATURES:
        raw = data.get(feat)

        if raw is None or str(raw).strip() == "":
            if feat in OPTIONAL:
                row[feat] = np.nan
            else:
                errors.append(f"{feat} is required")
            continue

        try:
            value = float(raw)
        except (TypeError, ValueError):
            errors.append(f"{feat} must be a number")
            continue

        low, high = LIMITS[feat]
        if not (low <= value <= high):
            errors.append(f"{feat} must be between {low} and {high}")
            continue

        row[feat] = value
    return row, errors


def risk_level(p):
    if p < 0.30:
        return "Low"
    if p < 0.60:
        return "Moderate"
    return "High"


@app.route("/")
def home():
    return render_template("index.html", metrics=model_info)


@app.route("/api/info")
def api_info():
    return jsonify(message="Diabetes Risk API is running", model=model_info)

@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(errors=["Send a JSON object in the request body"]), 400

    row, errors = parse_input(data)
    if errors:
        return jsonify(errors=errors), 400

    X_new = pd.DataFrame([row], columns=FEATURES)
    proba = float(pipeline.predict_proba(X_new)[0, 1])

    return jsonify(
        probability=round(proba, 3),
        prediction=int(proba >= THRESHOLD),
        risk_level=risk_level(proba),
        disclaimer="Educational project, not medical advice.",
    )


if __name__ == "__main__":
    app.run(debug=True)