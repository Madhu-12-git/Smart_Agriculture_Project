import pandas as pd
import joblib

# Load model and encoders
model = joblib.load("../models/yield_model.pkl")
district_encoder = joblib.load("../models/district_encoder.pkl")
crop_encoder = joblib.load("../models/crop_encoder.pkl")

# Read sensor dataset
sensor_df = pd.read_csv("../datasets/sensor_data_balanced.csv")

farm_id = input("Enter Farm ID: ")

farm_data = sensor_df[sensor_df["Farm_ID"] == farm_id]

if len(farm_data) == 0:
    print("Farm ID not found")
    exit()

# Take latest record
record = farm_data.sample(1).iloc[0].copy()

district = record["District"]
crop = record["Crop"]

# Encode
record["District"] = district_encoder.transform([district])[0]
record["Crop"] = crop_encoder.transform([crop])[0]

# Remove Farm_ID
features = record.drop("Farm_ID")

# Convert to dataframe
X = pd.DataFrame([features])

# Predict
prediction = model.predict(X)[0]

print("\nFarm ID:", farm_id)
print("District:", district)
print("Crop:", crop)

print("\nPredicted Yield:")
print(round(prediction, 2), "kg/hectare")