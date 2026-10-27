
from db import get_db_connection

try:
    connection = get_db_connection()
    print("Successfully connected to LinkVault database!")

    connection.close()
except Exception as error:
    print("Connection failed:", error)
