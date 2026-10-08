from flask import Flask, jsonify, request
import requests, os
from database import conectar

app = Flask(__name__)
citas_url = os.getenv("CITAS_URL")


@app.route ("/usuarios")
def listar_usuarios():
    conexion = conectar()
    cursor = conexion.cursor (dictionary=True)
    cursor.execute(
        "SELECT  * FROM usuarios"
    )
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(usuarios)

app.run (host="0.0.0.0.", port=5000)
