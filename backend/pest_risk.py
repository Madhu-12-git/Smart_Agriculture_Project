import pandas as pd

farm_id = input("Enter Farm ID: ")

df = pd.read_csv("../datasets/sensor_data_balanced.csv")

farm_data = df[df["Farm_ID"] == farm_id]

if len(farm_data) == 0:
    print("Farm ID not found")
    exit()

record = farm_data.sample(1).iloc[0]

moisture = record["Moisture"]
humidity = record["Humidity"]
ndvi = record["NDVI"]

# Pest Risk Rules
if moisture > 75 and humidity > 80:
    risk = "HIGH"

elif moisture > 60 and humidity > 70:
    risk = "MEDIUM"

else:
    risk = "LOW"

print("\nFarm ID:", farm_id)
print("District:", record["District"])
print("Crop:", record["Crop"])

print("\nMoisture:", moisture)
print("Humidity:", humidity)
print("NDVI:", ndvi)

print("\nPest Risk:", risk)