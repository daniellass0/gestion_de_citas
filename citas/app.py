from flask import Flask, jsonify, request
import requests, os
from database import conectar

app = Flask(__name__)
citas_url = os.getenv("CITAS_URL")


@app.route ("/citas")
def listar_usuarios():
    conexion = conectar()
    cursor = conexion.cursor (dictionary=True)
    cursor.execute(
        "SELECT  * FROM citas"
    )
    citas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(citas)

app.run (host="0.0.0.0.", port=5001)
