from flask import Flask, jsonify, request
import requests
import os
from database import conectar

app = Flask(__name__)

USUARIOS_URL = os.getenv(
    "USUARIOS_URL", "http://usuarios:5000"
).rstrip("/")

PAGOS_URL = os.getenv(
    "PAGOS_URL", "http://pagos:5001"
).rstrip("/")

def normalizar_cita(cita):
    if cita is None:
        return None

    cita = dict(cita)

    if cita.get("hora") is not None:
        cita["hora"] = str(cita["hora"])

    return cita

@app.route("/citas", methods=["GET"])
def listar_citas():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM citas"
        )
    citas = [
    
    normalizar_cita(cita)
    for cita in cursor.fetchall()
    
    ]
    cursor.close()
    conexion.close()

    return jsonify(citas), 200


@app.route("/citas/<int:id>", methods=["GET"])
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    sql = """
        SELECT * FROM citas
        WHERE id = %s
    """

    cursor.execute(sql, (id,))
    cita = normalizar_cita(cursor.fetchone())

    cursor.close()
    conexion.close()

    return jsonify(cita), 200


@app.route("/citas", methods=["POST"])
def crear():
    nueva_cita = request.get_json(silent=True)
    campos = ("usuario_id", "pago_id", "fecha", "hora", "estado")

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
        INSERT INTO citas
        (usuario_id, pago_id, fecha, hora, estado)
        VALUES (%s, %s, %s, %s, %s)
    """

    valores = (
        nueva_cita["usuario_id"],
        nueva_cita["pago_id"],
        nueva_cita["fecha"],
        nueva_cita["hora"],
        nueva_cita["estado"]
    )

    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Cita creada con éxito",
        "id": nuevo_id
    }), 201


@app.route("/citas/<int:id>", methods=["PUT"])
def actualizar(id):
    cita_actualizada = request.get_json(silent=True)
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM citas WHERE id = %s",
        (id,)
    )
    cita = normalizar_cita(cursor.fetchone())

    if cita is None:
        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": "Cita no encontrada"
        }), 404

    sql = """
        UPDATE citas
        SET usuario_id = %s,
            pago_id = %s,
            fecha = %s,
            hora = %s,
            estado = %s
        WHERE id = %s
    """

    valores = (
        cita_actualizada.get("usuario_id", cita["usuario_id"]),
        cita_actualizada.get("pago_id", cita["pago_id"]),
        cita_actualizada.get("fecha", cita["fecha"]),
        cita_actualizada.get("hora", cita["hora"]),
        cita_actualizada.get("estado", cita["estado"]),
        id
    )

    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({
        "mensaje": "Cita actualizada con éxito"
    }), 200


@app.route("/citas/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()


    cursor.execute(
        "DELETE FROM citas WHERE id = %s",
        (id,)
    )

    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Cita eliminada con éxito",
        "id": id
    }), 200


@app.route("/citas/<int:id>/detalles", methods=["GET"])
def detalles(id):


    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM citas WHERE id = %s",
        (id,)
    )

    cita = normalizar_cita(cursor.fetchone())
    cursor.close()
    conexion.close()

    if cita is None:
        return jsonify({
            "mensaje": "Cita no encontrada"
        }), 404

    try:

        respuesta_usuario = requests.get(
            f"{USUARIOS_URL}/usuarios/{cita['usuario_id']}",

        )

        respuesta_usuario.raise_for_status()
        usuario = respuesta_usuario.json()
        respuesta_pago = requests.get(
            f"{PAGOS_URL}/pagos/{cita['pago_id']}",

        )

        respuesta_pago.raise_for_status()
        pago = respuesta_pago.json()

        resultado = {
            "cita": {
                "id": cita["id"],
                "fecha": cita["fecha"],
                "hora": cita["hora"],
                "estado": cita["estado"]
            },
            "pago": {
                "id_pago": pago["id"],
                "estado_pago": pago["estado"]
            },
            "usuario": {
                "id_usuario": usuario["id"],
                "nombre_usuario": usuario["nombre"]
            }
        }
        return jsonify(resultado), 200

    except (requests.RequestException, ValueError, KeyError):
        return jsonify({
            "error": "No fue posible obtener la información de Usuarios o Pagos"
        }), 502


app.run( host="0.0.0.0", port=int(os.getenv("PORT", 5002)))