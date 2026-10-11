
from flask import Flask, jsonify, request
import requests
import os
from database import conectar
app = Flask(__name__)
<<<<<<< HEAD

usuarios_url = os.getenv("USUARIOS_URL", "http://usuarios:5000")
=======
>>>>>>> main

usuarios_url = os.getenv("USUARIOS_URL")

@app.route("/citas", methods=["GET"])
def listar_citas():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

<<<<<<< HEAD
    cursor.execute("SELECT * FROM citas")
=======
    cursor.execute(
        "SELECT * FROM citas"
        )
>>>>>>> main
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
<<<<<<< HEAD
        return jsonify({"mensaje": "Cita no encontrada"}), 404
=======
        return jsonify({
            "mensaje": "Cita no encontrada"
        }), 404
>>>>>>> main

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
<<<<<<< HEAD
        return jsonify({"mensaje": "Cita no encontrada"}), 404

    try:
        respuesta = requests.get(f"{usuarios_url.rstrip('/')}/usuarios/{cita['usuario_id']}", timeout=5)
        usuario = respuesta.json() if respuesta.status_code == 200 else None
    except requests.exceptions.RequestException:
        usuario = None
=======
        return jsonify({
            "mensaje": "Cita no encontrada"
        }), 404


    respuesta = requests.get( f"{usuarios_url.rstrip('/')}/usuarios/{cita['usuario_id']}")

    usuario = respuesta.json()
>>>>>>> main

    return jsonify({
        "cita": cita,
        "usuario": usuario
    }), 200


@app.route("/citas", methods=["POST"])
def crear():
    nuevaCita = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
<<<<<<< HEAD

    sql = """
        INSERT INTO citas
        (usuario_id, fecha, hora, motivo, estado, pago_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        nuevaCita["usuario_id"],
        nuevaCita["fecha"],
        nuevaCita["hora"],
        nuevaCita.get("motivo"),
        nuevaCita.get("estado", "pendiente_pago"),
        nuevaCita.get("pago_id")
    )

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

    valores = (
        citaActualizada["usuario_id"], 
        citaActualizada["fecha"], 
        citaActualizada["hora"], 
        citaActualizada["motivo"], 
        citaActualizada["estado"], 
        citaActualizada["pago_id"], 
        id
    )

    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": "cita actualizada"}), 200


@app.route("/citas/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    sql_buscar = "SELECT * FROM citas WHERE id = %s"
    cursor.execute(sql_buscar, (id,))
    cita = cursor.fetchone()

    if cita is None:
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "Cita no encontrada"}), 404

    sql_eliminar = "DELETE FROM citas WHERE id = %s"
    cursor.execute(sql_eliminar, (id,))
    conexion.commit()

    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "cita eliminada", "cita": cita}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
=======
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

#@app.route("/citas", methods=["PUT"])
#def actualizar ():





app.run(host="0.0.0.0", port=5001)
>>>>>>> main
