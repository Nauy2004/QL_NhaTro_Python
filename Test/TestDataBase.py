import sqlite3
import os

db_path = os.path.abspath("../Data/BTL_QLPT.db")
print("Đường dẫn database:", db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Các bảng trong database:", tables)

conn.close()
