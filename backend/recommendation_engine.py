import pandas as pd
import joblib

# Load model and encoders
model = joblib.load("../models/yield_model.pkl")
district_encoder = joblib.load("../models/district_encoder.pkl")
crop_encoder = joblib.load("../models/crop_encoder.pkl")

# Read sensor data
sensor_df = pd.read_csv("../datasets/sensor_data_balanced.csv")

farm_id = input("Enter Farm ID: ")

farm_data = sensor_df[sensor_df["Farm_ID"] == farm_id]

if len(farm_data) == 0:
    print("Farm ID not found")
    exit()

record = farm_data.iloc[0].copy()

district = record["District"]
crop = record["Crop"]

# ----------------------------
# Yield Prediction
# ----------------------------

record["District"] = district_encoder.transform([district])[0]
record["Crop"] = crop_encoder.transform([crop])[0]

features = record.drop("Farm_ID")

X = pd.DataFrame([features])

predicted_yield = model.predict(X)[0]

# ----------------------------
# Pest Risk
# ----------------------------

moisture = record["Moisture"]
humidity = record["Humidity"]

if moisture > 75 and humidity > 80:
    risk = "HIGH"

elif moisture > 60 and humidity > 70:
    risk = "MEDIUM"

else:
    risk = "LOW"

# ----------------------------
# Recommendations
# ----------------------------

recommendations = []

if risk == "LOW":
    recommendations.append("Continue current irrigation schedule")
    recommendations.append("Maintain balanced fertilization")
    recommendations.append("Monitor crop weekly")

elif risk == "MEDIUM":
    recommendations.append("Inspect crops for pest symptoms")
    recommendations.append("Optimize irrigation practices")
    recommendations.append("Monitor field every 2-3 days")

else:
    recommendations.append("Immediate field inspection required")
    recommendations.append("Apply pest control measures")
    recommendations.append("Reduce excess moisture in field")

# ----------------------------
# Output
# ----------------------------

print("\n==============================")
print("SMART AGRICULTURE ADVISORY")
print("==============================")

print("\nFarm ID:", farm_id)
print("District:", district)
print("Crop:", crop)

print("\nPredicted Yield:")
print(round(predicted_yield, 2), "kg/hectare")

print("\nPest Risk:")
print(risk)

print("\nRecommendations:")

for rec in recommendations:
    print("✓", rec)