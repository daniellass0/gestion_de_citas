from flask import Flask, jsonify, request
import requests, os
import pybreaker
from database import conectar

app = Flask(__name__)

PAGOS_URL = os.getenv(
    "PAGOS_URL", "http://pagos:5001"
).rstrip("/")

circuito_pagos = pybreaker.CircuitBreaker(
    fail_max=int(os.getenv("CB_MAX_FALLOS", "3")),
    reset_timeout=int(os.getenv("CB_RECUPERACION", "30")),
    throw_new_error_on_trip=False
)

def normalizar_cita(cita):
    if cita is None:
        return None
    cita = dict(cita)
    if cita.get("hora") is not None:
        cita["hora"] = str(cita["hora"])
    if cita.get("fecha") is not None:
        cita["fecha"] = str(cita["fecha"])
    return cita

@app.route("/citas")
def listar_citas():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM citas")
    citas = [
        normalizar_cita(cita)
        for cita in cursor.fetchall()
    ]
    cursor.close()
    conexion.close()

    return jsonify(citas), 200

@app.route("/citas/<int:id>")
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

    if cita is None:
        return jsonify({"mensaje": "Cita no encontrada"}), 404

    return jsonify(cita), 200


@app.route("/citas", methods=["POST"])
def crear():
    nueva_cita = request.get_json(silent=True)
    if not nueva_cita:
        return jsonify({"mensaje": "Datos JSON no válidos o faltantes"}), 400
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO citas
        (usuario_id, pago_id, fecha, hora, estado)
        VALUES (%s, %s, %s, %s, %s)
    """
    valores = (
        nueva_cita.get("usuario_id"),
        nueva_cita.get("pago_id"),
        nueva_cita.get("fecha"),
        nueva_cita.get("hora"),
        nueva_cita.get("estado")
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
    cita_actualizada = request.get_json(silent=True) or {}
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

    tiempo_maximo = float(
        os.getenv("PAGOS_TIMEOUT", "2")
    )
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

    if not PAGOS_URL:
        return jsonify({
            "mensaje": "La variable PAGOS_URL no está configurada"
        }), 500

    pago_id = cita["pago_id"]
    url = f"{PAGOS_URL}/pagos/{pago_id}/detalles"

    try:
        with circuito_pagos.calling():
            respuesta_pago = requests.get(url,timeout=tiempo_maximo)
            if respuesta_pago.status_code >= 500:
                respuesta_pago.raise_for_status()

    except pybreaker.CircuitBreakerError:
        return jsonify({"mensaje": "Circuito abierto: Pagos no disponible"}), 503

    except requests.exceptions.Timeout:
        return jsonify({"mensaje": "El servicio de pagos no responde"}), 504

    except requests.exceptions.ConnectionError:
        return jsonify({"mensaje": "No se pudo conectar con el servicio de pagos"}), 503

    except requests.exceptions.HTTPError:
        return jsonify({"mensaje": "Error en el servicio de pagos" }), 502

    except requests.exceptions.RequestException:
        return jsonify({"mensaje": "Error en la comunicación con Pagos"}), 502

    if respuesta_pago.status_code == 404:
        return jsonify({ "mensaje": "No se encontró el pago o el usuario asociado"}), 404

    if respuesta_pago.status_code != 200:
        return jsonify({"mensaje": "Error en el servicio de pagos"}), 502

    try:
        datos_pago = respuesta_pago.json()

        resultado = {
            "cita": {
                "id": cita["id"],
                "fecha": cita["fecha"],
                "hora": cita["hora"],
                "estado": cita["estado"]
            },
            "pago": datos_pago["pago"],
            "usuario": datos_pago["usuario"]
        }
        return jsonify(resultado), 200
    except (ValueError, KeyError, TypeError):
        return jsonify({"mensaje": "La respuesta de Pagos tiene un formato inválido"}), 502

@app.route("/circuito/pagos", methods=["GET"])
def estado_circuito():

    return jsonify({
        "estado": circuito_pagos.current_state.upper(),
        "fallos_consecutivos": circuito_pagos.fail_counter,
        "umbral_fallas": circuito_pagos.fail_max,
        "periodo_recuperacion": circuito_pagos.reset_timeout
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5002)))