import mysql.connector
from core.config import settings

# MySQL bağlantısı aç
def get_connection():
    try:
        connection = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            database=settings.DB_NAME
        )
        return connection
    except mysql.connector.Error as e:
        print(f"DB bağlantı hatası: {e}")
        return None

# Bağlantıyı kapat
def close_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()