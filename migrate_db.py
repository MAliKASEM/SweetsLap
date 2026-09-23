"""Add Arabic columns to existing database."""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add columns if they don't exist
try:
    cursor.execute("ALTER TABLE menu_items ADD COLUMN name_ar TEXT DEFAULT ''")
    print("Added name_ar column")
except Exception as e:
    print(f"name_ar: {e}")

try:
    cursor.execute("ALTER TABLE menu_items ADD COLUMN ingredients_ar TEXT DEFAULT ''")
    print("Added ingredients_ar column")
except Exception as e:
    print(f"ingredients_ar: {e}")

conn.commit()
conn.close()
print("Migration complete.")
