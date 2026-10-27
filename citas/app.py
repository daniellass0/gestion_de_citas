from flask import Flask, jsonify, request
import requests, os
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

    if cita.get("fecha") is not None:
        cita["fecha"] = str(cita["fecha"])

    return cita


def consultar(url):
    """Hace un GET a otro servicio. Devuelve el JSON o None si falla."""
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            return respuesta.json()
        return None
    except requests.RequestException:
        return None


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

    pago_id = cita["pago_id"]

    url = f"{PAGOS_URL}/pagos/{pago_id}/detalles"

    try:
        respuesta_pago = requests.get(url)

        if respuesta_pago.status_code != 200:
            return jsonify({
                "mensaje": "No fue posible obtener los detalles del pago"
            }), respuesta_pago.status_code

        datos_pago = respuesta_pago.json()

        return jsonify({
            "cita": {
                "id": cita["id"],
                "fecha": str(cita["fecha"]),
                "hora": cita["hora"],
                "estado": cita["estado"]
            },
            "pago": datos_pago["pago"],
            "usuario": datos_pago["usuario"]
        }), 200

    except requests.exceptions.ConnectionError:
        return jsonify({
            "mensaje": "El servicio de pagos no está disponible"
        }), 503



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5002)))