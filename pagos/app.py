from flask import Flask, jsonify, request
from database import conectar
import requests
import os
import pybreaker

app = Flask(__name__)

USUARIOS_URL = os.getenv(
    "USUARIOS_URL", "http://usuarios:5000"
).rstrip("/")

circuito_usuarios = pybreaker.CircuitBreaker(
    fail_max=int(os.getenv("CB_MAX_FALLOS", "3")),
    reset_timeout=int(os.getenv("CB_RECUPERACION", "30")),
    throw_new_error_on_trip=False
)

@app.route("/pagos", methods=["GET"])
def listar_pagos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pagos")
    pagos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return jsonify(pagos), 200

@app.route("/pagos/<int:id>", methods=["GET"])
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    sql = """
        SELECT * FROM pagos
        WHERE id = %s
    """
    cursor.execute(sql, (id,))
    pago = cursor.fetchone()

    cursor.close()
    conexion.close()

    if pago is None:
        return jsonify({"mensaje": "Pago no encontrado"}), 404

    return jsonify(pago), 200

@app.route("/pagos", methods=["POST"])
def crear():

    nuevo_pago = request.get_json(silent=True)

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
        INSERT INTO pagos
        (usuario_id, monto, estado, creado)
        VALUES (%s, %s, %s, %s)
    """

    valores = (
        nuevo_pago["usuario_id"],
        nuevo_pago["monto"],
        nuevo_pago["estado"],
        nuevo_pago["creado"]
    )

    cursor.execute(sql, valores)
    conexion.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Pago creado con éxito",
        "id": nuevo_id
    }), 201

@app.route("/pagos/<int:id>", methods=["PUT"])
def actualizar(id):
    pago_actualizado = request.get_json(silent=True)


    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM pagos WHERE id = %s",
        (id,)
    )

    if cursor.fetchone() is None:
        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": "Pago no encontrado"
        }), 404

    sql = """
        UPDATE pagos
        SET monto = %s, estado = %s, creado = %s
        WHERE id = %s
    """

    valores = (
        pago_actualizado["monto"],
        pago_actualizado["estado"],
        pago_actualizado["creado"],
        id
    )

    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Pago actualizado con éxito"
    }), 200



@app.route("/pagos/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
        DELETE FROM pagos
        WHERE id = %s
    """

    cursor.execute(sql, (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Pago eliminado con éxito"
    }), 200

@app.route("/pagos/<int:id>/detalles", methods=["GET"])
def detalles(id):

    tiempo_maximo = float(os.getenv("USUARIOS_TIMEOUT", "2"))
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute( "SELECT * FROM pagos WHERE id = %s",(id,))
    pago = cursor.fetchone()
    cursor.close()
    conexion.close()

    if pago is None:
        return jsonify({"mensaje": "Pago no encontrado"}), 404
    if not USUARIOS_URL:
        return jsonify({"mensaje": "La variable USUARIOS_URL no está configurada"}), 500
    usuario_id = pago["usuario_id"]
    url = f"{USUARIOS_URL}/usuarios/{usuario_id}"

    try:
        with circuito_usuarios.calling():
            respuesta = requests.get(url,timeout=tiempo_maximo)
            if respuesta.status_code >= 500:
                respuesta.raise_for_status()

    except pybreaker.CircuitBreakerError:
        return jsonify({"mensaje": "Circuito abierto: Usuarios no disponible"}), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "mensaje": "El servicio de usuarios no responde"
        }), 504

    except requests.exceptions.ConnectionError:
        return jsonify({
            "mensaje": "No se pudo conectar con el servicio de usuarios"
        }), 503

    except requests.exceptions.HTTPError:
        return jsonify({
            "mensaje": "Error en el servicio de usuarios"
        }), 502

    except requests.exceptions.RequestException:
        return jsonify({
            "mensaje": "Error en la comunicación con Usuarios"
        }), 502

    # Validar la respuesta del servicio Usuarios
    if respuesta.status_code == 404:
        return jsonify({
            "mensaje": "Usuario no encontrado"
        }), 404

    if respuesta.status_code != 200:
        return jsonify({
            "mensaje": "Error en el servicio de usuarios"
        }), 502

    try:
        usuario = respuesta.json()

        resultado = {
            "pago": {
                "id": pago["id"],
                "usuario_id": pago["usuario_id"],
                "monto": str(pago["monto"]),
                "estado": pago["estado"],
                "creado": str(pago["creado"])
            },
            "usuario": {
                "id_usuario": usuario["id"],
                "nombre_usuario": usuario["nombre"]
            }
        }

        return jsonify(resultado), 200

    except (ValueError, KeyError, TypeError):
        return jsonify({
            "mensaje": "La respuesta de Usuarios tiene un formato inválido"
        }), 502

@app.route("/circuito/usuarios", methods=["GET"])
def estado_circuito():

    return jsonify({
        "estado": circuito_usuarios.current_state.upper(),
        "fallos_consecutivos": circuito_usuarios.fail_counter,
        "umbral_fallas": circuito_usuarios.fail_max,
        "periodo_recuperacion": circuito_usuarios.reset_timeout
    }), 200

    
app.run(host="0.0.0.0", port=5001)
