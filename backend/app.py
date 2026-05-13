from collections import defaultdict
from csv import DictReader
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib


app = Flask(__name__)
CORS(app)

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
MODEL_PATH = PROJECT_ROOT / "multi_crime_model.pkl"
LABEL_ENCODER_PATH = PROJECT_ROOT / "label_encoder.pkl"
DATA_PATH = PROJECT_ROOT / "data" / "crime_data.csv"

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

target_cols = ["murder", "rape", "robbery", "theft", "assault", "property_crime"]
max_year = 0
yearly_totals = defaultdict(lambda: defaultdict(float))
yearly_counts = defaultdict(int)

with DATA_PATH.open(newline="", encoding="utf-8") as csv_file:
    reader = DictReader(csv_file)
    for row in reader:
        year = int(row["year"])
        max_year = max(max_year, year)
        yearly_counts[year] += 1
        for col in target_cols:
            yearly_totals[year][col] += float(row[col])

yearly_means = {}
for year, totals in yearly_totals.items():
    count = yearly_counts[year]
    yearly_means[year] = {col: totals[col] / count for col in target_cols}

sorted_years = sorted(yearly_means)
trend_rates = {col: None for col in target_cols}

for col in target_cols:
    growth_values = []
    previous_value = None
    for year in sorted_years:
        current_value = yearly_means[year][col]
        if previous_value not in (None, 0):
            growth_values.append((current_value - previous_value) / previous_value)
        previous_value = current_value

    if growth_values:
        trend_rates[col] = sum(growth_values) / len(growth_values)


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

    preds = model.predict([[state_encoded, year, population]])[0]

    if year > max_year:
        year_gap = year - max_year
        for col in target_cols:
            if trend_rates[col] is not None:
                preds[target_cols.index(col)] *= (1 + trend_rates[col]) ** year_gap

    prediction_dict = {
        crime: max(0, int(round(preds[index])))
        for index, crime in enumerate(target_cols)
    }

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