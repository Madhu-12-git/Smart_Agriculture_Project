import sqlite3
import pandas as pd

# Create database
conn = sqlite3.connect("agriculture.db")

cursor = conn.cursor()

# Farm Master Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS farm_master (
    Farm_ID TEXT PRIMARY KEY,
    District TEXT,
    Crop TEXT
)
""")

# Sensor Readings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_readings (
    Reading_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Farm_ID TEXT,
    N INTEGER,
    P INTEGER,
    K INTEGER,
    Moisture REAL,
    pH REAL,
    Temperature REAL,
    Humidity REAL,
    NDVI REAL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Load farm master dataset
farm_df = pd.read_csv("../datasets/farm_master_balanced.csv")

# Insert farm data
farm_df.to_sql(
    "farm_master",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()
conn.close()

print("Database created successfully!")
print("Farm master data loaded!")