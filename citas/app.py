
from flask import Flask, jsonify, request
import requests
import os
from database import conectar
app = Flask(__name__)

usuarios_url = os.getenv("USUARIOS_URL")

@app.route("/citas", methods=["GET"])
def listar_citas():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM citas"
        )
    citas = cursor.fetchall()
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
    cita = cursor.fetchone()
    cursor.close()
    conexion.close()

    if cita is None:
        return jsonify({
            "mensaje": "Cita no encontrada"
        }), 404

    return jsonify(cita), 200


@app.route("/citas/<int:id>/detalles", methods=["GET"])
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
        return jsonify({
            "mensaje": "Cita no encontrada"
        }), 404


    respuesta = requests.get( f"{usuarios_url.rstrip('/')}/usuarios/{cita['usuario_id']}")

    usuario = respuesta.json()

    return jsonify({
        "cita": cita,
        "usuario": usuario
    }), 200


@app.route("/citas", methods=["POST"])
def crear():
    nuevaCita = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql="""
        INSERT INTO usuarios
        (usuario_id, fecha, hora, motivo, estado, pago_id, )
        VALUES (%s, %s, %s,%s, %s,%s)
    """
    valores =(nuevaCita["usuario_id"], nuevaCita["fecha"], nuevaCita["hora"], nuevaCita["motivo"], nuevaCita["estado"], nuevaCita["pago_id"])

    cursor.execute(sql, valores)
    cursor.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "cita creada", "id": nuevo_id}), 201



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
