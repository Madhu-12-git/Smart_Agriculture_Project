from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------
# Load Dataset
# -----------------------------

sensor_df = pd.read_csv("../datasets/sensor_data_balanced.csv")
history_df = pd.read_csv("../datasets/historical_yield_data_balanced.csv")
# -----------------------------
# Home API
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Smart Agriculture Advisory System API is Running"
    }

# -----------------------------
# Farm Details API
# -----------------------------

@app.get("/farm/{farm_id}")
def get_farm(farm_id: str):

    farm = sensor_df[sensor_df["Farm_ID"] == farm_id]

    if len(farm) == 0:
        return {
            "status": "Not Found"
        }

    record = farm.iloc[0]

    # -----------------------------
    # Yield Prediction
    # -----------------------------

    predicted_yield = round(
        (record["N"] * 0.5) +
        (record["P"] * 0.3) +
        (record["K"] * 0.2),
        2
    )

    # -----------------------------
    # District Average Yield
    # -----------------------------
    district = record["District"]
    district_avg = history_df[
        history_df["District"] == district
        ]["Yield"].mean()

    district_avg = round(float(district_avg) / 100, 2)

    # -----------------------------
    # Pest Risk
    # -----------------------------

    if record["Moisture"] > 75 and record["Humidity"] > 80:
        pest_risk = "HIGH"

    elif record["Moisture"] > 60 and record["Humidity"] > 70:
        pest_risk = "MEDIUM"

    else:
        pest_risk = "LOW"

    # -----------------------------
    # Data Quality
    # -----------------------------

    quality_score = 100
    quality_status = "GOOD"

    # -----------------------------
    # Recommendations
    # -----------------------------

    recommendations = []

    if pest_risk == "LOW":

        recommendations = [
            "Maintain irrigation schedule",
            "Apply balanced fertilizer",
            "Monitor crop weekly"
        ]

    elif pest_risk == "MEDIUM":

        recommendations = [
            "Inspect crop every 2-3 days",
            "Reduce excess moisture",
            "Monitor pest symptoms"
        ]

    else:

        recommendations = [
            "Immediate pest control required",
            "Reduce field moisture",
            "Consult agriculture officer"
        ]
    # -----------------------------
    # NDVI History
    # -----------------------------

    farm_history = sensor_df[
        sensor_df["Farm_ID"] == farm_id
    ]

    ndvi_values = farm_history["NDVI"].astype(float).tolist()

    ndvi_labels = []

    for i in range(len(ndvi_values)):
        ndvi_labels.append(f"Reading {i+1}")
    return {

        "Farm_ID": record["Farm_ID"],
        "District": record["District"],
        "Crop": record["Crop"],

        "N": float(record["N"]),
        "P": float(record["P"]),
        "K": float(record["K"]),

        "Moisture": float(record["Moisture"]),
        "Temperature": float(record["Temperature"]),
        "Humidity": float(record["Humidity"]),

        "pH": float(record["pH"]),
        "NDVI": float(record["NDVI"]),

        "Yield": predicted_yield,
        "DistrictAverage": district_avg,
        "PestRisk": pest_risk,

        "QualityScore": quality_score,
        "QualityStatus": quality_status,

        "Recommendations": recommendations,
        "NDVIDates": ndvi_labels,
        "NDVIHistory": ndvi_values
    }