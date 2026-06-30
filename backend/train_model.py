import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
import joblib

# Load dataset
df = pd.read_csv("../datasets/historical_yield_data_balanced.csv")

# Encode categorical columns
district_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

df["District"] = district_encoder.fit_transform(df["District"])
df["Crop"] = crop_encoder.fit_transform(df["Crop"])

# Features and target
X = df.drop("Yield", axis=1)
y = df["Yield"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Performance")
print("-------------------")
print("Mean Absolute Error:", round(mae, 2))
print("R² Score:", round(r2, 4))

# Save model
joblib.dump(model, "../models/yield_model.pkl")

# Save encoders
joblib.dump(district_encoder, "../models/district_encoder.pkl")
joblib.dump(crop_encoder, "../models/crop_encoder.pkl")

print("\nModel saved successfully!")