import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("olist.db")
print("Database files created and connected successfully!")

df = pd.read_csv("data/olist_orders_dataset.csv")
print(f"Total orders loaded in memory: {len(df)}")

df.to_sql("orders", conn, if_exists="replace", index=False)
print("Table 'orders' successfully saved in olist.db!")

for file_name in os.listdir("data"):
    if file_name.endswith(".csv"):
        table_name = file_name.replace(".csv", "").replace("olist_", "").replace("_dataset", "")
        file_path = os.path.join("data", file_name)
        df = pd.read_csv(file_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {len(df):,} rows into '{table_name}'")
conn.close()
print("All tables successfully written to olist.db!")

