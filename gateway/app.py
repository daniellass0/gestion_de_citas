from flask import Flask, jsonify, request, Response
import os
import requests

app = Flask(__name__)
USUARIOS_URL = os.getenv("USUARIOS_URL", "http://usuarios:5000")
PAGOS_URL = os.getenv("PAGOS_URL", "http://pagos:5001")
CITAS_URL = os.getenv("CITAS_URL", "http://citas:5002")

def reenviar(metodo, url):
    try:
        respuesta = requests.request(metodo, url, params=request.args, json=request.get_json(silent=True), timeout=5)
        return Response(respuesta.content, status=respuesta.status_code, content_type=respuesta.headers.get("Content-Type", "application/json"))
    except requests.exceptions.Timeout:
        return jsonify({
            "mensaje": "El servicio no respondió a tiempo"
        }), 504
    except requests.exceptions.ConnectionError:
        return jsonify({
            "mensaje": "No se pudo conectar con el servicio vecino"
        }), 503

@app.after_request
def permitir_home(respuesta):
    respuesta.headers["Access-Control-Allow-Origin"] = "*"
    return respuesta

@app.route("/usuarios", methods=["GET", "POST"])
def ruta_usuarios():
    return reenviar(request.method, USUARIOS_URL + "/usuarios")

@app.route("/usuarios/<path:ruta>", methods=["GET", "PUT", "DELETE"])
def ruta_usuarios_detalle(ruta):
    return reenviar(request.method, USUARIOS_URL + "/usuarios/" + ruta)

@app.route("/pagos", methods=["GET", "POST"])
def ruta_pagos():
    return reenviar(request.method, PAGOS_URL + "/pagos")

@app.route("/pagos/<path:ruta>", methods=["GET", "PUT", "DELETE"])
def ruta_pagos_detalle(ruta):
    return reenviar(request.method, PAGOS_URL + "/pagos/" + ruta)

@app.route("/citas", methods=["GET", "POST"])
def ruta_citas():
    return reenviar(request.method, CITAS_URL + "/citas")

@app.route("/citas/<path:ruta>", methods=["GET", "PUT", "DELETE"])
def ruta_citas_detalle(ruta):
    return reenviar(request.method, CITAS_URL + "/citas/" + ruta)


app.run(host="0.0.0.0", port=5000)
