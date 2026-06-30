import sqlite3
import pandas as pd

conn = sqlite3.connect("agriculture.db")

query = "SELECT * FROM farm_master LIMIT 10"

df = pd.read_sql(query, conn)

print(df)

conn.close()