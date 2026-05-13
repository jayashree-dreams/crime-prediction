from flask import Flask, render_template, request
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Get PORT from environment variable (Render requirement)
port = int(os.environ.get('PORT', 5000))

# Load model & encoder
model = joblib.load('multi_crime_model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Load original data for year trend adjustment
df = pd.read_csv("data/crime_data.csv")
max_year = df['year'].max()

# Calculate yearly trend (average % increase per year)
target_cols = ['murder', 'rape', 'robbery', 'theft', 'assault', 'property_crime']
trend_rates = {}

for col in target_cols:
    yearly_data = df[['year', col]].groupby('year').mean()
    yearly_data['shift'] = yearly_data[col].shift(1)
    yearly_data['growth'] = (yearly_data[col] - yearly_data['shift']) / yearly_data['shift']
    trend_rates[col] = yearly_data['growth'].mean()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        state = request.form['state']
        year = int(request.form['year'])
        population = int(request.form['population'])

        # Encode state
        state_encoded = label_encoder.transform([state])[0]

        input_df = pd.DataFrame([[state_encoded, year, population]], 
                                columns=['state', 'year', 'population'])

        preds = model.predict(input_df)[0]
        preds = pd.Series(preds, index=target_cols)

        # Apply future year trend adjustment
        if year > max_year:
            year_gap = year - max_year
            for col in target_cols:
                if trend_rates[col] is not None:
                    preds[col] *= (1 + trend_rates[col]) ** year_gap

        prediction_dict = {crime: int(preds[crime]) for crime in target_cols}

        # Make graph
        plt.figure(figsize=(8, 4))
        plt.bar(prediction_dict.keys(), prediction_dict.values())
        plt.xticks(rotation=20)
        plt.title(f"Crime Prediction — {state} ({year})")
        plt.tight_layout()

        graph_path = "static/prediction_graph.png"
        plt.savefig(graph_path)
        plt.close()

        return render_template("index.html",
                               prediction_dict=prediction_dict,
                               graph_image=True)
    
    except Exception as e:
        print("❌ Error:", e)
        return render_template("index.html",
                               prediction_dict=None,
                               graph_image=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)