from flask import Flask, jsonify, request
import requests, os
from database import conectar

app = Flask(__name__)

usuarios_url = os.getenv("USUARIOS_URL", "http://usuarios:5000")
pagos_url = os.getenv("PAGOS_URL", "http://pagos:5000")


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
    cursor.execute(
        "SELECT * FROM citas"
    )
    citas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(citas)


@app.route("/citas/<int:id>")
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        SELECT * FROM citas
        WHERE id = %s
    """
    cursor.execute(sql, (id,))
    cita = cursor.fetchone()
    cursor.close()
    conexion.close()
    if cita is None:
        return jsonify({"mensaje": "cita no encontrada"}), 404
    return jsonify(cita)


@app.route("/citas/<int:id>/detalles")
def detalles(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        SELECT * FROM citas
        WHERE id = %s
    """
    cursor.execute(sql, (id,))
    cita = cursor.fetchone()
    cursor.close()
    conexion.close()
    if cita is None:
        return jsonify({"mensaje": "cita no encontrada"}), 404

    # comunicacion con el servicio de usuarios
    usuario = consultar(f"{usuarios_url}/usuarios/{cita['usuario_id']}")

    # comunicacion con el servicio de pagos (la cita puede no tener pago aun)
    pago = None
    if cita["pago_id"] is not None:
        pago = consultar(f"{pagos_url}/pagos/{cita['pago_id']}")

    return jsonify({
        "cita": cita,
        "usuario": usuario,
        "pago": pago
    })


@app.route("/citas", methods=["POST"])
def crear():
    nuevaCita = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        INSERT INTO citas
        (usuario_id, fecha, hora, motivo, estado, pago_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (nuevaCita["usuario_id"], nuevaCita["fecha"], nuevaCita["hora"], nuevaCita["motivo"], nuevaCita["estado"], nuevaCita.get("pago_id"))

    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "cita creada", "id": nuevo_id}), 201


@app.route("/citas/<int:id>", methods=["PUT"])
def actualizar(id):
    citaActualizada = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    sql = """
        UPDATE citas
        SET usuario_id = %s, fecha = %s, hora = %s,
            motivo = %s, estado = %s, pago_id = %s
        WHERE id = %s
    """

    valores = (citaActualizada["usuario_id"], citaActualizada["fecha"], citaActualizada["hora"], citaActualizada["motivo"], citaActualizada["estado"], citaActualizada.get("pago_id"), id)

    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": "cita actualizada"}), 200


@app.route("/citas/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        DELETE FROM citas
        WHERE id = %s
    """
    cursor.execute(sql, (id,))
    conexion.commit()
    eliminadas = cursor.rowcount
    cursor.close()
    conexion.close()
    if eliminadas == 0:
        return jsonify({"mensaje": "cita no encontrada"}), 404
    return jsonify({"mensaje": "cita eliminada"}), 200


app.run(host="0.0.0.0", port=5001)