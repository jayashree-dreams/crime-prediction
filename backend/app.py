from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import pandas as pd


app = Flask(__name__)
CORS(app)

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
MODEL_PATH = PROJECT_ROOT / "multi_crime_model.pkl"
LABEL_ENCODER_PATH = PROJECT_ROOT / "label_encoder.pkl"
DATA_PATH = PROJECT_ROOT / "data" / "crime_data.csv"

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

df = pd.read_csv(DATA_PATH)
max_year = int(df["year"].max())
target_cols = ["murder", "rape", "robbery", "theft", "assault", "property_crime"]
trend_rates = {}

for col in target_cols:
    yearly_data = df[["year", col]].groupby("year").mean()
    yearly_data["shift"] = yearly_data[col].shift(1)
    yearly_data["growth"] = (yearly_data[col] - yearly_data["shift"]) / yearly_data["shift"]
    trend_rates[col] = yearly_data["growth"].mean()


@app.get("/")
def home():
    return jsonify({"message": "Crime prediction API is running."})


@app.get("/states")
def states():
    return jsonify(sorted(label_encoder.classes_.tolist()))


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True) or request.form

    try:
        state = payload["state"]
        year = int(payload["year"])
        population = int(payload["population"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "state, year, and population are required."}), 400

    try:
        state_encoded = label_encoder.transform([state])[0]
    except ValueError:
        return jsonify({"error": f"Unknown state: {state}"}), 400

    input_df = pd.DataFrame([[state_encoded, year, population]], columns=["state", "year", "population"])
    preds = model.predict(input_df)[0]
    preds = pd.Series(preds, index=target_cols)

    if year > max_year:
        year_gap = year - max_year
        for col in target_cols:
            if pd.notna(trend_rates[col]):
                preds[col] *= (1 + trend_rates[col]) ** year_gap

    prediction_dict = {crime: max(0, int(round(preds[crime]))) for crime in target_cols}

    return jsonify(
        {
            "state": state,
            "year": year,
            "population": population,
            "predictions": prediction_dict,
            "total_crimes": int(sum(prediction_dict.values())),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)