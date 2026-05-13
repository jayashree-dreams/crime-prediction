import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
df = pd.read_csv("data/crime_data.csv")

# Encode state
le = LabelEncoder()
df['state'] = le.fit_transform(df['state'])

# Features + targets
X = df[['state', 'year', 'population']]
y = df[['murder', 'rape', 'robbery', 'theft', 'assault', 'property_crime']]

# Model
model = MultiOutputRegressor(RandomForestRegressor())
model.fit(X, y)

# Save model + label encoder
joblib.dump(model, "multi_crime_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("Model Saved Successfully!")