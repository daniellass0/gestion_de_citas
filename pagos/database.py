import mysql.connector 
import os 
import time

def conectar():
    for intento in range(10):
        try:
            conexion = mysql.connector.connect(
                host = os.getenv("DB_PAGOS_HOST"),
                port = int(os.getenv("DB_PAGOS_PORT", 3306)),
                user = os.getenv("DB_PAGOS_USER"),
                password = os.getenv("DB_PAGOS_PASSWORD"),
                database = os.getenv("DB_PAGOS_NAME")
            )
            return conexion
        except mysql.connector.Error:
            print("la base de datos aun esta cargando")
        intento + 1
        time.sleep(3)
