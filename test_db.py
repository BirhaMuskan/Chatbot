from app.database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT TOP 5 name FROM sys.tables")

for row in cursor.fetchall():
    print(row)

conn.close()