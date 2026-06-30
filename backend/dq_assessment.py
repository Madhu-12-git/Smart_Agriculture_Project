import pandas as pd

df = pd.read_csv("../datasets/sensor_data_balanced.csv")

print("\n==========================")
print("DATA QUALITY ASSESSMENT")
print("==========================")

# Missing values
missing_values = df.isnull().sum().sum()

# Duplicate rows
duplicates = df.duplicated().sum()

# Range checks
invalid_records = 0

invalid_records += len(df[(df["Moisture"] < 0) | (df["Moisture"] > 100)])
invalid_records += len(df[(df["Humidity"] < 0) | (df["Humidity"] > 100)])
invalid_records += len(df[(df["pH"] < 0) | (df["pH"] > 14)])
invalid_records += len(df[(df["NDVI"] < 0) | (df["NDVI"] > 1)])

total_records = len(df)

quality_score = (
    1 - (missing_values + duplicates + invalid_records)
    / max(total_records, 1)
) * 100

quality_score = max(0, round(quality_score, 2))

print("\nMissing Values :", missing_values)
print("Duplicate Records :", duplicates)
print("Invalid Records :", invalid_records)

print("\nQuality Score :", quality_score, "%")

if quality_score >= 90:
    status = "GOOD"
elif quality_score >= 70:
    status = "MODERATE"
else:
    status = "POOR"

print("Status :", status)