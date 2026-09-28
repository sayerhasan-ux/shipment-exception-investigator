import sqlite3

conn = sqlite3.connect("file:olist.db?mode=ro", uri=True)
cursor = conn.cursor()

cursor.execute("SELECT COUNT (*) FROM orders;")
print(f"Read Success: Total orders = {cursor.fetchone()[0]}")
try:
    cursor.execute("DROP TABLE orders;")
except Exception as e:
    print(f"Security Check Passed: {e}")



