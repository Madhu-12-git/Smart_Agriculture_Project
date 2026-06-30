import pandas as pd

farm_id = input("Enter Farm ID: ")

df = pd.read_csv("../datasets/sensor_data_balanced.csv")

farm_data = df[df["Farm_ID"] == farm_id]

if len(farm_data) > 0:
    print("\nSensor Records Found\n")
    print(farm_data.head())
else:
    print("Farm ID not found")