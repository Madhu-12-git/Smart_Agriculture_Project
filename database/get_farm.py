import sqlite3

farm_id = input("Enter Farm ID: ")

conn = sqlite3.connect("agriculture.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT District, Crop FROM farm_master WHERE Farm_ID=?",
    (farm_id,)
)

result = cursor.fetchone()

if result:
    print("\nFarm Found")
    print("District:", result[0])
    print("Crop:", result[1])
else:
    print("\nFarm ID not found")

conn.close()